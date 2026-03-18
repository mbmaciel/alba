import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class ProdutoFiscalWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Cadastro Produto Fiscal")
        self.config(width=1400, height=800)  # Aumentada a largura de 1200 para 1400

        # Frame principal
        main_frame = ttkb.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Barra de ferramentas no topo
        toolbar_frame = ttkb.Frame(main_frame, relief="raised", borderwidth=2, padding=5)
        toolbar_frame.pack(fill=tk.X, pady=(0, 15))

        # Create standard message panel
        self.ensure_message_panel(main_frame)

        # Container para os botões grudados
        button_container = ttkb.Frame(toolbar_frame)
        button_container.pack(side=tk.LEFT)

        # Botões da barra de ferramentas com ícones
        self.btn_novo = ttkb.Button(button_container, text="➕", command=self.novo, width=3)
        self.btn_novo.pack(side=tk.LEFT)
        self.create_tooltip(self.btn_novo, "Novo")

        self.btn_salvar = ttkb.Button(button_container, text="💾", command=self.salvar, width=3)
        self.btn_salvar.pack(side=tk.LEFT)
        self.create_tooltip(self.btn_salvar, "Salvar")

        self.btn_remover = ttkb.Button(button_container, text="🗑️", command=self.remover, width=3)
        self.btn_remover.pack(side=tk.LEFT)
        self.create_tooltip(self.btn_remover, "Remover")

        # Separador visual
        separator = ttkb.Separator(toolbar_frame, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

        # Botões de navegação
        nav_container = ttkb.Frame(toolbar_frame)
        nav_container.pack(side=tk.LEFT, padx=(10, 0))

        btn_primeiro = ttkb.Button(nav_container, text="⏮", command=self.ir_primeiro, width=3)
        btn_primeiro.pack(side=tk.LEFT)
        self.create_tooltip(btn_primeiro, "Primeiro")
        
        btn_anterior = ttkb.Button(nav_container, text="◀", command=self.ir_anterior, width=3)
        btn_anterior.pack(side=tk.LEFT)
        self.create_tooltip(btn_anterior, "Anterior")
        
        btn_proximo = ttkb.Button(nav_container, text="▶", command=self.ir_proximo, width=3)
        btn_proximo.pack(side=tk.LEFT)
        self.create_tooltip(btn_proximo, "Próximo")
        
        btn_ultimo = ttkb.Button(nav_container, text="⏭", command=self.ir_ultimo, width=3)
        btn_ultimo.pack(side=tk.LEFT)
        self.create_tooltip(btn_ultimo, "Último")

        # Separador visual
        separator2 = ttkb.Separator(toolbar_frame, orient=tk.VERTICAL)
        separator2.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

        # Botões de busca
        search_container = ttkb.Frame(toolbar_frame)
        search_container.pack(side=tk.LEFT, padx=(10, 0))

        btn_buscar = ttkb.Button(search_container, text="🔍", command=self.buscar_produto_por_nome, width=3)
        btn_buscar.pack(side=tk.LEFT)
        self.create_tooltip(btn_buscar, "Buscar Produto")
        
        btn_atualizar = ttkb.Button(search_container, text="🔄", command=self.carregar_dados, width=3)
        btn_atualizar.pack(side=tk.LEFT)
        self.create_tooltip(btn_atualizar, "Atualizar Lista")

        # Notebook para as abas
        notebook = ttkb.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

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
            ])
        ]

        # Processar abas normais
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
                    
                    # Adicionar tooltip
                    if var == "nm_produto":
                        self.create_tooltip(search_button, "Buscar por Nome")
                    else:  # cd_produto
                        self.create_tooltip(search_button, "Buscar por Código")
                    setattr(self, f"entry_{var}", entry)
                else:
                    entry = ttkb.Entry(frame, width=40)
                    entry.grid(row=i, column=1, padx=5, pady=3)
                    setattr(self, f"entry_{var}", entry)

        # Aba especial "Tributação" com layout em colunas
        tributacao_frame = ttkb.Frame(notebook)
        self.frames["Tributação"] = tributacao_frame
        notebook.add(tributacao_frame, text="Tributação")

        # Campos da aba Tributação organizados em 3 colunas
        tributacao_fields = [
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
        ]

        # Organizar em 3 colunas
        num_cols = 3
        col_width = 25  # Largura dos campos de entrada

        for i, (label, var) in enumerate(tributacao_fields):
            row = i % ((len(tributacao_fields) + num_cols - 1) // num_cols)  # Calcular linha
            col_group = i // ((len(tributacao_fields) + num_cols - 1) // num_cols)  # Calcular grupo de coluna
            
            # Posições das colunas: 0,1 | 2,3 | 4,5
            label_col = col_group * 2
            entry_col = col_group * 2 + 1
            
            # Label
            ttkb.Label(tributacao_frame, text=label).grid(
                row=row, 
                column=label_col, 
                sticky=tk.W, 
                padx=(5, 2), 
                pady=3
            )
            
            # Entry
            entry = ttkb.Entry(tributacao_frame, width=col_width)
            entry.grid(
                row=row, 
                column=entry_col, 
                padx=(2, 15), 
                pady=3,
                sticky=tk.W
            )
            setattr(self, f"entry_{var}", entry)

        # Configurar peso das colunas para distribuição uniforme
        for col in range(6):  # 3 grupos x 2 colunas cada
            tributacao_frame.columnconfigure(col, weight=1 if col % 2 == 1 else 0)

        # Aba especial "Códigos Tributação" com layout em colunas
        codigos_frame = ttkb.Frame(notebook)
        self.frames["Códigos Tributação"] = codigos_frame
        notebook.add(codigos_frame, text="Códigos Tributação")

        # Campos da aba Códigos Tributação organizados em 3 colunas
        codigos_fields = [
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
        ]

        # Organizar em 3 colunas
        num_cols = 3
        col_width = 25  # Largura dos campos de entrada

        for i, (label, var) in enumerate(codigos_fields):
            row = i % ((len(codigos_fields) + num_cols - 1) // num_cols)  # Calcular linha
            col_group = i // ((len(codigos_fields) + num_cols - 1) // num_cols)  # Calcular grupo de coluna
            
            # Posições das colunas: 0,1 | 2,3 | 4,5
            label_col = col_group * 2
            entry_col = col_group * 2 + 1
            
            # Label
            ttkb.Label(codigos_frame, text=label).grid(
                row=row, 
                column=label_col, 
                sticky=tk.W, 
                padx=(5, 2), 
                pady=3
            )
            
            # Entry
            entry = ttkb.Entry(codigos_frame, width=col_width)
            entry.grid(
                row=row, 
                column=entry_col, 
                padx=(2, 15), 
                pady=3,
                sticky=tk.W
            )
            setattr(self, f"entry_{var}", entry)

        # Configurar peso das colunas para distribuição uniforme
        for col in range(6):  # 3 grupos x 2 colunas cada
            codigos_frame.columnconfigure(col, weight=1 if col % 2 == 1 else 0)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview para exibir produtos
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "nm_produto", "cd_produto", "cd_unidade", "cd_ncm"), show="headings", height=12)
        
        # Configuração das colunas
        self.tree.heading("id", text="COD")
        self.tree.heading("nm_produto", text="Nome Produto")
        self.tree.heading("cd_produto", text="Código")
        self.tree.heading("cd_unidade", text="Unidade")
        self.tree.heading("cd_ncm", text="NCM")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("nm_produto", width=300, minwidth=200, anchor=tk.W)
        self.tree.column("cd_produto", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column("cd_unidade", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("cd_ncm", width=100, minwidth=80, anchor=tk.CENTER)
        
        # Scrollbar para o Treeview
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_dados()
        self.ir_primeiro()

    def create_tooltip(self, widget, text):
        """Cria um tooltip para o widget especificado"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            
            label = tk.Label(tooltip, text=text, background="lightyellow", 
                           relief="solid", borderwidth=1, font=("Arial", 8))
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar_campos()
        self.entry_cd_produto.focus()

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
            SELECT id_produto, nm_produto, cd_produto, cd_unidade, cd_ncm FROM alba0005 
            WHERE nm_produto LIKE ?
            ORDER BY nm_produto
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
            SELECT id_produto, nm_produto, cd_produto, cd_unidade, cd_ncm FROM alba0005 
            WHERE cd_produto LIKE ?
            ORDER BY nm_produto
        """, (f'%{codigo_busca}%',))
        
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def _execute_save(self):
        campos = [attr[6:] for attr in dir(self) if attr.startswith("entry_")]
        valores = [getattr(self, f"entry_{c}").get() for c in campos]
        placeholders = ', '.join(['?'] * len(campos))
        sql = f"INSERT INTO alba0005 ({', '.join(campos)}) VALUES ({placeholders})"
        
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()
            self.limpar_campos()
            self.carregar_dados()
            self.show_message("Produto fiscal salvo com sucesso!", "success")
        except Exception as e:
            self.show_message(f"Erro ao salvar produto: {str(e)}", "error")

    def salvar(self):
        # Verificar se os campos obrigatórios estão preenchidos
        if not self.entry_cd_produto.get() or not self.entry_nm_produto.get():
            self.show_message("Preencha os campos obrigatórios (Código e Nome do Produto).", "warning")
            return

        confirmation_message = f"Confirma a gravação do produto '{self.entry_nm_produto.get()}'?"
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('save')

        if not self.request_confirmation('save', confirmation_message, self._execute_save):
            return

    def _execute_removal(self, id_produto, nome_produto):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alba0005 WHERE id_produto = ?", (id_produto,))
            conn.commit()
            conn.close()
            self.carregar_dados()
            self.limpar_campos()
            self.show_message(f"Produto '{nome_produto}' removido com sucesso!", "success")
        except Exception as e:
            self.show_message(f"Erro ao remover produto: {str(e)}", "error")

    def remover(self):
        item = self.tree.focus()
        if not item:
            self.show_message("Selecione um produto para remover.", "warning")
            return

        id_produto = self.tree.item(item)["values"][0]
        nome_produto = self.tree.item(item)["values"][1]

        confirmation_message = f"Pressione 'Remover' novamente para excluir o produto '{nome_produto}'."

        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('remove')

        if not self.request_confirmation('remove', confirmation_message, self._execute_removal, id_produto, nome_produto):
            return

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_produto, nm_produto, cd_produto, cd_unidade, cd_ncm FROM alba0005 ORDER BY nm_produto")
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
            column_map = {
                "TX_PRODUTO": "ds_produto",
            }
            for i, col in enumerate(col_names):
                entry_name = column_map.get(col, col).lower()
                entry = getattr(self, f"entry_{entry_name}", None)
                if entry:
                    entry.delete(0, tk.END)
                    entry.insert(0, row[i] if row[i] is not None else "")

    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        campos = [attr[6:] for attr in dir(self) if attr.startswith("entry_")]
        for campo in campos:
            entry = getattr(self, f"entry_{campo}", None)
            if entry:
                entry.delete(0, tk.END)

    def ir_primeiro(self):
        """Navega para o primeiro registro"""
        children = self.tree.get_children()
        if children:
            first_item = children[0]
            self.tree.selection_set(first_item)
            self.tree.focus(first_item)
            self.tree.see(first_item)
            self.on_select(None)

    def ir_ultimo(self):
        """Navega para o último registro"""
        children = self.tree.get_children()
        if children:
            last_item = children[-1]
            self.tree.selection_set(last_item)
            self.tree.focus(last_item)
            self.tree.see(last_item)
            self.on_select(None)

    def ir_anterior(self):
        """Navega para o registro anterior"""
        selection = self.tree.selection()
        if not selection:
            self.ir_ultimo()
            return

        current = selection[0]
        prev_item = self.tree.prev(current)
        if prev_item:
            self.tree.selection_set(prev_item)
            self.tree.focus(prev_item)
            self.tree.see(prev_item)
            self.on_select(None)
        else:
            self.ir_ultimo()

    def ir_proximo(self):
        """Navega para o próximo registro"""
        selection = self.tree.selection()
        if not selection:
            self.ir_primeiro()
            return

        current = selection[0]
        next_item = self.tree.next(current)
        if next_item:
            self.tree.selection_set(next_item)
            self.tree.focus(next_item)
            self.tree.see(next_item)
            self.on_select(None)
        else:
            self.ir_primeiro()
