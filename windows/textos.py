import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class TextosWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Textos")
        self.geometry("800x600")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttkb.Label(frame, text="ID Texto").grid(row=0, column=0, sticky=tk.W)
        self.entry_id = ttkb.Entry(frame, width=10)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        ttkb.Label(frame, text="Descrição").grid(row=0, column=2, sticky=tk.W)
        self.entry_desc = ttkb.Entry(frame, width=50)
        self.entry_desc.grid(row=0, column=3, padx=5, pady=5)

        ttkb.Label(frame, text="Prazo").grid(row=1, column=0, sticky=tk.W)
        self.entry_prazo = ttkb.Entry(frame, width=80)
        self.entry_prazo.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        ttkb.Label(frame, text="Condições").grid(row=2, column=0, sticky=tk.W)
        self.entry_condicoes = ttkb.Entry(frame, width=80)
        self.entry_condicoes.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

        ttkb.Label(frame, text="Observações").grid(row=3, column=0, sticky=tk.W)
        self.entry_obs = ttkb.Entry(frame, width=80)
        self.entry_obs.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

        ttkb.Label(frame, text="Tipo de Texto").grid(row=4, column=0, sticky=tk.W)
        self.entry_tipo = ttkb.Entry(frame, width=20)
        self.entry_tipo.grid(row=4, column=1, padx=5, pady=5)

        ttkb.Button(frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).grid(row=5, column=2, pady=10)
        ttkb.Button(frame, text="Remover", command=self.remover, bootstyle=DANGER).grid(row=5, column=3)

        self.tree = ttkb.Treeview(self, columns=("id_texto", "nm_descricao", "tp_tipo"), show="headings")
        self.tree.heading("id_texto", text="ID")
        self.tree.heading("nm_descricao", text="Descrição")
        self.tree.heading("tp_tipo", text="Tipo")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def salvar(self):
        id_texto = self.entry_id.get()
        desc = self.entry_desc.get()
        prazo = self.entry_prazo.get()
        cond = self.entry_condicoes.get()
        obs = self.entry_obs.get()
        tipo = self.entry_tipo.get()

        if not id_texto or not desc:
            messagebox.showwarning("Atenção", "Preencha ao menos ID e Descrição.")
            return

        try:
            id_texto = int(id_texto)
        except ValueError:
            messagebox.showwarning("Erro", "ID deve ser um número.")
            return

        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM textos WHERE id_texto = ?", (id_texto,))
        existe = cursor.fetchone()[0]

        if existe:
            cursor.execute("""
                UPDATE textos SET
                    nm_descricao = ?, tx_prazo = ?, tx_condicoes = ?,
                    tx_obs = ?, tp_tipo = ?
                WHERE id_texto = ?
            """, (desc, prazo, cond, obs, tipo, id_texto))
        else:
            cursor.execute("""
                INSERT INTO textos (
                    id_texto, nm_descricao, tx_prazo, tx_condicoes, tx_obs, tp_tipo
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (id_texto, desc, prazo, cond, obs, tipo))

        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        id_texto = self.tree.item(item)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM textos WHERE id_texto = ?", (id_texto,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_texto, nm_descricao, tp_tipo FROM textos ORDER BY id_texto")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        id_texto, desc, tipo = item["values"]

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tx_prazo, tx_condicoes, tx_obs FROM textos WHERE id_texto = ?
        """, (id_texto,))
        result = cursor.fetchone()
        conn.close()

        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, id_texto)

        self.entry_desc.delete(0, tk.END)
        self.entry_desc.insert(0, desc)

        self.entry_tipo.delete(0, tk.END)
        self.entry_tipo.insert(0, tipo or "")

        self.entry_prazo.delete(0, tk.END)
        self.entry_prazo.insert(0, result[0] if result else "")

        self.entry_condicoes.delete(0, tk.END)
        self.entry_condicoes.insert(0, result[1] if result else "")

        self.entry_obs.delete(0, tk.END)
        self.entry_obs.insert(0, result[2] if result else "")

    def limpar(self):
        for entry in [
            self.entry_id, self.entry_desc, self.entry_prazo,
            self.entry_condicoes, self.entry_obs, self.entry_tipo
        ]:
            entry.delete(0, tk.END)
