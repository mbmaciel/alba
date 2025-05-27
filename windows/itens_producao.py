import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class ItensProducaoWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Itens de Produção (alba0009)")
        self.geometry("1000x550")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # ID Ordem de Fabricação
        ttkb.Label(frame, text="Ordem de Fabricação").grid(row=0, column=0, sticky=tk.W)
        self.combo_of = ttkb.Combobox(frame, width=20, state="readonly")
        self.combo_of.grid(row=0, column=1, padx=5, pady=5)

        # Produto
        ttkb.Label(frame, text="Produto").grid(row=0, column=2, sticky=tk.W)
        self.combo_produto = ttkb.Combobox(frame, width=40, state="readonly")
        self.combo_produto.grid(row=0, column=3, columnspan=2, padx=5, pady=5)

        # Cliente
        ttkb.Label(frame, text="Cliente").grid(row=1, column=0, sticky=tk.W)
        self.combo_cliente = ttkb.Combobox(frame, width=40, state="readonly")
        self.combo_cliente.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        ttkb.Label(frame, text="Quantidade").grid(row=1, column=3, sticky=tk.W)
        self.entry_qtd = ttkb.Entry(frame, width=10)
        self.entry_qtd.grid(row=1, column=4, padx=5)

        ttkb.Label(frame, text="Valor Unit.").grid(row=2, column=0, sticky=tk.W)
        self.entry_unit = ttkb.Entry(frame, width=15)
        self.entry_unit.grid(row=2, column=1, padx=5)

        ttkb.Label(frame, text="Desc. %").grid(row=2, column=2, sticky=tk.W)
        self.entry_desc = ttkb.Entry(frame, width=10)
        self.entry_desc.grid(row=2, column=3, padx=5)

        ttkb.Label(frame, text="Total").grid(row=2, column=4, sticky=tk.W)
        self.entry_total = ttkb.Entry(frame, width=15)
        self.entry_total.grid(row=2, column=5, padx=5)

        ttkb.Button(frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).grid(row=3, column=4, pady=10)
        ttkb.Button(frame, text="Remover", command=self.remover, bootstyle=DANGER).grid(row=3, column=5)

        self.tree = ttkb.Treeview(self, columns=("id", "of", "produto", "cliente", "qtd", "unit", "total"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.carregar_produtos()
        self.carregar_clientes()
        self.carregar_of()
        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def carregar_produtos(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_produto, cd_produto || ' - ' || nm_produto FROM alba0005 ORDER BY nm_produto")
        self.produtos = cursor.fetchall()
        conn.close()
        self.combo_produto["values"] = [desc for _, desc in self.produtos]

    def carregar_clientes(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nr_cnpj_cpf, nm_razao FROM alba0001 ORDER BY nm_razao")
        self.clientes = cursor.fetchall()
        conn.close()
        self.combo_cliente["values"] = [nome for _, nome in self.clientes]

    def carregar_of(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_of FROM alba0003 ORDER BY id_of")
        self.ordens = cursor.fetchall()
        conn.close()
        self.combo_of["values"] = [str(id) for (id,) in self.ordens]

    def salvar(self):
        id_of = int(self.combo_of.get())
        desc_prod = self.combo_produto.get()
        id_produto = next((id for id, desc in self.produtos if desc == desc_prod), None)

        nome_cliente = self.combo_cliente.get()
        cd_cliente = next((cd for cd, nome in self.clientes if nome == nome_cliente), None)

        qtd = int(self.entry_qtd.get())
        unit = float(self.entry_unit.get())
        desc = float(self.entry_desc.get())
        total = qtd * unit * (1 - desc / 100)

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alba0009 (
                id_of, id_produto, cd_cliente, qt_produto, vl_unitario,
                pc_desc_coml, pc_desc_fiscal, vl_unit_final, vl_produto,
                vl_total, fl_status, fl_comissao
            ) VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?, ?, 'ATIVO', 'S')
        """, (
            id_of, id_produto, cd_cliente, qtd, unit,
            desc, total, total, total
        ))
        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        recnum = self.tree.item(item)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alba0009 WHERE recnum = ?", (recnum,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.recnum, i.id_of,
                   p.nm_produto, c.nm_razao,
                   i.qt_produto, i.vl_unitario, i.vl_total
            FROM alba0009 i
            LEFT JOIN alba0005 p ON i.id_produto = p.id_produto
            LEFT JOIN alba0001 c ON i.cd_cliente = c.nr_cnpj_cpf
        """)
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def limpar(self):
        self.combo_of.set("")
        self.combo_produto.set("")
        self.combo_cliente.set("")
        self.entry_qtd.delete(0, tk.END)
        self.entry_unit.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.entry_total.delete(0, tk.END)
