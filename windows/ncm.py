import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class NcmWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Consulta de NCM")
        self.geometry("700x500")
        self.resizable(False, False)

        # Frame principal
        main_frame = ttkb.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Barra de ferramentas no topo
        toolbar_frame = ttkb.Frame(main_frame, relief="raised", borderwidth=2, padding=5)
        toolbar_frame.pack(fill=tk.X, pady=(0, 15))

        # Container para os botões grudados
        button_container = ttkb.Frame(toolbar_frame)
        button_container.pack(side=tk.LEFT)

        # Botões da barra de ferramentas com ícones
        self.btn_novo = ttkb.Button(button_container, text="➕", command=self.novo, width=3)
        self.btn_novo.pack(side=tk.LEFT)

        self.btn_salvar = ttkb.Button(button_container, text="💾", command=self.salvar, width=3)
        self.btn_salvar.pack(side=tk.LEFT)

        self.btn_remover = ttkb.Button(button_container, text="🗑️", command=self.remover, width=3)
        self.btn_remover.pack(side=tk.LEFT)

        # Separador visual
        separator = ttkb.Separator(toolbar_frame, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

        # Botões de navegação
        nav_container = ttkb.Frame(toolbar_frame)
        nav_container.pack(side=tk.LEFT, padx=(10, 0))

        ttkb.Button(nav_container, text="⏮", command=self.ir_primeiro, width=3).pack(side=tk.LEFT)
        ttkb.Button(nav_container, text="◀", command=self.ir_anterior, width=3).pack(side=tk.LEFT)
        ttkb.Button(nav_container, text="▶", command=self.ir_proximo, width=3).pack(side=tk.LEFT)
        ttkb.Button(nav_container, text="⏭", command=self.ir_ultimo, width=3).pack(side=tk.LEFT)

        # Separador visual
        separator2 = ttkb.Separator(toolbar_frame, orient=tk.VERTICAL)
        separator2.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

        # Botão de busca
        search_container = ttkb.Frame(toolbar_frame)
        search_container.pack(side=tk.LEFT, padx=(10, 0))

        ttkb.Button(search_container, text="🔍", command=self.buscar_ncm, width=3).pack(side=tk.LEFT)

        # Frame para campos de entrada
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        ttkb.Label(input_frame, text="Código NCM").grid(row=0, column=0, sticky=tk.W)
        self.entry_codigo = ttkb.Entry(input_frame, width=15)
        self.entry_codigo.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Descrição").grid(row=0, column=2, sticky=tk.W)
        self.entry_descricao = ttkb.Entry(input_frame, width=60)
        self.entry_descricao.grid(row=0, column=3, pady=5, padx=5)

        # Frame para busca
        search_frame = ttkb.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 15))

        ttkb.Label(search_frame, text="Buscar código NCM").grid(row=0, column=0, sticky=tk.W)
        self.entry_busca = ttkb.Entry(search_frame, width=30)
        self.entry_busca.grid(row=0, column=1, pady=5, padx=(5, 10))
        self.entry_busca.bind("<Return>", lambda e: self.buscar_ncm())

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("codigo", "descricao"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("codigo", text="Código")
        self.tree.heading("descricao", text="Descrição")
        self.tree.column("codigo", width=120, minwidth=100, anchor=tk.CENTER)
        self.tree.column("descricao", width=500, minwidth=300, anchor=tk.W)
        
        # Scrollbar para o Treeview
        scrollbar = ttkb.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar()
        self.entry_codigo.focus()

    def salvar(self):
        codigo = self.entry_codigo.get()
        descricao = self.entry_descricao.get()

        if not codigo or not descricao:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        conn = self.conectar()
        cursor = conn.cursor()

        # Verifica se já existe
        cursor.execute("SELECT COUNT(*) FROM ncm WHERE cd_ncm = ?", (codigo,))
        existe = cursor.fetchone()[0]

        if existe:
            cursor.execute("UPDATE ncm SET nm_ncm = ? WHERE cd_ncm = ?", (descricao, codigo))
        else:
            cursor.execute("INSERT INTO ncm (cd_ncm, nm_ncm) VALUES (?, ?)", (codigo, descricao))

        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        codigo = self.tree.item(item)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ncm WHERE cd_ncm = ?", (codigo,))
        conn.commit()
        conn.close()
        self.carregar()

    def buscar_ncm(self):
        codigo = self.entry_busca.get()
        if not codigo:
            self.carregar()
            return
            
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT cd_ncm, nm_ncm FROM ncm WHERE cd_ncm LIKE ? OR nm_ncm LIKE ? ORDER BY cd_ncm", 
                      (f"%{codigo}%", f"%{codigo}%"))
        resultados = cursor.fetchall()
        conn.close()

        self.tree.delete(*self.tree.get_children())
        for row in resultados:
            self.tree.insert("", "end", values=row)

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT cd_ncm, nm_ncm FROM ncm ORDER BY cd_ncm")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        codigo, descricao = item["values"]
        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, codigo)
        self.entry_descricao.delete(0, tk.END)
        self.entry_descricao.insert(0, descricao)

    def limpar(self):
        self.entry_codigo.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_busca.delete(0, tk.END)
        
