import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import sqlite3
from windows.base_window import BaseWindow

class TipoWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.set_title("Cadastro de Tipos de Clientes")
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

        # Frame para campos de entrada
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        ttkb.Label(input_frame, text="ID Tipo").grid(row=0, column=0, sticky=tk.W)
        self.entry_id = ttkb.Entry(input_frame, width=10)
        self.entry_id.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Nome do Tipo").grid(row=0, column=2, sticky=tk.W)
        self.entry_nome = ttkb.Entry(input_frame, width=50)
        self.entry_nome.grid(row=0, column=3, pady=5, padx=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id_tipo", "nm_tipo"), show="headings", height=15)
            
        # Configuração das colunas - ID menor, Descrição maior
        self.tree.heading("id_tipo", text="ID")
        self.tree.heading("nm_tipo", text="Descrição")
        self.tree.column("id_tipo", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("nm_tipo", width=500, minwidth=300, anchor=tk.W)
            
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
        self.entry_id.focus()

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
