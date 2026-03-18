import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class ContatoWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_id = None  # Para controlar inserção/atualização
        aplicar_estilo(self)
        self.set_title("Cadastro de Contatos")
        self.config(width=900, height=600)

        # Frame principal
        main_frame = ttkb.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para barra de ferramentas e mensagens
        top_frame = ttkb.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 15))

        # Barra de ferramentas no topo (lado esquerdo)
        toolbar_frame = ttkb.Frame(top_frame, relief="raised", borderwidth=2, padding=5)
        toolbar_frame.pack(side=tk.LEFT, fill=tk.Y)

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

        # Botão de busca
        search_container = ttkb.Frame(toolbar_frame)
        search_container.pack(side=tk.LEFT, padx=(10, 0))

        btn_buscar = ttkb.Button(search_container, text="🔍", command=self.buscar_contato, width=3)
        btn_buscar.pack(side=tk.LEFT)
        self.create_tooltip(btn_buscar, "Buscar Contato")
        
        btn_recarregar = ttkb.Button(search_container, text="🔄", command=self.carregar_contatos, width=3)
        btn_recarregar.pack(side=tk.LEFT)
        self.create_tooltip(btn_recarregar, "Recarregar Lista")

        # Message panel frame (positioned after toolbar, before input fields)
        message_frame = ttkb.Frame(main_frame)
        message_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

        # Message frame title
        ttkb.Label(message_frame, text="Mensagens:", font=("Arial", 8, "bold")).pack(anchor=tk.W)

        # Message label with consistent styling
        self.message_label = ttkb.Label(
            message_frame, 
            text="Sistema pronto para uso", 
            foreground="blue",
            font=("Arial", 8),
            wraplength=400
        )
        self.message_label.pack(anchor=tk.W, fill=tk.BOTH, expand=True)

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

        # Frame principal dividido em duas partes
        content_frame = ttkb.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para o Treeview de contatos (parte superior)
        tree_frame = ttkb.Frame(content_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "nome", "ddd", "telefone", "celular", "depto", "email"), show="headings", height=10)
        
        # Configuração das colunas
        self.tree.heading("id", text="COD")
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
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        # Frame para painel de visualização das empresas relacionadas
        visualization_frame = ttkb.LabelFrame(content_frame, text="📋 Empresas Relacionadas ao Contato", padding=10)
        visualization_frame.pack(fill=tk.BOTH, expand=False, pady=(10, 0))

        # Treeview para mostrar empresas relacionadas
        self.tree_empresas = ttkb.Treeview(
            visualization_frame, 
            columns=("id_pessoa", "razao_social", "fantasia", "cnpj", "telefone", "email"), 
            show="headings", 
            height=6
        )
        
        # Configuração das colunas do painel de empresas
        self.tree_empresas.heading("id_pessoa", text="COD")
        self.tree_empresas.heading("razao_social", text="Razão Social")
        self.tree_empresas.heading("fantasia", text="Nome Fantasia")
        self.tree_empresas.heading("cnpj", text="CNPJ/CPF")
        self.tree_empresas.heading("telefone", text="Telefone")
        self.tree_empresas.heading("email", text="Email")
        
        # Configuração da largura das colunas
        self.tree_empresas.column("id_pessoa", width=50, minwidth=40, anchor=tk.CENTER)
        self.tree_empresas.column("razao_social", width=200, minwidth=150, anchor=tk.W)
        self.tree_empresas.column("fantasia", width=150, minwidth=100, anchor=tk.W)
        self.tree_empresas.column("cnpj", width=120, minwidth=100, anchor=tk.CENTER)
        self.tree_empresas.column("telefone", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree_empresas.column("email", width=180, minwidth=120, anchor=tk.W)
        
        # Scrollbar para o Treeview de empresas
        scrollbar_empresas = tk.Scrollbar(visualization_frame, orient=tk.VERTICAL, command=self.tree_empresas.yview)
        self.tree_empresas.configure(yscrollcommand=scrollbar_empresas.set)
        
        # Pack do Treeview de empresas e Scrollbar
        self.tree_empresas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_empresas.pack(side=tk.RIGHT, fill=tk.Y)

        self.carregar_contatos()

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            tooltip.configure(bg="lightyellow", relief="solid", borderwidth=1)
            
            label = tk.Label(tooltip, text=text, bg="lightyellow", 
                           font=("Arial", 8), padx=5, pady=2)
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def show_message(self, message, msg_type="info"):
        """Enhanced message display with consistent styling and behavior"""
        colors = {
            "info": "blue",
            "success": "green", 
            "warning": "orange",
            "error": "red"
        }
        
        self.message_label.config(
            text=message,
            foreground=colors.get(msg_type, "blue")
        )
        
        # Auto-clear message after 5 seconds for non-error messages
        if msg_type != "error":
            self.after(5000, lambda: self.message_label.config(
                text="Sistema pronto para uso", 
                foreground="blue"
            ))

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar_campos()
        self.entry_nome.focus()
        self.show_message("Campos limpos. Digite os dados do novo contato.", "info")

    def buscar_contato(self):
        nome_busca = self.entry_nome.get()
        if not nome_busca:
            self.carregar_contatos()
            self.show_message("Busca limpa. Mostrando todos os contatos.", "info")
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
        
        resultados = cursor.fetchall()
        for row in resultados:
            # Formatar celular com DDD
            id_contato, nome, ddd, telefone, celular, depto, email = row
            celular_formatado = f"{row[4] or ''}"  # nr_celular já pode conter DDD
            self.tree.insert("", "end", values=(id_contato, nome, ddd, telefone, celular_formatado, depto, email))
        
        conn.close()
        
        if resultados:
            self.show_message(f"Encontrados {len(resultados)} contato(s) com '{nome_busca}'", "success")
        else:
            self.show_message(f"Nenhum contato encontrado com '{nome_busca}'", "warning")

    def _execute_save(self):
        nome = self.entry_nome.get()
        ddd = self.entry_ddd.get()
        telefone = self.entry_telefone.get()
        ramal = self.entry_ramal.get()
        ddd_cel = self.entry_ddd_cel.get()
        celular = self.entry_celular.get()
        depto = self.entry_depto.get()
        email = self.entry_email.get()

        conn = self.conectar()
        try:
            cursor = conn.cursor()
            
            if self.current_id is None:
                # Novo registro - INSERT
                cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM contatos")
                next_recnum = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO contatos (recnum, nm_contato, nr_ddd_fone, nr_telefone, nr_ramal, nr_ddd_cel, nr_celular, nm_depto, nm_email)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (next_recnum, nome, ddd, telefone, ramal, ddd_cel, celular, depto, email))
            else:
                # Atualização - UPDATE
                cursor.execute("""
                    UPDATE contatos SET
                        nm_contato=?, nr_ddd_fone=?, nr_telefone=?, nr_ramal=?,
                        nr_ddd_cel=?, nr_celular=?, nm_depto=?, nm_email=?
                    WHERE id_contato=?
                """, (nome, ddd, telefone, ramal, ddd_cel, celular, depto, email, self.current_id))

            conn.commit()
            self.limpar_campos()
            self.carregar_contatos()
            self.show_message(f"Contato '{nome}' salvo com sucesso!", "success")
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            if "UNIQUE constraint failed" in str(e):
                self.show_message("ERRO: Já existe um contato com estes dados.", "error")
            else:
                self.show_message(f"ERRO de integridade: {str(e)}", "error")
        except sqlite3.Error as e:
            conn.rollback()
            self.show_message(f"ERRO ao salvar contato: {str(e)}", "error")
        finally:
            conn.close()

    def salvar(self):
        nome = self.entry_nome.get()
        telefone = self.entry_telefone.get()

        if not nome or not telefone:
            self.show_message("ATENÇÃO: Preencha os campos obrigatórios: Nome e Telefone.", "warning")
            return

        confirmation_message = f"Confirma a gravação do contato '{nome}'?"
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('save')

        if not self.request_confirmation('save', confirmation_message, self._execute_save):
            return

    def _execute_removal(self, contato_id, nome_contato):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contatos WHERE id_contato = ?", (contato_id,))
            conn.commit()
            conn.close()
            self.carregar_contatos()
            self.limpar_campos()
            self.show_message(f"Contato '{nome_contato}' removido com sucesso!", "success")
        except sqlite3.Error as e:
            self.show_message(f"ERRO ao remover contato: {str(e)}", "error")

    def remover(self):
        selecionado = self.tree.focus()
        if not selecionado:
            self.show_message("ATENÇÃO: Selecione um contato para remover.", "warning")
            return
        
        item = self.tree.item(selecionado)
        contato_id = item["values"][0]
        nome_contato = item["values"][1]
        
        confirmation_message = f"Pressione 'Remover' novamente para excluir o contato '{nome_contato}'."

        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('remove')

        if not self.request_confirmation('remove', confirmation_message, self._execute_removal, contato_id, nome_contato):
            return

    def carregar_contatos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_contato, nm_contato, nr_ddd_fone, nr_telefone, nr_celular, nm_depto, nm_email 
                FROM contatos 
                ORDER BY nm_contato
            """)
            
            resultados = cursor.fetchall()
            for row in resultados:
                # Formatar celular com DDD
                id_contato, nome, ddd, telefone, celular, depto, email = row
                celular_formatado = f"{celular or ''}"
                self.tree.insert("", "end", values=(id_contato, nome, ddd, telefone, celular_formatado, depto, email))
            
            conn.close()
            self.show_message(f"Carregados {len(resultados)} contatos", "success")
            
        except sqlite3.Error as e:
            self.show_message(f"ERRO ao carregar contatos: {str(e)}", "error")

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        
        contato_id = item["values"][0]
        self.current_id = contato_id  # Armazenar o ID para edição
        nome_selecionado = item["values"][1]
        
        try:
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
                
                self.show_message(f"Contato selecionado: {nome_selecionado}", "info")
                
                # Carregar empresas relacionadas
                self.carregar_empresas_relacionadas(contato_id)
                
        except sqlite3.Error as e:
            self.show_message(f"ERRO ao carregar dados do contato: {str(e)}", "error")

    def carregar_empresas_relacionadas(self, contato_id):
        """Carrega as empresas relacionadas ao contato selecionado"""
        # Limpar o treeview de empresas
        for row in self.tree_empresas.get_children():
            self.tree_empresas.delete(row)
            
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            
            # Buscar empresas que têm este contato associado
            # Assumindo que existe uma tabela de relacionamento ou campo na tabela pessoas
            cursor.execute("""
                SELECT p.id_pessoa, p.nm_razao_social, p.nm_fantasia, p.nr_cnpj_cpf, p.nr_telefone, p.nm_email
                FROM pessoas p
                INNER JOIN contatos c ON p.id_contato = c.id_contato
                WHERE c.id_contato = ?
                ORDER BY p.nm_razao_social
            """, (contato_id,))
            
            resultados = cursor.fetchall()
            
            for row in resultados:
                id_pessoa, razao_social, fantasia, cnpj, telefone, email = row
                self.tree_empresas.insert("", "end", values=(
                    id_pessoa, 
                    razao_social or "", 
                    fantasia or "", 
                    cnpj or "", 
                    telefone or "", 
                    email or ""
                ))
            
            conn.close()
            
            if resultados:
                self.show_message(f"Encontradas {len(resultados)} empresa(s) relacionada(s)", "info")
            else:
                self.show_message("Nenhuma empresa relacionada encontrada", "info")
                
        except sqlite3.Error as e:
            self.show_message(f"ERRO ao carregar empresas relacionadas: {str(e)}", "error")
        for row in self.tree_empresas.get_children():
            self.tree_empresas.delete(row)
            
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            
            # Query para buscar empresas relacionadas através da tabela alba0003
            cursor.execute("""
                SELECT DISTINCT 
                    e.id_pessoa,
                    e.nm_razao,
                    e.nm_fantasia,
                    e.nr_cnpj_cpf,
                    CASE 
                        WHEN e.nr_ddd != '' AND e.nr_telefone != '' 
                        THEN '(' || e.nr_ddd || ') ' || e.nr_telefone
                        ELSE ''
                    END as telefone_formatado,
                    e.nm_email
                FROM alba0003 rel
                INNER JOIN alba0001 e ON rel.id_pessoa = e.id_pessoa
                WHERE rel.id_contato = ?
                ORDER BY e.nm_razao
            """, (contato_id,))
            
            resultados = cursor.fetchall()
            
            for row in resultados:
                id_pessoa, razao, fantasia, cnpj, telefone, email = row
                self.tree_empresas.insert("", "end", values=(
                    id_pessoa, 
                    razao or "", 
                    fantasia or "", 
                    cnpj or "", 
                    telefone or "", 
                    email or ""
                ))
            
            conn.close()
            
            if resultados:
                self.show_message(f"Painel atualizado: {len(resultados)} empresa(s) relacionada(s) ao contato", "success")
            else:
                self.show_message("Painel atualizado: Nenhuma empresa relacionada a este contato", "info")
                
        except sqlite3.Error as e:
            self.show_message(f"ERRO ao carregar empresas relacionadas: {str(e)}", "error")

    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.current_id = None
        self.entry_nome.delete(0, tk.END)
        self.entry_ddd.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_ramal.delete(0, tk.END)
        self.entry_ddd_cel.delete(0, tk.END)
        self.entry_celular.delete(0, tk.END)
        self.entry_depto.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        
        # Limpar também o painel de empresas relacionadas
        for row in self.tree_empresas.get_children():
            self.tree_empresas.delete(row)
        
        # Limpar também o painel de empresas relacionadas
        for row in self.tree_empresas.get_children():
            self.tree_empresas.delete(row)

    # Métodos de navegação
    def ir_primeiro(self):
        try:
            items = self.tree.get_children()
            if items:
                first_item = items[0]
                self.tree.selection_set(first_item)
                self.tree.focus(first_item)
                self.tree.see(first_item)
                self.on_select(None)
        except Exception as e:
            self.show_message(f"Erro ao navegar: {str(e)}", "error")

    def ir_anterior(self):
        try:
            selection = self.tree.selection()
            if not selection:
                self.ir_primeiro()
                return

            current_index = self.tree.index(selection[0])
            if current_index > 0:
                prev_item = self.tree.get_children()[current_index - 1]
                self.tree.selection_set(prev_item)
                self.tree.focus(prev_item)
                self.tree.see(prev_item)
                self.on_select(None)
        except Exception as e:
            self.show_message(f"Erro ao navegar: {str(e)}", "error")

    def ir_proximo(self):
        try:
            selection = self.tree.selection()
            if not selection:
                self.ir_primeiro()
                return

            current_index = self.tree.index(selection[0])
            items = self.tree.get_children()
            if current_index < len(items) - 1:
                next_item = items[current_index + 1]
                self.tree.selection_set(next_item)
                self.tree.focus(next_item)
                self.tree.see(next_item)
                self.on_select(None)
        except Exception as e:
            self.show_message(f"Erro ao navegar: {str(e)}", "error")

    def ir_ultimo(self):
        try:
            items = self.tree.get_children()
            if items:
                last_item = items[-1]
                self.tree.selection_set(last_item)
                self.tree.focus(last_item)
                self.tree.see(last_item)
                self.on_select(None)
        except Exception as e:
            self.show_message(f"Erro inesperado: {str(e)}", "error")
