import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class NatopWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Naturezas da Operação (NATOP)")
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
        ttkb.Label(input_frame, text="Descrição").grid(row=0, column=0, sticky=tk.W)
        self.entry_desc = ttkb.Entry(input_frame, width=40)
        self.entry_desc.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="CFOP").grid(row=0, column=2, sticky=tk.W)
        self.entry_cfop = ttkb.Entry(input_frame, width=20)
        self.entry_cfop.grid(row=0, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Fluxo").grid(row=0, column=4, sticky=tk.W)
        self.entry_fluxo = ttkb.Entry(input_frame, width=20)
        self.entry_fluxo.grid(row=0, column=5, pady=5, padx=5)

        # Segunda linha
        ttkb.Label(input_frame, text="Livro Entrada").grid(row=1, column=0, sticky=tk.W)
        self.entry_ent = ttkb.Entry(input_frame, width=15)
        self.entry_ent.grid(row=1, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Livro Saída").grid(row=1, column=2, sticky=tk.W)
        self.entry_sai = ttkb.Entry(input_frame, width=15)
        self.entry_sai.grid(row=1, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Livro Serviço").grid(row=1, column=4, sticky=tk.W)
        self.entry_srv = ttkb.Entry(input_frame, width=15)
        self.entry_srv.grid(row=1, column=5, pady=5, padx=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "desc", "cfop", "fluxo", "ent", "sai", "srv"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("desc", text="Descrição")
        self.tree.heading("cfop", text="CFOP")
        self.tree.heading("fluxo", text="Fluxo")
        self.tree.heading("ent", text="Livro Ent.")
        self.tree.heading("sai", text="Livro Saí.")
        self.tree.heading("srv", text="Livro Srv.")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("desc", width=300, minwidth=200, anchor=tk.W)
        self.tree.column("cfop", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("fluxo", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("ent", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("sai", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("srv", width=80, minwidth=60, anchor=tk.CENTER)
        
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
        cfop = self.entry_cfop.get()
        fluxo = self.entry_fluxo.get()
        ent = self.entry_ent.get()
        sai = self.entry_sai.get()
        srv = self.entry_srv.get()

        if not desc or not cfop:
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios (Descrição e CFOP).")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO natop (ds_natop, cd_cfop, fl_fluxo, fl_livro_ent, fl_livro_sai, fl_livro_srv)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (desc, cfop, fluxo, ent, sai, srv)
        )
        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        id_natop = self.tree.item(item)["values"][0]
        
        resposta = messagebox.askyesno("Confirmar", "Deseja realmente remover este registro?")
        if not resposta:
            return
            
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM natop WHERE id_natop = ?", (id_natop,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_natop, ds_natop, cd_cfop, fl_fluxo, fl_livro_ent, fl_livro_sai, fl_livro_srv FROM natop ORDER BY ds_natop")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        _, desc, cfop, fluxo, ent, sai, srv = item["values"]
        
        self.entry_desc.delete(0, tk.END)
        self.entry_desc.insert(0, desc or "")
        
        self.entry_cfop.delete(0, tk.END)
        self.entry_cfop.insert(0, cfop or "")
        
        self.entry_fluxo.delete(0, tk.END)
        self.entry_fluxo.insert(0, fluxo or "")
        
        self.entry_ent.delete(0, tk.END)
        self.entry_ent.insert(0, ent or "")
        
        self.entry_sai.delete(0, tk.END)
        self.entry_sai.insert(0, sai or "")
        
        self.entry_srv.delete(0, tk.END)
        self.entry_srv.insert(0, srv or "")

    def limpar(self):
        self.entry_desc.delete(0, tk.END)
        self.entry_cfop.delete(0, tk.END)
        self.entry_fluxo.delete(0, tk.END)
        self.entry_ent.delete(0, tk.END)
        self.entry_sai.delete(0, tk.END)
        self.entry_srv.delete(0, tk.END)

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
