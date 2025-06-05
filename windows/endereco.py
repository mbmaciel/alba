import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class EnderecoWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Endereços (alba0002)")
        self.geometry("900x500")
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

        # Primeira linha
        ttkb.Label(input_frame, text="Pessoa").grid(row=0, column=0, sticky=tk.W)
        self.combo_pessoa = ttkb.Combobox(input_frame, width=40, state="readonly")
        self.combo_pessoa.grid(row=0, column=1, columnspan=2, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Tipo").grid(row=0, column=3, sticky=tk.W)
        self.combo_tipo = ttkb.Combobox(input_frame, width=15, state="readonly")
        self.combo_tipo["values"] = ["E", "C", "F"]
        self.combo_tipo.grid(row=0, column=4, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="CEP").grid(row=0, column=5, sticky=tk.W)
        self.entry_cep = ttkb.Entry(input_frame, width=15)
        self.entry_cep.grid(row=0, column=6, pady=5, padx=5)

        # Segunda linha
        ttkb.Label(input_frame, text="Número").grid(row=1, column=0, sticky=tk.W)
        self.entry_numero = ttkb.Entry(input_frame, width=15)
        self.entry_numero.grid(row=1, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Complemento").grid(row=1, column=2, sticky=tk.W)
        self.entry_compl = ttkb.Entry(input_frame, width=40)
        self.entry_compl.grid(row=1, column=3, columnspan=4, pady=5, padx=(5, 0), sticky=tk.W+tk.E)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "pessoa", "tipo", "cep", "numero", "compl"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("pessoa", text="Pessoa")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("cep", text="CEP")
        self.tree.heading("numero", text="Número")
        self.tree.heading("compl", text="Complemento")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("pessoa", width=250, minwidth=200, anchor=tk.W)
        self.tree.column("tipo", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column("cep", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column("numero", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("compl", width=200, minwidth=150, anchor=tk.W)
        
        # Scrollbar para o Treeview
        scrollbar = ttkb.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_pessoas()
        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar()
        self.combo_pessoa.focus()

    def carregar_pessoas(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_pessoa, nm_razao FROM alba0001 ORDER BY nm_razao")
        self.pessoas = cursor.fetchall()
        conn.close()
        self.combo_pessoa["values"] = [nome for _, nome in self.pessoas]

    def salvar(self):
        nome_pessoa = self.combo_pessoa.get()
        id_pessoa = next((id for id, nome in self.pessoas if nome == nome_pessoa), None)
        tipo = self.combo_tipo.get()
        cep = self.entry_cep.get()
        numero = self.entry_numero.get()
        compl = self.entry_compl.get()

        if not id_pessoa or not cep:
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios (Pessoa e CEP).")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alba0002 (id_pessoa, tp_ender, cd_cep, nr_numero, nm_compl)
            VALUES (?, ?, ?, ?, ?)
        """, (id_pessoa, tipo, cep, numero, compl))
        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        id_ender = self.tree.item(item)["values"][0]
        
        resposta = messagebox.askyesno("Confirmar", "Deseja realmente remover este endereço?")
        if not resposta:
            return
            
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alba0002 WHERE id_ender = ?", (id_ender,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id_ender, e.id_pessoa, e.tp_ender, e.cd_cep, e.nr_numero, e.nm_compl, p.nm_razao
            FROM alba0002 e
            LEFT JOIN alba0001 p ON e.id_pessoa = p.id_pessoa
            ORDER BY p.nm_razao
        """)
        for row in cursor.fetchall():
            id_ender, id_pessoa, tipo, cep, numero, compl, nome = row
            self.tree.insert("", "end", values=(id_ender, nome or f"ID {id_pessoa}", tipo, cep, numero, compl))
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        _, pessoa_nome, tipo, cep, numero, compl = item["values"]
        
        self.combo_pessoa.set(pessoa_nome or "")
        
        self.combo_tipo.set(tipo or "")
        
        self.entry_cep.delete(0, tk.END)
        self.entry_cep.insert(0, cep or "")
        
        self.entry_numero.delete(0, tk.END)
        self.entry_numero.insert(0, numero or "")
        
        self.entry_compl.delete(0, tk.END)
        self.entry_compl.insert(0, compl or "")

    def limpar(self):
        self.combo_pessoa.set("")
        self.combo_tipo.set("")
        self.entry_cep.delete(0, tk.END)
        self.entry_numero.delete(0, tk.END)
        self.entry_compl.delete(0, tk.END)
        
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
