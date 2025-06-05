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
        self.geometry("900x600")
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

        self.btn_salvar = ttkb.Button(button_container, text="💾", command=self.salvar_contato, width=3)
        self.btn_salvar.pack(side=tk.LEFT)

        self.btn_remover = ttkb.Button(button_container, text="🗑️", command=self.remover_contato, width=3)
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

        ttkb.Button(search_container, text="🔍", command=self.buscar_contato, width=3).pack(side=tk.LEFT)
        ttkb.Button(search_container, text="🔄", command=self.carregar_contatos, width=3).pack(side=tk.LEFT)

        # Frame para campos de entrada
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        # Primeira linha
        ttkb.Label(input_frame, text="Nome do Contato").grid(row=0, column=0, sticky=tk.W)
        self.entry_nome = ttkb.Entry(input_frame, width=45)
        self.entry_nome.grid(row=0, column=1, columnspan=2, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Departamento").grid(row=0, column=3, sticky=tk.W)
        self.entry_depto = ttkb.Entry(input_frame, width=30)
        self.entry_depto.grid(row=0, column=4, pady=5, padx=5)

        # Segunda linha
        ttkb.Label(input_frame, text="DDD").grid(row=1, column=0, sticky=tk.W)
        self.entry_ddd = ttkb.Entry(input_frame, width=10)
        self.entry_ddd.grid(row=1, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Telefone").grid(row=1, column=2, sticky=tk.W)
        self.entry_telefone = ttkb.Entry(input_frame, width=20)
        self.entry_telefone.grid(row=1, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Ramal").grid(row=1, column=4, sticky=tk.W)
        self.entry_ramal = ttkb.Entry(input_frame, width=15)
        self.entry_ramal.grid(row=1, column=5, pady=5, padx=5)

        # Terceira linha
        ttkb.Label(input_frame, text="DDD Celular").grid(row=2, column=0, sticky=tk.W)
        self.entry_ddd_cel = ttkb.Entry(input_frame, width=10)
        self.entry_ddd_cel.grid(row=2, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Celular").grid(row=2, column=2, sticky=tk.W)
        self.entry_celular = ttkb.Entry(input_frame, width=20)
        self.entry_celular.grid(row=2, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Email").grid(row=2, column=4, sticky=tk.W)
        self.entry_email = ttkb.Entry(input_frame, width=30)
        self.entry_email.grid(row=2, column=5, pady=5, padx=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "nome", "ddd", "telefone", "celular", "depto", "email"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("ddd", text="DDD")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("celular", text="Celular")
        self.tree.heading("depto", text="Departamento")
        self.tree.heading("email", text="Email")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("nome", width=200, minwidth=150, anchor=tk.W)
        self.tree.column("ddd", width=60, minwidth=50, anchor=tk.CENTER)
        self.tree.column("telefone", width=120, minwidth=100, anchor=tk.CENTER)
        self.tree.column("celular", width=120, minwidth=100, anchor=tk.CENTER)
        self.tree.column("depto", width=150, minwidth=100, anchor=tk.W)
        self.tree.column("email", width=200, minwidth=150, anchor=tk.W)
        
        # Scrollbar para o Treeview
        scrollbar = ttkb.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_contatos()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar_campos()
        self.entry_nome.focus()

    def buscar_contato(self):
        nome_busca = self.entry_nome.get()
        if not nome_busca:
            self.carregar_contatos()
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_contato, nm_contato, nr_ddd_fone, nr_telefone, nr_celular, nm_depto, nm_email
            FROM contatos 
            WHERE nm_contato LIKE ?
            ORDER BY nm_contato
        """, (f'%{nome_busca}%',))
        for row in cursor.fetchall():
            # Formatar celular com DDD
            id_contato, nome, ddd, telefone, celular, depto, email = row
            celular_formatado = f"{row[4] or ''}"  # nr_celular já pode conter DDD
            self.tree.insert("", "end", values=(id_contato, nome, ddd, telefone, celular_formatado, depto, email))
        conn.close()

    def salvar_contato(self):
        nome = self.entry_nome.get()
        ddd = self.entry_ddd.get()
        telefone = self.entry_telefone.get()
        ramal = self.entry_ramal.get()
        ddd_cel = self.entry_ddd_cel.get()
        celular = self.entry_celular.get()
        depto = self.entry_depto.get()
        email = self.entry_email.get()

        if not nome or not telefone:
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios: Nome e Telefone.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contatos (nm_contato, nr_ddd_fone, nr_telefone, nr_ramal, nr_ddd_cel, nr_celular, nm_depto, nm_email) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nome, ddd, telefone, ramal, ddd_cel, celular, depto, email))
        conn.commit()
        conn.close()
        self.limpar_campos()
        self.carregar_contatos()
        messagebox.showinfo("Sucesso", "Contato salvo com sucesso!")

    def remover_contato(self):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um contato para remover.")
            return
            
        item = self.tree.item(selecionado)
        contato_id = item["values"][0]
        
        resposta = messagebox.askyesno("Confirmar", "Deseja realmente remover este contato?")
        if not resposta:
            return
            
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contatos WHERE id_contato = ?", (contato_id,))
        conn.commit()
        conn.close()
        self.carregar_contatos()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Contato removido com sucesso!")

    def carregar_contatos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_contato, nm_contato, nr_ddd_fone, nr_telefone, nr_celular, nm_depto, nm_email 
            FROM contatos 
            ORDER BY nm_contato
        """)
        for row in cursor.fetchall():
            # Formatar celular com DDD
            id_contato, nome, ddd, telefone, celular, depto, email = row
            celular_formatado = f"{celular or ''}"
            self.tree.insert("", "end", values=(id_contato, nome, ddd, telefone, celular_formatado, depto, email))
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        
        contato_id = item["values"][0]
        
        # Buscar todos os dados do contato selecionado
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nm_contato, nr_ddd_fone, nr_telefone, nr_ramal, nr_ddd_cel, nr_celular, nm_depto, nm_email
            FROM contatos 
            WHERE id_contato = ?
        """, (contato_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            nome, ddd, telefone, ramal, ddd_cel, celular, depto, email = result
            
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, nome or "")
            
            self.entry_ddd.delete(0, tk.END)
            self.entry_ddd.insert(0, ddd or "")
            
            self.entry_telefone.delete(0, tk.END)
            self.entry_telefone.insert(0, telefone or "")
            
            self.entry_ramal.delete(0, tk.END)
            self.entry_ramal.insert(0, ramal or "")
            
            self.entry_ddd_cel.delete(0, tk.END)
            self.entry_ddd_cel.insert(0, ddd_cel or "")
            
            self.entry_celular.delete(0, tk.END)
            self.entry_celular.insert(0, celular or "")
            
            self.entry_depto.delete(0, tk.END)
            self.entry_depto.insert(0, depto or "")
            
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, email or "")

    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.entry_nome.delete(0, tk.END)
        self.entry_ddd.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_ramal.delete(0, tk.END)
        self.entry_ddd_cel.delete(0, tk.END)
        self.entry_celular.delete(0, tk.END)
        self.entry_depto.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

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
