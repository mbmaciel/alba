import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo

import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class ContatoWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Contatos")
        self.geometry("600x350")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Nome do Contato with search button
        ttkb.Label(frame, text="Nome do Contato").grid(row=0, column=0, sticky=tk.W)
        
        # Create a frame to hold the entry and search button
        search_frame = ttkb.Frame(frame)
        search_frame.grid(row=0, column=1, columnspan=2, pady=5, sticky=tk.W+tk.E)
        
        self.entry_nome = ttkb.Entry(search_frame, width=45)
        self.entry_nome.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Create search button with magnifying glass icon or text
        search_button = ttkb.Button(search_frame, text="🔍", bootstyle=INFO, 
                                   command=self.buscar_contato, width=3)
        search_button.pack(side=tk.RIGHT, padx=(5, 0))

        ttkb.Label(frame, text="DDD").grid(row=1, column=0, sticky=tk.W)
        self.entry_ddd = ttkb.Entry(frame, width=10)
        self.entry_ddd.grid(row=1, column=1, pady=5)

        ttkb.Label(frame, text="Telefone").grid(row=2, column=0, sticky=tk.W)
        self.entry_telefone = ttkb.Entry(frame, width=30)
        self.entry_telefone.grid(row=2, column=1, pady=5)

        ttkb.Button(frame, text="Salvar", command=self.salvar_contato, bootstyle=SUCCESS).grid(row=3, column=1, sticky=tk.E, pady=10)
        ttkb.Button(frame, text="Remover", command=self.remover_contato, bootstyle=DANGER).grid(row=3, column=2, sticky=tk.W)
        ttkb.Button(frame, text="Limpar Filtro", command=self.carregar_contatos, bootstyle=INFO).grid(row=3, column=0, sticky=tk.W, pady=10)

        # Frame para botões de navegação
        nav_frame = ttkb.Frame(self, padding=5)
        nav_frame.pack(fill=tk.X, padx=10)

        # Botões de navegação
        ttkb.Button(nav_frame, text="⏮ Primeiro", command=self.ir_primeiro, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="◀ Anterior", command=self.ir_anterior, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Próximo ▶", command=self.ir_proximo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Último ⏭", command=self.ir_ultimo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)

        self.tree = ttkb.Treeview(self, columns=("id", "nome", "ddd", "telefone"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.heading("id", text="")
        
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_contatos()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def buscar_contato(self):
        nome_busca = self.entry_nome.get()
        if not nome_busca:
            self.carregar_contatos()
            return
            
        # Clear current treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        conn = self.conectar()
        cursor = conn.cursor()
        # Use LIKE with wildcards for partial matching
        cursor.execute("""
            SELECT id_contato, nm_contato, nr_ddd_fone, nr_telefone 
            FROM contatos 
            WHERE nm_contato LIKE ?
        """, (f'%{nome_busca}%',))
        
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def salvar_contato(self):
        nome = self.entry_nome.get()
        ddd = self.entry_ddd.get()
        telefone = self.entry_telefone.get()

        if not nome or not telefone:
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contatos (nm_contato, nr_ddd_fone, nr_telefone) VALUES (?, ?, ?)", (nome, ddd, telefone))
        conn.commit()
        conn.close()
        self.limpar_campos()
        self.carregar_contatos()

    def remover_contato(self):
        selecionado = self.tree.focus()
        if not selecionado:
            return
        item = self.tree.item(selecionado)
        contato_id = item["values"][0]

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contatos WHERE id_contato = ?", (contato_id,))
        conn.commit()
        conn.close()
        self.carregar_contatos()

    def carregar_contatos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_contato, nm_contato, nr_ddd_fone, nr_telefone FROM contatos")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        _, nome, ddd, telefone = item["values"]
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, nome)
        self.entry_ddd.delete(0, tk.END)
        self.entry_ddd.insert(0, ddd)
        self.entry_telefone.delete(0, tk.END)
        self.entry_telefone.insert(0, telefone)

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_ddd.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        
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
