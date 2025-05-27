import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo

import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class AtividWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Atividades")
        self.geometry("500x350")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttkb.Label(frame, text="Descrição da Atividade").grid(row=0, column=0, sticky=tk.W)
        self.entry_desc = ttkb.Entry(frame, width=50)
        self.entry_desc.grid(row=0, column=1, pady=5)

        ttkb.Button(frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).grid(row=1, column=1, sticky=tk.E, pady=10)
        ttkb.Button(frame, text="Remover", command=self.remover, bootstyle=DANGER).grid(row=1, column=2, sticky=tk.W)

        # Frame para botões de navegação
        nav_frame = ttkb.Frame(self, padding=5)
        nav_frame.pack(fill=tk.X, padx=10)

        # Botões de navegação
        ttkb.Button(nav_frame, text="⏮ Primeiro", command=self.ir_primeiro, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="◀ Anterior", command=self.ir_anterior, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Próximo ▶", command=self.ir_proximo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Último ⏭", command=self.ir_ultimo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)

        self.tree = ttkb.Treeview(self, columns=("id", "descricao"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("descricao", text="Descrição")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def salvar(self):
        desc = self.entry_desc.get()
        if not desc:
            messagebox.showwarning("Atenção", "Descrição obrigatória.")
            return
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ativid (nm_atividade) VALUES (?)", (desc,))
        conn.commit()
        conn.close()
        self.entry_desc.delete(0, tk.END)
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        id_atividade = self.tree.item(item)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ativid WHERE id_atividade = ?", (id_atividade,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_atividade, nm_atividade FROM ativid")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()
        
    def on_select(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item)["values"]
        if values:
            self.entry_desc.delete(0, tk.END)
            self.entry_desc.insert(0, values[1])
            
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
            anterior_item = items[idx - 1]
            self.tree.selection_set(anterior_item)
            self.tree.focus(anterior_item)
            self.tree.see(anterior_item)
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
            proximo_item = items[idx + 1]
            self.tree.selection_set(proximo_item)
            self.tree.focus(proximo_item)
            self.tree.see(proximo_item)
            self.on_select(None)
