import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class TipoWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Tipos")
        self.geometry("600x400")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttkb.Label(frame, text="ID Tipo").grid(row=0, column=0, sticky=tk.W)
        self.entry_id = ttkb.Entry(frame, width=10)
        self.entry_id.grid(row=0, column=1, pady=5)

        ttkb.Label(frame, text="Nome do Tipo").grid(row=0, column=2, sticky=tk.W)
        self.entry_nome = ttkb.Entry(frame, width=40)
        self.entry_nome.grid(row=0, column=3, pady=5, padx=5)

        ttkb.Button(frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).grid(row=1, column=2, pady=10)
        ttkb.Button(frame, text="Remover", command=self.remover, bootstyle=DANGER).grid(row=1, column=3)

        self.tree = ttkb.Treeview(self, columns=("id_tipo", "nm_tipo"), show="headings")
        self.tree.heading("id_tipo", text="ID")
        self.tree.heading("nm_tipo", text="Descrição")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def salvar(self):
        id_tipo = self.entry_id.get()
        nome = self.entry_nome.get()

        if not id_tipo or not nome:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        try:
            id_tipo = int(id_tipo)
        except ValueError:
            messagebox.showwarning("Erro", "ID deve ser um número.")
            return

        conn = self.conectar()
        cursor = conn.cursor()

        # Verifica se já existe
        cursor.execute("SELECT COUNT(*) FROM tipo WHERE id_tipo = ?", (id_tipo,))
        existe = cursor.fetchone()[0]

        if existe:
            cursor.execute("UPDATE tipo SET nm_tipo = ? WHERE id_tipo = ?", (nome, id_tipo))
        else:
            cursor.execute("INSERT INTO tipo (id_tipo, nm_tipo) VALUES (?, ?)", (id_tipo, nome))

        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        id_tipo = self.tree.item(item)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tipo WHERE id_tipo = ?", (id_tipo,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_tipo, nm_tipo FROM tipo ORDER BY id_tipo")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        id_tipo, nome = item["values"]
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, id_tipo)
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, nome)

    def limpar(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
