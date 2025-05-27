import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo

import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class NatopWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Naturezas da Operação (NATOP)")
        self.geometry("850x450")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttkb.Label(frame, text="Descrição").grid(row=0, column=0, sticky=tk.W)
        self.entry_desc = ttkb.Entry(frame, width=40)
        self.entry_desc.grid(row=0, column=1, pady=5)

        ttkb.Label(frame, text="CFOP").grid(row=1, column=0, sticky=tk.W)
        self.entry_cfop = ttkb.Entry(frame, width=20)
        self.entry_cfop.grid(row=1, column=1, pady=5)

        ttkb.Label(frame, text="Fluxo").grid(row=2, column=0, sticky=tk.W)
        self.entry_fluxo = ttkb.Entry(frame, width=20)
        self.entry_fluxo.grid(row=2, column=1, pady=5)

        ttkb.Label(frame, text="Livro Entrada").grid(row=0, column=2, sticky=tk.W)
        self.entry_ent = ttkb.Entry(frame, width=10)
        self.entry_ent.grid(row=0, column=3, pady=5)

        ttkb.Label(frame, text="Livro Saída").grid(row=1, column=2, sticky=tk.W)
        self.entry_sai = ttkb.Entry(frame, width=10)
        self.entry_sai.grid(row=1, column=3, pady=5)

        ttkb.Label(frame, text="Livro Serviço").grid(row=2, column=2, sticky=tk.W)
        self.entry_srv = ttkb.Entry(frame, width=10)
        self.entry_srv.grid(row=2, column=3, pady=5)

        ttkb.Button(frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).grid(row=3, column=1, pady=10, sticky=tk.E)
        ttkb.Button(frame, text="Remover", command=self.remover, bootstyle=DANGER).grid(row=3, column=2, sticky=tk.W)

        # Frame para botões de navegação
        nav_frame = ttkb.Frame(self, padding=5)
        nav_frame.pack(fill=tk.X, padx=10)

        # Botões de navegação
        ttkb.Button(nav_frame, text="⏮ Primeiro", command=self.ir_primeiro, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="◀ Anterior", command=self.ir_anterior, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Próximo ▶", command=self.ir_proximo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Último ⏭", command=self.ir_ultimo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)

        self.tree = ttkb.Treeview(self, columns=("id", "desc", "cfop", "fluxo", "ent", "sai", "srv"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def salvar(self):
        desc = self.entry_desc.get()
        cfop = self.entry_cfop.get()
        fluxo = self.entry_fluxo.get()
        ent = self.entry_ent.get()
        sai = self.entry_sai.get()
        srv = self.entry_srv.get()

        if not desc or not cfop:
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO natop (ds_natop, cd_cfop, fl_fluxo, fl_livro_ent, fl_livro_sai, fl_livro_srv)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (desc, cfop, fluxo, ent, sai, srv)
        )
        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        id_natop = self.tree.item(item)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM natop WHERE id_natop = ?", (id_natop,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_natop, ds_natop, cd_cfop, fl_fluxo, fl_livro_ent, fl_livro_sai, fl_livro_srv FROM natop")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        _, desc, cfop, fluxo, ent, sai, srv = item["values"]
        self.entry_desc.delete(0, tk.END)
        self.entry_desc.insert(0, desc)
        self.entry_cfop.delete(0, tk.END)
        self.entry_cfop.insert(0, cfop)
        self.entry_fluxo.delete(0, tk.END)
        self.entry_fluxo.insert(0, fluxo)
        self.entry_ent.delete(0, tk.END)
        self.entry_ent.insert(0, ent)
        self.entry_sai.delete(0, tk.END)
        self.entry_sai.insert(0, sai)
        self.entry_srv.delete(0, tk.END)
        self.entry_srv.insert(0, srv)

    def limpar(self):
        self.entry_desc.delete(0, tk.END)
        self.entry_cfop.delete(0, tk.END)
        self.entry_fluxo.delete(0, tk.END)
        self.entry_ent.delete(0, tk.END)
        self.entry_sai.delete(0, tk.END)
        self.entry_srv.delete(0, tk.END)

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
    

