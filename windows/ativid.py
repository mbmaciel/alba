import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class AtividWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Atividades")
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

        # Frame para campos de entrada
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        ttkb.Label(input_frame, text="Descrição da Atividade").grid(row=0, column=0, sticky=tk.W)
        self.entry_desc = ttkb.Entry(input_frame, width=60)
        self.entry_desc.grid(row=0, column=1, pady=5, padx=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "descricao"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("descricao", text="Descrição")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("descricao", width=600, minwidth=400, anchor=tk.W)
        
        # Scrollbar para o Treeview
        scrollbar = ttkb.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar()
        self.entry_desc.focus()

    def salvar(self):
        desc = self.entry_desc.get()
        if not desc:
            messagebox.showwarning("Atenção", "Descrição obrigatória.")
            return
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ativid (nm_atividade) VALUES (?)", (desc,))
        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()
        messagebox.showinfo("Sucesso", "Atividade salva com sucesso!")

    def remover(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione uma atividade para remover.")
            return
            
        id_atividade = self.tree.item(item)["values"][0]
        
        resposta = messagebox.askyesno("Confirmar", "Deseja realmente remover esta atividade?")
        if not resposta:
            return
            
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ativid WHERE id_atividade = ?", (id_atividade,))
        conn.commit()
        conn.close()
        self.carregar()
        self.limpar()
        messagebox.showinfo("Sucesso", "Atividade removida com sucesso!")

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_atividade, nm_atividade FROM ativid ORDER BY nm_atividade")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()
        
    def on_select(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item)["values"]
        if values:
            self.entry_desc.delete(0, tk.END)
            self.entry_desc.insert(0, values[1])

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.entry_desc.delete(0, tk.END)
            
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
            anterior_item = items[idx - 1]
            self.tree.selection_set(anterior_item)
            self.tree.focus(anterior_item)
            self.tree.see(anterior_item)
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
            proximo_item = items[idx + 1]
            self.tree.selection_set(proximo_item)
            self.tree.focus(proximo_item)
            self.tree.see(proximo_item)
            self.on_select(None)
