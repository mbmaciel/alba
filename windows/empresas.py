import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo

import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class EmpresaWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Empresas")
        self.geometry("600x400")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttkb.Label(frame, text="Razão Social").grid(row=0, column=0, sticky=tk.W)
        self.entry_razao = ttkb.Entry(frame, width=50)
        self.entry_razao.grid(row=0, column=1, columnspan=2, pady=5)

        ttkb.Label(frame, text="Nome Fantasia").grid(row=1, column=0, sticky=tk.W)
        self.entry_fantasia = ttkb.Entry(frame, width=50)
        self.entry_fantasia.grid(row=1, column=1, columnspan=2, pady=5)

        ttkb.Label(frame, text="CNPJ").grid(row=2, column=0, sticky=tk.W)
        self.entry_cnpj = ttkb.Entry(frame, width=30)
        self.entry_cnpj.grid(row=2, column=1, pady=5)

        ttkb.Button(frame, text="Salvar", command=self.salvar_empresa, bootstyle=SUCCESS).grid(row=3, column=1, sticky=tk.E, pady=10)
        ttkb.Button(frame, text="Remover", command=self.remover_empresa, bootstyle=DANGER).grid(row=3, column=2, sticky=tk.W)

        self.tree = ttkb.Treeview(self, columns=("id", "razao", "fantasia", "cnpj"), show="headings")
        # Configure all columns
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.heading("id", text="")
        
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_empresas()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def salvar_empresa(self):
        razao = self.entry_razao.get()
        fantasia = self.entry_fantasia.get()
        cnpj = self.entry_cnpj.get()

        if not razao or not cnpj:
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO empresas (nm_razao, nm_fantasia, nr_cnpj) VALUES (?, ?, ?)", (razao, fantasia, cnpj))
        conn.commit()
        conn.close()
        self.limpar_campos()
        self.carregar_empresas()

    def remover_empresa(self):
        selecionado = self.tree.focus()
        if not selecionado:
            return
        item = self.tree.item(selecionado)
        empresa_id = item["values"][0]

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM empresas WHERE id_empresa = ?", (empresa_id,))
        conn.commit()
        conn.close()
        self.carregar_empresas()

    def carregar_empresas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_empresa, nm_razao, nm_fantasia, nr_cnpj FROM empresas")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        _, razao, fantasia, cnpj = item["values"]
        self.entry_razao.delete(0, tk.END)
        self.entry_razao.insert(0, razao)
        self.entry_fantasia.delete(0, tk.END)
        self.entry_fantasia.insert(0, fantasia)
        self.entry_cnpj.delete(0, tk.END)
        self.entry_cnpj.insert(0, cnpj)

    def limpar_campos(self):
        self.entry_razao.delete(0, tk.END)
        self.entry_fantasia.delete(0, tk.END)
        self.entry_cnpj.delete(0, tk.END)
