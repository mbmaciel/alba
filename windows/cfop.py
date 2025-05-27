import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo

import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class CfopWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de CFOP")
        self.geometry("700x400")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttkb.Label(frame, text="Código CFOP").grid(row=0, column=0, sticky=tk.W)
        self.entry_codigo = ttkb.Entry(frame, width=15)
        self.entry_codigo.grid(row=0, column=1, pady=5)

        ttkb.Label(frame, text="Descrição").grid(row=1, column=0, sticky=tk.W)
        self.entry_descricao = ttkb.Entry(frame, width=40)
        self.entry_descricao.grid(row=1, column=1, columnspan=2, pady=5)

        ttkb.Label(frame, text="Flag Impostos").grid(row=2, column=0, sticky=tk.W)
        self.entry_impostos = ttkb.Entry(frame, width=10)
        self.entry_impostos.grid(row=2, column=1, pady=5, sticky=tk.W)

        ttkb.Label(frame, text="Flag Kardex").grid(row=2, column=2, sticky=tk.W)
        self.entry_kardex = ttkb.Entry(frame, width=10)
        self.entry_kardex.grid(row=2, column=3, pady=5, sticky=tk.W)

        ttkb.Button(frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).grid(row=3, column=2, pady=10, sticky=tk.E)
        ttkb.Button(frame, text="Remover", command=self.remover, bootstyle=DANGER).grid(row=3, column=3, pady=10, sticky=tk.W)

        # Frame para botões de navegação
        nav_frame = ttkb.Frame(self, padding=5)
        nav_frame.pack(fill=tk.X, padx=10)

        # Botões de navegação
        ttkb.Button(nav_frame, text="⏮ Primeiro", command=self.ir_primeiro, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="◀ Anterior", command=self.ir_anterior, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Próximo ▶", command=self.ir_proximo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Último ⏭", command=self.ir_ultimo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)

        self.tree = ttkb.Treeview(self, columns=("codigo", "descricao", "impostos", "kardex"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def salvar(self):
        codigo = self.entry_codigo.get().strip()
        descricao = self.entry_descricao.get().strip()
        impostos = self.entry_impostos.get().strip()
        kardex = self.entry_kardex.get().strip()

        if not codigo or not descricao:
            messagebox.showwarning("Campos obrigatórios", "Código e descrição são obrigatórios.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT OR REPLACE INTO cfop (cd_cfop, nm_cfop, fl_impostos, fl_kardex) VALUES (?, ?, ?, ?)",
                           (codigo, descricao, impostos, kardex))
            conn.commit()
        except Exception as e:
            messagebox.showerror("Erro ao salvar", str(e))
        finally:
            conn.close()

        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        codigo = self.tree.item(item)["values"][0]

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cfop WHERE cd_cfop = ?", (codigo,))
        conn.commit()
        conn.close()

        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT cd_cfop, nm_cfop, fl_impostos, fl_kardex FROM cfop")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        codigo, descricao, impostos, kardex = item["values"]
        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, codigo)
        self.entry_descricao.delete(0, tk.END)
        self.entry_descricao.insert(0, descricao)
        self.entry_impostos.delete(0, tk.END)
        self.entry_impostos.insert(0, impostos)
        self.entry_kardex.delete(0, tk.END)
        self.entry_kardex.insert(0, kardex)

    def limpar(self):
        self.entry_codigo.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_impostos.delete(0, tk.END)
        self.entry_kardex.delete(0, tk.END)
        
    def ir_primeiro(self):
        """Navega para o primeiro registro na lista"""
        items = self.tree.get_children()
        if items:
            primeiro_item = items[0]
            self.tree.selection_set(primeiro_item)
            self.tree.focus(primeiro_item)
            self.tree.see(primeiro_item)
            self.on_select(None)
            
    def ir_ultimo(self):
        """Navega para o último registro na lista"""
        items = self.tree.get_children()
        if items:
            ultimo_item = items[-1]
            self.tree.selection_set(ultimo_item)
            self.tree.focus(ultimo_item)
            self.tree.see(ultimo_item)
            self.on_select(None)
            
    def ir_anterior(self):
        """Navega para o registro anterior na lista"""
        selecionado = self.tree.selection()
        if not selecionado:
            self.ir_primeiro()
            return
            
        items = self.tree.get_children()
        idx = items.index(selecionado[0])
        
        if idx > 0:
            anterior = items[idx - 1]
            self.tree.selection_set(anterior)
            self.tree.focus(anterior)
            self.tree.see(anterior)
            self.on_select(None)
            
    def ir_proximo(self):
        """Navega para o próximo registro na lista"""
        selecionado = self.tree.selection()
        if not selecionado:
            self.ir_primeiro()
            return
            
        items = self.tree.get_children()
        idx = items.index(selecionado[0])
        
        if idx < len(items) - 1:
            proximo = items[idx + 1]
            self.tree.selection_set(proximo)
            self.tree.focus(proximo)
            self.tree.see(proximo)
            self.on_select(None)
