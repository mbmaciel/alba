import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo

import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class CepWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Consulta de CEPs")
        self.geometry("500x350")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttkb.Label(frame, text="Buscar por CEP").grid(row=0, column=0, sticky=tk.W)
        self.entry_cep = ttkb.Entry(frame, width=20)
        self.entry_cep.grid(row=0, column=1, pady=5)

        ttkb.Button(frame, text="Buscar", command=self.buscar_cep, bootstyle=PRIMARY).grid(row=0, column=2, padx=10)

        self.tree = ttkb.Treeview(self, columns=("cep", "cidade", "uf", "bairro", "endereco"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def buscar_cep(self):
        cep_valor = self.entry_cep.get()
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT cd_cep, nm_cidade, cd_uf, nm_bairro, nm_lograd FROM cep WHERE cd_cep LIKE ?", (f"%{cep_valor}%",))
        resultados = cursor.fetchall()
        conn.close()

        self.tree.delete(*self.tree.get_children())
        for row in resultados:
            self.tree.insert("", "end", values=row)
