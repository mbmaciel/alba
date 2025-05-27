import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo

import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class ComissaoWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Faixas de Comissão")
        self.geometry("600x350")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttkb.Label(frame, text="Desconto Inicial (%)").grid(row=0, column=0, sticky=tk.W)
        self.entry_ini = ttkb.Entry(frame, width=15)
        self.entry_ini.grid(row=0, column=1, padx=5, pady=5)

        ttkb.Label(frame, text="Desconto Final (%)").grid(row=1, column=0, sticky=tk.W)
        self.entry_fim = ttkb.Entry(frame, width=15)
        self.entry_fim.grid(row=1, column=1, padx=5, pady=5)

        ttkb.Label(frame, text="Comissão (%)").grid(row=2, column=0, sticky=tk.W)
        self.entry_comissao = ttkb.Entry(frame, width=15)
        self.entry_comissao.grid(row=2, column=1, padx=5, pady=5)

        ttkb.Button(frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).grid(row=3, column=1, pady=10, sticky=tk.E)
        ttkb.Button(frame, text="Remover", command=self.remover, bootstyle=DANGER).grid(row=3, column=2, padx=10)

        self.tree = ttkb.Treeview(self, columns=("id", "desc_ini", "desc_fim", "comissao"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.replace("_", " ").capitalize())
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def salvar(self):
        try:
            ini = float(self.entry_ini.get())
            fim = float(self.entry_fim.get())
            comissao = float(self.entry_comissao.get())
        except ValueError:
            messagebox.showerror("Erro", "Insira valores numéricos válidos.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO comissao (pc_desc_ini, pc_desc_fim, pc_comissao)
            VALUES (?, ?, ?)
        """, (ini, fim, comissao))
        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        id_comissao = self.tree.item(item)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM comissao WHERE id_comissao = ?", (id_comissao,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_comissao, pc_desc_ini, pc_desc_fim, pc_comissao FROM comissao")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        _, ini, fim, comissao = item["values"]
        self.entry_ini.delete(0, tk.END)
        self.entry_ini.insert(0, ini)
        self.entry_fim.delete(0, tk.END)
        self.entry_fim.insert(0, fim)
        self.entry_comissao.delete(0, tk.END)
        self.entry_comissao.insert(0, comissao)

    def limpar(self):
        self.entry_ini.delete(0, tk.END)
        self.entry_fim.delete(0, tk.END)
        self.entry_comissao.delete(0, tk.END)
