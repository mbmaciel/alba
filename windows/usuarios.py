import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo

import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class UsuarioWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Usuários")
        self.geometry("500x350")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttkb.Label(frame, text="Nome do Usuário").grid(row=0, column=0, sticky=tk.W)
        self.entry_nome = ttkb.Entry(frame, width=40)
        self.entry_nome.grid(row=0, column=1, pady=5)

        ttkb.Button(frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).grid(row=1, column=1, sticky=tk.E, pady=10)
        ttkb.Button(frame, text="Remover", command=self.remover, bootstyle=DANGER).grid(row=1, column=2, sticky=tk.W)

        self.tree = ttkb.Treeview(self, columns=("id", "nome"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)
        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def salvar(self):
        nome = self.entry_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Nome obrigatório")
            return
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuario (nm_nome) VALUES (?)", (nome,))
        conn.commit()
        conn.close()
        self.entry_nome.delete(0, tk.END)
        self.carregar()

    def remover(self):
        selecionado = self.tree.focus()
        if not selecionado:
            return
        id_usuario = self.tree.item(selecionado)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nm_nome FROM usuario")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if item:
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, item["values"][1])
