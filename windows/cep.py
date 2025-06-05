import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class CepWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Consulta de CEPs")
        self.geometry("800x500")
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

        ttkb.Button(search_container, text="🔍", command=self.buscar_cep, width=3).pack(side=tk.LEFT)

        # Frame para campos de entrada
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        # Primeira linha
        ttkb.Label(input_frame, text="CEP").grid(row=0, column=0, sticky=tk.W)
        self.entry_cep = ttkb.Entry(input_frame, width=12)
        self.entry_cep.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Cidade").grid(row=0, column=2, sticky=tk.W)
        self.entry_cidade = ttkb.Entry(input_frame, width=30)
        self.entry_cidade.grid(row=0, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="UF").grid(row=0, column=4, sticky=tk.W)
        self.entry_uf = ttkb.Entry(input_frame, width=5)
        self.entry_uf.grid(row=0, column=5, pady=5, padx=5)

        # Segunda linha
        ttkb.Label(input_frame, text="Bairro").grid(row=1, column=0, sticky=tk.W)
        self.entry_bairro = ttkb.Entry(input_frame, width=30)
        self.entry_bairro.grid(row=1, column=1, columnspan=2, pady=5, padx=(5, 20), sticky=tk.W)

        ttkb.Label(input_frame, text="Logradouro").grid(row=1, column=3, sticky=tk.W)
        self.entry_endereco = ttkb.Entry(input_frame, width=40)
        self.entry_endereco.grid(row=1, column=4, columnspan=2, pady=5, padx=(5, 0), sticky=tk.W+tk.E)

        # Frame para busca
        search_frame = ttkb.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 15))

        ttkb.Label(search_frame, text="Buscar por CEP").grid(row=0, column=0, sticky=tk.W)
        self.entry_busca = ttkb.Entry(search_frame, width=20)
        self.entry_busca.grid(row=0, column=1, pady=5, padx=(5, 10))
        self.entry_busca.bind("<Return>", lambda e: self.buscar_cep())

        # Label de informação sobre limite
        self.label_info = ttkb.Label(search_frame, text="Mostrando primeiros 100 registros. Use a busca para filtrar.", 
                                    foreground="gray")
        self.label_info.grid(row=0, column=2, pady=5, padx=(20, 0))

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("cep", "cidade", "uf", "bairro", "endereco"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("cep", text="CEP")
        self.tree.heading("cidade", text="Cidade")
        self.tree.heading("uf", text="UF")
        self.tree.heading("bairro", text="Bairro")
        self.tree.heading("endereco", text="Logradouro")
        
        self.tree.column("cep", width=80, minwidth=70, anchor=tk.CENTER)
        self.tree.column("cidade", width=150, minwidth=120, anchor=tk.W)
        self.tree.column("uf", width=50, minwidth=40, anchor=tk.CENTER)
        self.tree.column("bairro", width=150, minwidth=120, anchor=tk.W)
        self.tree.column("endereco", width=300, minwidth=200, anchor=tk.W)
        
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
        self.entry_cep.focus()

    def salvar(self):
        cep = self.entry_cep.get()
        cidade = self.entry_cidade.get()
        uf = self.entry_uf.get()
        bairro = self.entry_bairro.get()
        endereco = self.entry_endereco.get()

        if not cep or not cidade:
            messagebox.showwarning("Aviso", "Preencha ao menos CEP e Cidade.")
            return

        conn = self.conectar()
        cursor = conn.cursor()

        # Verifica se já existe
        cursor.execute("SELECT COUNT(*) FROM cep WHERE cd_cep = ?", (cep,))
        existe = cursor.fetchone()[0]

        if existe:
            cursor.execute("""
                UPDATE cep SET nm_cidade = ?, cd_uf = ?, nm_bairro = ?, nm_lograd = ? 
                WHERE cd_cep = ?
            """, (cidade, uf, bairro, endereco, cep))
        else:
            cursor.execute("""
                INSERT INTO cep (cd_cep, nm_cidade, cd_uf, nm_bairro, nm_lograd) 
                VALUES (?, ?, ?, ?, ?)
            """, (cep, cidade, uf, bairro, endereco))

        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        cep = self.tree.item(item)["values"][0]
        
        resposta = messagebox.askyesno("Confirmar", f"Deseja realmente remover o CEP {cep}?")
        if not resposta:
            return
            
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cep WHERE cd_cep = ?", (cep,))
        conn.commit()
        conn.close()
        self.carregar()

    def buscar_cep(self):
        cep_valor = self.entry_busca.get()
        if not cep_valor:
            self.carregar()
            return
            
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cd_cep, nm_cidade, cd_uf, nm_bairro, nm_lograd 
            FROM cep 
            WHERE cd_cep LIKE ? OR nm_cidade LIKE ? OR nm_bairro LIKE ? OR nm_lograd LIKE ?
            ORDER BY cd_cep
            LIMIT 100
        """, (f"%{cep_valor}%", f"%{cep_valor}%", f"%{cep_valor}%", f"%{cep_valor}%"))
        resultados = cursor.fetchall()
        conn.close()

        self.tree.delete(*self.tree.get_children())
        for row in resultados:
            self.tree.insert("", "end", values=row)
            
        # Atualizar label de informação
        if len(resultados) == 100:
            self.label_info.config(text=f"Mostrando primeiros 100 resultados para '{cep_valor}'. Refine a busca.")
        else:
            self.label_info.config(text=f"Encontrados {len(resultados)} resultados para '{cep_valor}'.")

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT cd_cep, nm_cidade, cd_uf, nm_bairro, nm_lograd FROM cep ORDER BY cd_cep LIMIT 100")
        rows = cursor.fetchall()
        conn.close()
        
        for row in rows:
            self.tree.insert("", "end", values=row)
            
        # Atualizar label de informação
        self.label_info.config(text="Mostrando primeiros 100 registros. Use a busca para filtrar.")

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        cep, cidade, uf, bairro, endereco = item["values"]
        
        self.entry_cep.delete(0, tk.END)
        self.entry_cep.insert(0, cep or "")
        
        self.entry_cidade.delete(0, tk.END)
        self.entry_cidade.insert(0, cidade or "")
        
        self.entry_uf.delete(0, tk.END)
        self.entry_uf.insert(0, uf or "")
        
        self.entry_bairro.delete(0, tk.END)
        self.entry_bairro.insert(0, bairro or "")
        
        self.entry_endereco.delete(0, tk.END)
        self.entry_endereco.insert(0, endereco or "")

    def limpar(self):
        self.entry_cep.delete(0, tk.END)
        self.entry_cidade.delete(0, tk.END)
        self.entry_uf.delete(0, tk.END)
        self.entry_bairro.delete(0, tk.END)
        self.entry_endereco.delete(0, tk.END)
        self.entry_busca.delete(0, tk.END)
        
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
