import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class ProdutoFiscalWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Produtos Fiscais (alba0005)")
        self.geometry("1000x500")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttkb.Label(frame, text="Código").grid(row=0, column=0, sticky=tk.W)
        self.entry_codigo = ttkb.Entry(frame, width=20)
        self.entry_codigo.grid(row=0, column=1, padx=5, pady=5)

        ttkb.Label(frame, text="Nome").grid(row=0, column=2, sticky=tk.W)
        self.entry_nome = ttkb.Entry(frame, width=40)
        self.entry_nome.grid(row=0, column=3, columnspan=2, padx=5, pady=5)

        ttkb.Label(frame, text="NCM").grid(row=1, column=0, sticky=tk.W)
        self.combo_ncm = ttkb.Combobox(frame, width=50, state="readonly")
        self.combo_ncm.grid(row=1, column=1, columnspan=4, padx=5, pady=5)

        ttkb.Label(frame, text="Unidade").grid(row=2, column=0, sticky=tk.W)
        self.entry_unidade = ttkb.Entry(frame, width=10)
        self.entry_unidade.grid(row=2, column=1, padx=5, pady=5)

        ttkb.Label(frame, text="Valor Venda").grid(row=2, column=2, sticky=tk.W)
        self.entry_venda = ttkb.Entry(frame, width=15)
        self.entry_venda.grid(row=2, column=3, padx=5, pady=5)

        ttkb.Label(frame, text="Tipo").grid(row=2, column=4, sticky=tk.W)
        self.entry_tipo = ttkb.Entry(frame, width=10)
        self.entry_tipo.grid(row=2, column=5, padx=5, pady=5)

        ttkb.Button(frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).grid(row=3, column=3, pady=10)
        ttkb.Button(frame, text="Remover", command=self.remover, bootstyle=DANGER).grid(row=3, column=4)

        # Frame para botões de navegação
        nav_frame = ttkb.Frame(self, padding=5)
        nav_frame.pack(fill=tk.X, padx=10)

        # Botões de navegação
        ttkb.Button(nav_frame, text="⏮ Primeiro", command=self.ir_primeiro, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="◀ Anterior", command=self.ir_anterior, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Próximo ▶", command=self.ir_proximo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Último ⏭", command=self.ir_ultimo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)

        self.tree = ttkb.Treeview(self, columns=("id", "codigo", "nome", "ncm", "valor"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_ncm()
        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def carregar_ncm(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT cd_ncm, nm_ncm FROM ncm ORDER BY cd_ncm")
        self.ncms = cursor.fetchall()
        conn.close()
        self.combo_ncm["values"] = [f"{cd} - {ds}" for cd, ds in self.ncms]

    def salvar(self):
        codigo = self.entry_codigo.get()
        nome = self.entry_nome.get()
        unidade = self.entry_unidade.get()
        tipo = self.entry_tipo.get()
        valor = self.entry_venda.get()

        ncm_label = self.combo_ncm.get()
        cd_ncm = ncm_label.split(" - ")[0] if " - " in ncm_label else ncm_label

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alba0005 (cd_produto, nm_produto, cd_unidade, fl_tipo, cd_ncm, vl_venda)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (codigo, nome, unidade, tipo, cd_ncm, valor))
        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        id_produto = self.tree.item(item)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alba0005 WHERE id_produto = ?", (id_produto,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id_produto, p.cd_produto, p.nm_produto, n.nm_ncm, p.vl_venda
            FROM alba0005 p
            LEFT JOIN ncm n ON p.cd_ncm = n.cd_ncm
        """)
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        _, codigo, nome, ncm_desc, valor = item["values"]
        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, codigo)
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, nome)
        self.entry_venda.delete(0, tk.END)
        self.entry_venda.insert(0, valor)
        self.combo_ncm.set(ncm_desc or "")

    def limpar(self):
        self.entry_codigo.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_unidade.delete(0, tk.END)
        self.entry_tipo.delete(0, tk.END)
        self.entry_venda.delete(0, tk.END)
        self.combo_ncm.set("")
        
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
