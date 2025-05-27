import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo

import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class NcmWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Consulta de NCM")
        self.geometry("600x350")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttkb.Label(frame, text="Buscar código NCM").grid(row=0, column=0, sticky=tk.W)
        self.entry_ncm = ttkb.Entry(frame, width=30)
        self.entry_ncm.grid(row=0, column=1, pady=5)
        ttkb.Button(frame, text="Buscar", command=self.buscar_ncm, bootstyle=PRIMARY).grid(row=0, column=2, padx=10)

        self.tree = ttkb.Treeview(self, columns=("codigo", "descricao"), show="headings")
        self.tree.heading("codigo", text="Código")
        self.tree.heading("descricao", text="Descrição")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def buscar_ncm(self):
        codigo = self.entry_ncm.get()
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT cd_ncm, nm_ncm FROM ncm WHERE cd_ncm LIKE ?", (f"%{codigo}%",))
        resultados = cursor.fetchall()
        conn.close()

        self.tree.delete(*self.tree.get_children())
        for row in resultados:
            self.tree.insert("", "end", values=row)
