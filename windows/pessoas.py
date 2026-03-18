import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class PessoaWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_id = None
        self.current_recnum = None
        aplicar_estilo(self)
        self.set_title("Cadastro de Clientes (alba0001)")
        self.config(width=1100, height=700)

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

        # Botão para buscar pessoa
        search_container = ttkb.Frame(toolbar_frame)
        search_container.pack(side=tk.LEFT, padx=(10, 0))

        btn_buscar_pessoa = ttkb.Button(search_container, text="👤", command=self.buscar_pessoa, width=3)
        btn_buscar_pessoa.pack(side=tk.LEFT)
        self.create_tooltip(btn_buscar_pessoa, "Buscar Cliente")

        # Separador visual
        separator2 = ttkb.Separator(toolbar_frame, orient=tk.VERTICAL)
        separator2.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

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
        ttkb.Label(input_frame, text="Tipo (F/J)").grid(row=0, column=0, sticky=tk.W)
        self.tipo_pessoa_labels = {"F": "Física", "J": "Jurídica"}
        self.tipo_pessoa_by_label = {label: key for key, label in self.tipo_pessoa_labels.items()}
        self.combo_tipo_pessoa = ttkb.Combobox(
            input_frame,
            width=10,
            state="readonly",
            values=list(self.tipo_pessoa_labels.values())
        )
        self.combo_tipo_pessoa.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="CNPJ/CPF").grid(row=0, column=2, sticky=tk.W)
        self.entry_doc = ttkb.Entry(input_frame, width=20)
        self.entry_doc.grid(row=0, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="IE/RG").grid(row=0, column=4, sticky=tk.W)
        self.entry_ie_rg = ttkb.Entry(input_frame, width=20)
        self.entry_ie_rg.grid(row=0, column=5, pady=5, padx=5)

        # Segunda linha
        ttkb.Label(input_frame, text="Razão Social / Nome").grid(row=1, column=0, sticky=tk.W)
        self.entry_razao = ttkb.Entry(input_frame, width=50)
        self.entry_razao.grid(row=1, column=1, columnspan=3, pady=5, padx=(5, 20), sticky=tk.W+tk.E)

        ttkb.Label(input_frame, text="IM").grid(row=1, column=4, sticky=tk.W)
        self.entry_im = ttkb.Entry(input_frame, width=20)
        self.entry_im.grid(row=1, column=5, pady=5, padx=5)

        # Terceira linha
        ttkb.Label(input_frame, text="Nome Fantasia").grid(row=2, column=0, sticky=tk.W)
        self.entry_fantasia = ttkb.Entry(input_frame, width=50)
        self.entry_fantasia.grid(row=2, column=1, columnspan=3, pady=5, padx=(5, 20), sticky=tk.W+tk.E)

        # Campo 'Cód. Unitron' removido

        # Quarta linha - Telefones
        ttkb.Label(input_frame, text="DDD").grid(row=3, column=0, sticky=tk.W)
        self.entry_ddd = ttkb.Entry(input_frame, width=5)
        self.entry_ddd.grid(row=3, column=1, pady=5, padx=(5, 5), sticky=tk.W)

        ttkb.Label(input_frame, text="Telefone").grid(row=3, column=2, sticky=tk.W)
        self.entry_tel = ttkb.Entry(input_frame, width=15)
        self.entry_tel.grid(row=3, column=3, pady=5, padx=(5, 20), sticky=tk.W)

        ttkb.Label(input_frame, text="DDD2").grid(row=3, column=4, sticky=tk.W)
        self.entry_ddd2 = ttkb.Entry(input_frame, width=5)
        self.entry_ddd2.grid(row=3, column=5, pady=5, padx=5, sticky=tk.W)

        # Quinta linha - Telefones continuação
        ttkb.Label(input_frame, text="Telefone 2").grid(row=4, column=0, sticky=tk.W)
        self.entry_tel2 = ttkb.Entry(input_frame, width=15)
        self.entry_tel2.grid(row=4, column=1, pady=5, padx=(5, 20), sticky=tk.W)

        ttkb.Label(input_frame, text="DDD Cel").grid(row=4, column=2, sticky=tk.W)
        self.entry_ddd_cel = ttkb.Entry(input_frame, width=5)
        self.entry_ddd_cel.grid(row=4, column=3, pady=5, padx=(5, 5), sticky=tk.W)

        ttkb.Label(input_frame, text="Celular").grid(row=4, column=4, sticky=tk.W)
        self.entry_celular = ttkb.Entry(input_frame, width=15)
        self.entry_celular.grid(row=4, column=5, pady=5, padx=5, sticky=tk.W)

        # Sexta linha - Email e Site
        ttkb.Label(input_frame, text="Email").grid(row=5, column=0, sticky=tk.W)
        self.entry_email = ttkb.Entry(input_frame, width=30)
        self.entry_email.grid(row=5, column=1, columnspan=2, pady=5, padx=(5, 20), sticky=tk.W+tk.E)

        ttkb.Label(input_frame, text="Site").grid(row=5, column=3, sticky=tk.W)
        self.entry_site = ttkb.Entry(input_frame, width=30)
        self.entry_site.grid(row=5, column=4, columnspan=2, pady=5, padx=5, sticky=tk.W+tk.E)

        # Sétima linha - Combos
        ttkb.Label(input_frame, text="Tipo de Cliente").grid(row=6, column=0, sticky=tk.W)
        self.combo_tipo = ttkb.Combobox(input_frame, width=25, state="readonly")
        self.combo_tipo.grid(row=6, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Atividade").grid(row=6, column=2, sticky=tk.W)
        self.combo_atividade = ttkb.Combobox(input_frame, width=25, state="readonly")
        self.combo_atividade.grid(row=6, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Transportadora").grid(row=6, column=4, sticky=tk.W)
        self.combo_transp = ttkb.Combobox(input_frame, width=25, state="readonly")
        self.combo_transp.grid(row=6, column=5, pady=5, padx=5)

        # Oitava linha - Checkboxes
        checkbox_frame = ttkb.Frame(input_frame)
        checkbox_frame.grid(row=7, column=0, columnspan=6, pady=10, sticky=tk.W)

        self.var_cliente = tk.IntVar()
        self.var_fornec = tk.IntVar()
        self.var_transp = tk.IntVar()
        self.var_ativo = tk.IntVar()

        ttkb.Checkbutton(checkbox_frame, text="Cliente", variable=self.var_cliente).pack(side=tk.LEFT, padx=(0, 20))
        ttkb.Checkbutton(checkbox_frame, text="Fornecedor", variable=self.var_fornec).pack(side=tk.LEFT, padx=(0, 20))
        ttkb.Checkbutton(checkbox_frame, text="Transportadora", variable=self.var_transp).pack(side=tk.LEFT, padx=(0, 20))
        ttkb.Checkbutton(checkbox_frame, text="Ativo", variable=self.var_ativo).pack(side=tk.LEFT)

        # Nona linha - Observações
        ttkb.Label(input_frame, text="Observações").grid(row=8, column=0, sticky=tk.NW)
        self.text_obs = tk.Text(input_frame, width=80, height=3, wrap=tk.WORD)
        self.text_obs.grid(row=8, column=1, columnspan=5, pady=5, padx=(5, 0), sticky=tk.W+tk.E)
        
        # Scrollbar para observações
        scrollbar_obs = tk.Scrollbar(input_frame, orient=tk.VERTICAL, command=self.text_obs.yview)
        self.text_obs.configure(yscrollcommand=scrollbar_obs.set)
        scrollbar_obs.grid(row=8, column=6, sticky=tk.NS, pady=5)

        # Configurar expansão das colunas
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)

        # Frame para o Treeview (área expandida) - Endereços da pessoa selecionada
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Label para indicar que são endereços
        self.endereco_label = ttkb.Label(tree_frame, text="Endereços do Cliente Selecionado:", font=("Arial", 10, "bold"))
        self.endereco_label.pack(anchor=tk.W, pady=(0, 5))

        # Treeview com colunas para endereços
        self.tree = ttkb.Treeview(tree_frame, columns=("id_ender", "tp_ender", "cep", "numero", "complemento", "cidade", "uf", "bairro", "logradouro"), show="headings", height=15)
        
        # Configuração das colunas para endereços
        self.tree.heading("id_ender", text="COD")
        self.tree.heading("tp_ender", text="Tipo")
        self.tree.heading("cep", text="CEP")
        self.tree.heading("numero", text="Número")
        self.tree.heading("complemento", text="Complemento")
        self.tree.heading("cidade", text="Cidade")
        self.tree.heading("uf", text="UF")
        self.tree.heading("bairro", text="Bairro")
        self.tree.heading("logradouro", text="Logradouro")
        
        # Make ID column visible
        self.tree.column("id_ender", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("tp_ender", width=60, minwidth=50, anchor=tk.CENTER)
        self.tree.column("cep", width=80, minwidth=70, anchor=tk.CENTER)
        self.tree.column("numero", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("complemento", width=120, minwidth=100, anchor=tk.W)
        self.tree.column("cidade", width=120, minwidth=100, anchor=tk.W)
        self.tree.column("uf", width=50, minwidth=40, anchor=tk.CENTER)
        self.tree.column("bairro", width=120, minwidth=100, anchor=tk.W)
        self.tree.column("logradouro", width=200, minwidth=150, anchor=tk.W)
        
        # Scrollbar para o Treeview
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        # Lista de pessoas para navegação
        self.pessoas_list = []
        self.current_pessoa_index = -1
        
        self.carregar_tipos()
        self.carregar_atividades()
        self.carregar_transportadoras()
        self.carregar_pessoas_list()
        self.carregar()

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
            "error": "red",
            "danger": "red"
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

    def _get_tipo_pessoa(self):
        raw_value = self.combo_tipo_pessoa.get().strip()
        if not raw_value:
            return ""
        mapped = self.tipo_pessoa_by_label.get(raw_value, raw_value)
        return mapped.upper().strip()

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar()
        self.current_pessoa_index = -1  # Reset navigation index
        self.combo_tipo_pessoa.focus()
        self.show_message("Campos limpos. Preencha os dados da nova pessoa.", "info")

    def carregar_tipos(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_tipo, nm_tipo FROM tipo ORDER BY nm_tipo")
            self.tipos = cursor.fetchall()
            conn.close()
            self.combo_tipo["values"] = [nome for _, nome in self.tipos]
        except Exception as e:
            self.show_message(f"ERRO ao carregar tipos: {str(e)}", "error")

    def carregar_atividades(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_atividade, nm_atividade FROM ativid ORDER BY nm_atividade")
            self.atividades = cursor.fetchall()
            conn.close()
            self.combo_atividade["values"] = [nome for _, nome in self.atividades]
        except Exception as e:
            self.show_message(f"ERRO ao carregar atividades: {str(e)}", "error")

    def carregar_transportadoras(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_pessoa, nm_razao FROM alba0001
                WHERE fl_transp = 'S' OR fl_transp = '1'
                ORDER BY nm_razao
            """)
            self.transportadoras = cursor.fetchall()
            conn.close()
            self.combo_transp["values"] = [nome for _, nome in self.transportadoras]
        except Exception as e:
            self.show_message(f"ERRO ao carregar transportadoras: {str(e)}", "error")

    def carregar_pessoas_list(self):
        """Carrega lista de pessoas para navegação"""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_pessoa, nm_razao FROM alba0001
                ORDER BY CAST(id_pessoa AS INTEGER)
            """)
            self.pessoas_list = cursor.fetchall()
            conn.close()
        except Exception as e:
            self.show_message(f"ERRO ao carregar lista de pessoas: {str(e)}", "error")
            self.pessoas_list = []

    def buscar_pessoa(self):
        """Abre janela para buscar e selecionar uma pessoa"""
        if not self.pessoas_list:
            self.show_message("Nenhuma pessoa cadastrada", "warning")
            return
            
        # Criar janela de busca
        search_window = tk.Toplevel(self)
        search_window.title("Buscar Cliente")
        search_window.geometry("600x400")
        search_window.transient(self)
        search_window.grab_set()
        
        # Frame principal
        main_frame = ttkb.Frame(search_window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campo de busca
        ttkb.Label(main_frame, text="Digite o nome da pessoa:").pack(anchor=tk.W)
        search_entry = ttkb.Entry(main_frame, width=50)
        search_entry.pack(fill=tk.X, pady=(5, 10))
        
        # Lista de pessoas
        listbox_frame = ttkb.Frame(main_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        listbox = tk.Listbox(listbox_frame)
        scrollbar_list = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar_list.set)
        
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_list.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Preencher lista inicial
        for id_pessoa, nome in self.pessoas_list:
            listbox.insert(tk.END, f"{id_pessoa} - {nome}")
        
        def filtrar_pessoas():
            termo = search_entry.get().lower()
            listbox.delete(0, tk.END)
            for id_pessoa, nome in self.pessoas_list:
                if termo in nome.lower():
                    listbox.insert(tk.END, f"{id_pessoa} - {nome}")
        
        def selecionar_pessoa():
            selection = listbox.curselection()
            if selection:
                texto = listbox.get(selection[0])
                id_pessoa = int(texto.split(" - ")[0])
                
                # Encontrar índice na lista
                for i, (pid, _) in enumerate(self.pessoas_list):
                    if pid == id_pessoa:
                        self.current_pessoa_index = i
                        break
                
                self.selecionar_pessoa_por_id(id_pessoa)
                search_window.destroy()
        
        search_entry.bind("<KeyRelease>", lambda e: filtrar_pessoas())
        listbox.bind("<Double-Button-1>", lambda e: selecionar_pessoa())
        
        # Botões
        button_frame = ttkb.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttkb.Button(button_frame, text="Selecionar", command=selecionar_pessoa).pack(side=tk.LEFT, padx=(0, 5))
        ttkb.Button(button_frame, text="Cancelar", command=search_window.destroy).pack(side=tk.LEFT)
        
        search_entry.focus()

    def _execute_save(self):
        # Coletar dados dos campos
        tipo = self._get_tipo_pessoa()
        razao = self.entry_razao.get().strip()
        fantasia = self.entry_fantasia.get().strip()
        cnpj = self.entry_doc.get().strip()
        ie_rg = self.entry_ie_rg.get().strip()
        im = self.entry_im.get().strip()
        ddd = self.entry_ddd.get().strip()
        telefone = self.entry_tel.get().strip()
        ddd2 = self.entry_ddd2.get().strip()
        telefone2 = self.entry_tel2.get().strip()
        ddd_cel = self.entry_ddd_cel.get().strip()
        celular = self.entry_celular.get().strip()
        email = self.entry_email.get().strip()
        site = self.entry_site.get().strip()
        unitron = None  # Campo removido
        obs = self.text_obs.get("1.0", tk.END).strip()

        fl_cliente = '1' if self.var_cliente.get() else '0'
        fl_fornec = '1' if self.var_fornec.get() else '0'
        fl_transp = '1' if self.var_transp.get() else '0'
        fl_ativo = '1' if self.var_ativo.get() else '0'

        nome_tipo = self.combo_tipo.get().strip()
        id_tipo = next((id for id, nome in self.tipos if nome == nome_tipo), None) if nome_tipo else None

        nome_atividade = self.combo_atividade.get().strip()
        id_atividade = next((id for id, nome in self.atividades if nome == nome_atividade), None) if nome_atividade else None

        nome_transp = self.combo_transp.get().strip()
        id_transp = next((id for id, nome in self.transportadoras if nome == nome_transp), None) if nome_transp else None

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            is_update = self.current_id is not None

            if is_update:
                # Atualizar registro existente - preserva recnum existente
                sql = """UPDATE alba0001 SET
                         tp_pessoa = ?, nm_razao = ?, nm_fantasia = ?, nr_cnpj_cpf = ?,
                         nr_ie_rg = ?, nr_im = ?, nr_ddd = ?, nr_telefone = ?,
                         nr_ddd2 = ?, nr_telefone2 = ?, nr_ddd_cel = ?, nr_celular = ?,
                         nm_email = ?, nm_site = ?, tx_obs = ?,
                         fl_cliente = ?, fl_fornec = ?, fl_transp = ?, fl_ativo = ?,
                         id_tipo = ?, id_atividade = ?, id_transp = ?
                         WHERE id_pessoa = ?"""

                cursor.execute(sql, (
                    tipo, razao, fantasia or '', cnpj or '', ie_rg or '', im or '',
                    ddd or '', telefone or '', ddd2 or '', telefone2 or '',
                    ddd_cel or '', celular or '', email or '', site or '',
                    obs or '',
                    fl_cliente, fl_fornec, fl_transp, fl_ativo,
                    id_tipo or 0, id_atividade or 0, id_transp or 0, self.current_id
                ))

                self.show_message(f"Cliente '{razao}' atualizado com sucesso!", "success")

            else:
                # Inserir novo registro - usar utility method para recnum
                next_recnum = self.get_next_recnum("alba0001")
                if next_recnum is None:
                    self.show_message("ERRO: Não foi possível obter próximo recnum", "error")
                    return

                cursor.execute("SELECT COALESCE(MAX(id_pessoa), 0) + 1 FROM alba0001")
                next_id_pessoa = cursor.fetchone()[0]

                cursor.execute("SELECT COALESCE(MAX(id_antigo), 0) + 1 FROM alba0001")
                next_id_antigo = cursor.fetchone()[0]

                # Construir SQL com todos os campos
                sql = """INSERT INTO alba0001 
                         (id_pessoa, id_antigo, recnum, tp_pessoa, nm_razao, nm_fantasia, 
                          nr_cnpj_cpf, nr_ie_rg, nr_im, nr_ddd, nr_telefone, nr_ddd2,
                          nr_telefone2, nr_ddd_cel, nr_celular, nm_email, nm_site,
                          tx_obs, fl_cliente, fl_fornec, fl_transp, fl_ativo,
                          id_tipo, id_atividade, id_transp)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

                cursor.execute(sql, (
                    next_id_pessoa, next_id_antigo, next_recnum, tipo, razao,
                    fantasia or '', cnpj or '', ie_rg or '', im or '',
                    ddd or '', telefone or '', ddd2 or '', telefone2 or '',
                    ddd_cel or '', celular or '', email or '', site or '',
                    obs or '',
                    fl_cliente, fl_fornec, fl_transp, fl_ativo,
                    id_tipo or 0, id_atividade or 0, id_transp or 0
                ))

                self.show_message(f"Cliente '{razao}' salvo com sucesso!", "success")
                self.current_id = next_id_pessoa
                self.current_recnum = next_recnum

            conn.commit()
            self.carregar_pessoas_list()  # Atualizar lista de pessoas
            self.carregar()  # Carregar endereços

        except sqlite3.IntegrityError as e:
            conn.rollback()
            self.show_message(f"ERRO ao salvar: {str(e)}", "error")
        except Exception as e:
            conn.rollback()
            self.show_message(f"ERRO inesperado: {str(e)}", "error")
        finally:
            conn.close()

    def salvar(self):
        # Coletar dados dos campos
        tipo = self._get_tipo_pessoa()
        razao = self.entry_razao.get().strip()
        fantasia = self.entry_fantasia.get().strip()
        cnpj = self.entry_doc.get().strip()
        ie_rg = self.entry_ie_rg.get().strip()
        im = self.entry_im.get().strip()
        ddd = self.entry_ddd.get().strip()
        telefone = self.entry_tel.get().strip()
        ddd2 = self.entry_ddd2.get().strip()
        telefone2 = self.entry_tel2.get().strip()
        ddd_cel = self.entry_ddd_cel.get().strip()
        celular = self.entry_celular.get().strip()
        email = self.entry_email.get().strip()
        site = self.entry_site.get().strip()
        unitron = None  # Campo removido
        obs = self.text_obs.get("1.0", tk.END).strip()

        fl_cliente = '1' if self.var_cliente.get() else '0'
        fl_fornec = '1' if self.var_fornec.get() else '0'
        fl_transp = '1' if self.var_transp.get() else '0'
        fl_ativo = '1' if self.var_ativo.get() else '0'

        nome_tipo = self.combo_tipo.get().strip()
        id_tipo = next((id for id, nome in self.tipos if nome == nome_tipo), None) if nome_tipo else None

        nome_atividade = self.combo_atividade.get().strip()
        id_atividade = next((id for id, nome in self.atividades if nome == nome_atividade), None) if nome_atividade else None

        nome_transp = self.combo_transp.get().strip()
        id_transp = next((id for id, nome in self.transportadoras if nome == nome_transp), None) if nome_transp else None

        if not razao or not tipo:
            self.show_message("ATENÇÃO: Preencha os campos obrigatórios (Razão Social e Tipo).", "warning")
            return

        confirmation_message = f"Confirma a gravação da pessoa '{razao}'?"
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('save')

        if not self.request_confirmation('save', confirmation_message, self._execute_save):
            return

    def carregar(self):
        """Carrega endereços da pessoa selecionada ou limpa se nenhuma pessoa selecionada"""
        try:
            self.tree.delete(*self.tree.get_children())
            
            if not self.current_id:
                self.show_message("Selecione uma pessoa para ver seus endereços", "info")
                return
            
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.id_ender, e.tp_ender, e.cd_cep, e.nr_numero, e.nm_compl,
                       c.nm_cidade, c.cd_uf, c.nm_bairro, c.nm_lograd
                FROM alba0002 e
                LEFT JOIN cep c ON e.cd_cep = c.cd_cep
                WHERE e.id_pessoa = ?
                ORDER BY CAST(e.id_ender AS INTEGER)
            """, (self.current_id,))
            resultados = cursor.fetchall()
            
            for row in resultados:
                self.tree.insert("", "end", values=row)
            conn.close()
            
            if resultados:
                self.show_message(f"Carregados {len(resultados)} endereços para o cliente selecionado", "success")
            else:
                self.show_message("Cliente selecionado não possui endereços cadastrados", "info")
                
        except Exception as e:
            self.show_message(f"ERRO ao carregar endereços: {str(e)}", "error")

    def on_select(self, event):
        """Evento de seleção no treeview de endereços"""
        item = self.tree.item(self.tree.focus())
        if not item:
            return

        try:
            id_ender, tp_ender, cep, numero, complemento, cidade, uf, bairro, logradouro = item["values"]
            self.show_message(f"Endereço selecionado: {tp_ender} - {logradouro}, {numero} - {cidade}/{uf}", "info")
        except Exception as e:
            self.show_message(f"ERRO ao selecionar endereço: {str(e)}", "error")

    def selecionar_pessoa_por_id(self, id_pessoa):
        """Seleciona uma pessoa e carrega seus dados nos campos e endereços no painel"""
        self.current_id = id_pessoa
        
        try:
            # Buscar todos os dados da pessoa selecionada incluindo todos os campos
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.tp_pessoa, p.nm_razao, p.nm_fantasia, p.nr_cnpj_cpf,
                       p.nr_ie_rg, p.nr_im, p.nr_ddd, p.nr_telefone, p.nr_ddd2,
                       p.nr_telefone2, p.nr_ddd_cel, p.nr_celular, p.nm_email,
                       p.nm_site, p.tx_obs,
                       p.fl_cliente, p.fl_fornec, p.fl_transp, p.fl_ativo,
                       p.id_tipo, p.id_atividade, p.id_transp, p.recnum,
                       tp.nm_tipo, a.nm_atividade, t.nm_razao as transp_nome
                FROM alba0001 p
                LEFT JOIN tipo tp ON p.id_tipo = tp.id_tipo
                LEFT JOIN ativid a ON p.id_atividade = a.id_atividade
                LEFT JOIN alba0001 t ON p.id_transp = t.id_pessoa
                WHERE p.id_pessoa = ?
            """, (id_pessoa,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                (tipo, razao, fantasia, cnpj, ie_rg, im, ddd, telefone, ddd2,
                 telefone2, ddd_cel, celular, email, site, obs,
                 fl_cliente, fl_fornec, fl_transp, fl_ativo,
                 id_tipo, id_atividade, id_transp, recnum,
                 nome_tipo, nome_atividade, nome_transp) = result
                
                # Sincronizar recnum com o registro selecionado
                self.current_recnum = recnum
                
                # Preencher os campos básicos
                tipo_label = self.tipo_pessoa_labels.get(tipo, tipo or "")
                self.combo_tipo_pessoa.set(tipo_label)
                
                self.entry_razao.delete(0, tk.END)
                self.entry_razao.insert(0, razao or "")
                
                self.entry_fantasia.delete(0, tk.END)
                self.entry_fantasia.insert(0, fantasia or "")
                
                self.entry_doc.delete(0, tk.END)
                self.entry_doc.insert(0, cnpj or "")
                
                # Preencher novos campos
                self.entry_ie_rg.delete(0, tk.END)
                self.entry_ie_rg.insert(0, ie_rg or "")
                
                self.entry_im.delete(0, tk.END)
                self.entry_im.insert(0, im or "")
                
                self.entry_ddd.delete(0, tk.END)
                self.entry_ddd.insert(0, ddd or "")
                
                self.entry_tel.delete(0, tk.END)
                self.entry_tel.insert(0, telefone or "")
                
                self.entry_ddd2.delete(0, tk.END)
                self.entry_ddd2.insert(0, ddd2 or "")
                
                self.entry_tel2.delete(0, tk.END)
                self.entry_tel2.insert(0, telefone2 or "")
                
                self.entry_ddd_cel.delete(0, tk.END)
                self.entry_ddd_cel.insert(0, ddd_cel or "")
                
                self.entry_celular.delete(0, tk.END)
                self.entry_celular.insert(0, celular or "")
                
                self.entry_email.delete(0, tk.END)
                self.entry_email.insert(0, email or "")
                
                self.entry_site.delete(0, tk.END)
                self.entry_site.insert(0, site or "")
                
                # Campo 'Cód. Unitron' removido
                
                # Preencher observações
                self.text_obs.delete("1.0", tk.END)
                self.text_obs.insert("1.0", obs or "")
                
                # Preencher combos
                self.combo_tipo.set(nome_tipo or "")
                self.combo_atividade.set(nome_atividade or "")
                self.combo_transp.set(nome_transp or "")
                
                # Preencher checkboxes
                self.var_cliente.set(1 if str(fl_cliente) == '1' else 0)
                self.var_fornec.set(1 if str(fl_fornec) == '1' else 0)
                self.var_transp.set(1 if str(fl_transp) == '1' else 0)
                self.var_ativo.set(1 if str(fl_ativo) == '1' else 0)
                
                # Atualizar label dos endereços
                self.endereco_label.config(text=f"Endereços de: {razao}")
                
                # Carregar endereços da pessoa
                self.carregar()
                
                self.show_message(f"Cliente selecionado: {razao}", "info")
                
        except Exception as e:
            self.show_message(f"ERRO ao carregar dados do cliente: {str(e)}", "error")

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.current_id = None
        self.current_recnum = None
        
        # Limpar campos básicos
        self.combo_tipo_pessoa.set("")
        self.entry_razao.delete(0, tk.END)
        self.entry_fantasia.delete(0, tk.END)
        self.entry_doc.delete(0, tk.END)
        
        # Limpar novos campos
        self.entry_ie_rg.delete(0, tk.END)
        self.entry_im.delete(0, tk.END)
        self.entry_ddd.delete(0, tk.END)
        self.entry_tel.delete(0, tk.END)
        self.entry_ddd2.delete(0, tk.END)
        self.entry_tel2.delete(0, tk.END)
        self.entry_ddd_cel.delete(0, tk.END)
        self.entry_celular.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_site.delete(0, tk.END)
        # Campo 'Cód. Unitron' removido
        
        # Limpar observações
        self.text_obs.delete("1.0", tk.END)
        
        # Limpar combos
        self.combo_tipo.set("")
        self.combo_atividade.set("")
        self.combo_transp.set("")
        
        # Limpar checkboxes
        self.var_cliente.set(0)
        self.var_fornec.set(0)
        self.var_transp.set(0)
        self.var_ativo.set(0)
        
        # Limpar lista de endereços
        self.tree.delete(*self.tree.get_children())
        
        # Resetar label dos endereços
        self.endereco_label.config(text="Endereços do Cliente Selecionado:")

    def _execute_removal(self, razao):
        try:
            conn = self.conectar()
            cursor = conn.cursor()

            # Remover endereços da pessoa primeiro
            cursor.execute("DELETE FROM alba0002 WHERE id_pessoa = ?", (self.current_id,))

            # Remover a pessoa
            cursor.execute("DELETE FROM alba0001 WHERE id_pessoa = ?", (self.current_id,))
            conn.commit()
            conn.close()

            self.carregar_pessoas_list()  # Atualizar lista de pessoas
            self.limpar()
            self.show_message(f"Cliente '{razao}' e seus endereços removidos com sucesso!", "success")
        except Exception as e:
            self.show_message(f"ERRO ao remover cliente: {str(e)}", "error")

    def remover(self):
        if not self.current_id:
            self.show_message("ATENÇÃO: Selecione uma pessoa para remover.", "warning")
            return

        razao = self.entry_razao.get()

        confirmation_message = f"Pressione 'Remover' novamente para excluir '{razao}' e todos os seus endereços."

        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('remove')

        if not self.request_confirmation('remove', confirmation_message, self._execute_removal, razao):
            return

    # Métodos de navegação entre pessoas
    def ir_primeiro(self):
        if self.pessoas_list:
            self.current_pessoa_index = 0
            id_pessoa = self.pessoas_list[0][0]
            self.selecionar_pessoa_por_id(id_pessoa)

    def ir_anterior(self):
        if self.pessoas_list and self.current_pessoa_index > 0:
            self.current_pessoa_index -= 1
            id_pessoa = self.pessoas_list[self.current_pessoa_index][0]
            self.selecionar_pessoa_por_id(id_pessoa)

    def ir_proximo(self):
        if self.pessoas_list and self.current_pessoa_index < len(self.pessoas_list) - 1:
            self.current_pessoa_index += 1
            id_pessoa = self.pessoas_list[self.current_pessoa_index][0]
            self.selecionar_pessoa_por_id(id_pessoa)

    def ir_ultimo(self):
        if self.pessoas_list:
            self.current_pessoa_index = len(self.pessoas_list) - 1
            id_pessoa = self.pessoas_list[-1][0]
            self.selecionar_pessoa_por_id(id_pessoa)
