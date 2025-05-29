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
        self.title("Cadastro Produto Fiscal")
        self.geometry("900x700")
        self.resizable(True, True)

        notebook = ttkb.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frames = {}
        abas = [
            ("Identificação", [
                ("Código Produto", "cd_produto"),
                ("Nome Produto", "nm_produto"),
                ("Descrição", "ds_produto"),
                ("Código Barra", "cd_barra"),
                ("Unidade", "cd_unidade"),
                ("NCM", "cd_ncm"),
                ("CEST", "cd_cest"),
                ("EX TIPI", "cd_ex_tipi"),
                ("Gênero", "cd_genero")
            ]),
            ("Tributação", [
                ("CFOP", "cd_cfop"),
                ("CST ICMS", "cd_cst_icms"),
                ("CST IPI", "cd_cst_ipi"),
                ("CST PIS", "cd_cst_pis"),
                ("CST COFINS", "cd_cst_cofins"),
                ("Alíquota ICMS", "vl_aliq_icms"),
                ("Alíquota IPI", "vl_aliq_ipi"),
                ("Alíquota PIS", "vl_aliq_pis"),
                ("Alíquota COFINS", "vl_aliq_cofins"),
                ("Motivo Desoneração", "cd_motivo_desoneracao"),
                ("Valor ICMS Desonerado", "vl_icms_desonerado")
            ]),
            ("Serviço", [
                ("Serviço", "cd_servico"),
                ("Lista Serviço", "cd_lista_servico"),
                ("Município", "cd_municipio")
            ]),
            ("Enquadramento", [
                ("Enquadramento IPI", "cd_enquadramento_ipi"),
                ("Enquadramento Legal", "cd_enquadramento_legal"),
                ("Situação Tributária", "cd_situacao_tributaria"),
                ("Tipo Item", "cd_tipo_item"),
                ("Benefício Fiscal", "cd_beneficio_fiscal")
            ]),
            ("Códigos Tributação", [
                ("Tributação", "cd_codigo_tributacao"),
                ("Municipal", "cd_codigo_tributacao_municipio"),
                ("Estadual", "cd_codigo_tributacao_estadual"),
                ("Federal", "cd_codigo_tributacao_federal"),
                ("Internacional", "cd_codigo_tributacao_internacional"),
                ("Outros", "cd_codigo_tributacao_outros"),
                ("Simples", "cd_codigo_tributacao_simples"),
                ("Especial", "cd_codigo_tributacao_especial"),
                ("Substituição", "cd_codigo_tributacao_substituicao"),
                ("Isenção", "cd_codigo_tributacao_isenção"),
                ("Redução", "cd_codigo_tributacao_reducao"),
                ("Diferimento", "cd_codigo_tributacao_diferimento"),
                ("Suspensão", "cd_codigo_tributacao_suspensao")
            ])
        ]

        for tab_name, fields in abas:
            frame = ttkb.Frame(notebook)
            self.frames[tab_name] = frame
            notebook.add(frame, text=tab_name)
            for i, (label, var) in enumerate(fields):
                ttkb.Label(frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=3)
                
                # Adicionar lupa ao lado do campo "Nome Produto" e "Código Produto"
                if var == "nm_produto" or var == "cd_produto":
                    search_frame = ttkb.Frame(frame)
                    search_frame.grid(row=i, column=1, padx=5, pady=3, sticky=tk.W+tk.E)
                    entry = ttkb.Entry(search_frame, width=40)
                    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                    
                    # Definir o comando de busca apropriado
                    if var == "nm_produto":
                        search_command = self.buscar_produto_por_nome
                    else:  # cd_produto
                        search_command = self.buscar_produto_por_codigo
                        
                    search_button = ttkb.Button(search_frame, text="🔍", bootstyle=INFO, command=search_command, width=3)
                    search_button.pack(side=tk.RIGHT, padx=(5, 0))
                    setattr(self, f"entry_{var}", entry)
                else:
                    entry = ttkb.Entry(frame, width=40)
                    entry.grid(row=i, column=1, padx=5, pady=3)
                    setattr(self, f"entry_{var}", entry)

        # Botões principais
        frame_botoes = ttkb.Frame(self)
        frame_botoes.pack(fill=tk.X, padx=10, pady=(0, 10))
        ttkb.Button(frame_botoes, text="Salvar", command=self.salvar_dados, bootstyle=SUCCESS).pack(side=tk.RIGHT, padx=5)
        ttkb.Button(frame_botoes, text="Limpar", command=self.limpar_campos, bootstyle=INFO).pack(side=tk.RIGHT, padx=5)
        ttkb.Button(frame_botoes, text="Limpar Filtro", command=self.carregar_dados, bootstyle=INFO).pack(side=tk.LEFT, padx=5)

        # Botões de navegação
        frame_nav = ttkb.Frame(self)
        frame_nav.pack(fill=tk.X, padx=10, pady=(0, 10))
        ttkb.Button(frame_nav, text="⏮ Primeiro", command=self.ir_primeiro, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(frame_nav, text="◀ Anterior", command=self.ir_anterior, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(frame_nav, text="Próximo ▶", command=self.ir_proximo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(frame_nav, text="Último ⏭", command=self.ir_ultimo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)

        # Treeview para exibir produtos
        self.tree = ttkb.Treeview(self, columns=("id", "cd_produto", "nm_produto", "cd_unidade", "cd_ncm" ), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.column("id", width=0, stretch=False)
        self.tree.heading("id", text="")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_dados()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def buscar_produto_por_nome(self):
        nome_busca = self.entry_nm_produto.get()
        if not nome_busca:
            self.carregar_dados()
            return
        
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM alba0005 
            WHERE nm_produto LIKE ?
        """, (f'%{nome_busca}%',))
        
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def buscar_produto_por_codigo(self):
        codigo_busca = self.entry_cd_produto.get()
        if not codigo_busca:
            self.carregar_dados()
            return
        
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM alba0005 
            WHERE cd_produto LIKE ?
        """, (f'%{codigo_busca}%',))
        
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def salvar_dados(self):
        campos = [attr[6:] for attr in dir(self) if attr.startswith("entry_")]
        valores = [getattr(self, f"entry_{c}").get() for c in campos]
        placeholders = ', '.join(['?'] * len(campos))
        sql = f"INSERT INTO alba0005 ({', '.join(campos)}) VALUES ({placeholders})"
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(sql, valores)
        conn.commit()
        conn.close()
        self.limpar_campos()
        self.carregar_dados()

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alba0005")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        id_registro = item["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alba0005 WHERE id_produto = ?", (id_registro,))
        row = cursor.fetchone()
        col_names = [desc[0] for desc in cursor.description]
        conn.close()
        if row:
            for i, col in enumerate(col_names):
                entry = getattr(self, f"entry_{col}", None)
                if entry:
                    entry.delete(0, tk.END)
                    entry.insert(0, row[i])

    def limpar_campos(self):
        for attr in dir(self):
            if attr.startswith("entry_"):
                getattr(self, attr).delete(0, tk.END)


    def ir_primeiro(self):
        items = self.tree.get_children()
        if items:
            self.tree.selection_set(items[0])
            self.tree.focus(items[0])
            self.tree.see(items[0])
            self.on_select(None)

    def ir_ultimo(self):
        items = self.tree.get_children()
        if items:
            self.tree.selection_set(items[-1])
            self.tree.focus(items[-1])
            self.tree.see(items[-1])
            self.on_select(None)

    def ir_anterior(self):
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
