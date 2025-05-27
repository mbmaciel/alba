import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo

import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class TiponfWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Tipos de Nota Fiscal")
        self.geometry("650x400")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttkb.Label(frame, text="Nome").grid(row=0, column=0, sticky=tk.W)
        self.entry_nome = ttkb.Entry(frame, width=40)
        self.entry_nome.grid(row=0, column=1, pady=5)

        ttkb.Label(frame, text="Tipo (fl_tiponf)").grid(row=1, column=0, sticky=tk.W)
        self.entry_tipo = ttkb.Entry(frame, width=30)
        self.entry_tipo.grid(row=1, column=1, pady=5)

        ttkb.Label(frame, text="Mapa (fl_mapa)").grid(row=2, column=0, sticky=tk.W)
        self.entry_mapa = ttkb.Entry(frame, width=30)
        self.entry_mapa.grid(row=2, column=1, pady=5)

        ttkb.Button(frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).grid(row=3, column=1, sticky=tk.E, pady=10)
        ttkb.Button(frame, text="Remover", command=self.remover, bootstyle=DANGER).grid(row=3, column=2, sticky=tk.W)

        # Frame para botões de navegação
        nav_frame = ttkb.Frame(self, padding=5)
        nav_frame.pack(fill=tk.X, padx=10)

        # Botões de navegação
        ttkb.Button(nav_frame, text="⏮ Primeiro", command=self.ir_primeiro, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="◀ Anterior", command=self.ir_anterior, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Próximo ▶", command=self.ir_proximo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Último ⏭", command=self.ir_ultimo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)

        self.tree = ttkb.Treeview(self, columns=("id", "nome", "tipo", "mapa"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.heading("id", text="")
            
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def salvar(self):
        nome = self.entry_nome.get()
        tipo = self.entry_tipo.get()
        mapa = self.entry_mapa.get()

        if not nome:
            messagebox.showwarning("Atenção", "Nome é obrigatório.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tiponf (nm_tiponf, fl_tiponf, fl_mapa) VALUES (?, ?, ?)",
            (nome, tipo, mapa)
        )
        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        id_tiponf = self.tree.item(item)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tiponf WHERE id_tiponf = ?", (id_tiponf,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_tiponf, nm_tiponf, fl_tiponf, fl_mapa FROM tiponf")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        _, nome, tipo, mapa = item["values"]
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, nome)
        self.entry_tipo.delete(0, tk.END)
        self.entry_tipo.insert(0, tipo)
        self.entry_mapa.delete(0, tk.END)
        self.entry_mapa.insert(0, mapa)

    def limpar(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_tipo.delete(0, tk.END)
        self.entry_mapa.delete(0, tk.END)
        
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
