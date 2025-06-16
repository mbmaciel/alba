import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class TiponfWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Cadastro de Tipos de Nota Fiscal")
        self.config(width=700, height=500)

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

        # Frame para campos de entrada
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        ttkb.Label(input_frame, text="Nome").grid(row=0, column=0, sticky=tk.W)
        self.entry_nome = ttkb.Entry(input_frame, width=40)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Tipo (fl_tiponf)").grid(row=1, column=0, sticky=tk.W)
        self.entry_tipo = ttkb.Entry(input_frame, width=30)
        self.entry_tipo.grid(row=1, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Mapa (fl_mapa)").grid(row=2, column=0, sticky=tk.W)
        self.entry_mapa = ttkb.Entry(input_frame, width=30)
        self.entry_mapa.grid(row=2, column=1, pady=5, padx=(5, 20))

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "nome", "tipo", "mapa"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("mapa", text="Mapa")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("nome", width=300, minwidth=200, anchor=tk.W)
        self.tree.column("tipo", width=150, minwidth=100, anchor=tk.CENTER)
        self.tree.column("mapa", width=150, minwidth=100, anchor=tk.CENTER)
        
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
        self.entry_nome.focus()

    def salvar(self):
        nome = self.entry_nome.get()
        tipo = self.entry_tipo.get()
        mapa = self.entry_mapa.get()

        if not nome:
            messagebox.showwarning("Atenção", "Nome é obrigatório.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tiponf (nm_tiponf, fl_tiponf, fl_mapa) VALUES (?, ?, ?)",
            (nome, tipo, mapa)
        )
        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        id_tiponf = self.tree.item(item)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tiponf WHERE id_tiponf = ?", (id_tiponf,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_tiponf, nm_tiponf, fl_tiponf, fl_mapa FROM tiponf")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        _, nome, tipo, mapa = item["values"]
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, nome)
        self.entry_tipo.delete(0, tk.END)
        self.entry_tipo.insert(0, tipo)
        self.entry_mapa.delete(0, tk.END)
        self.entry_mapa.insert(0, mapa)

    def limpar(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_tipo.delete(0, tk.END)
        self.entry_mapa.delete(0, tk.END)
        
