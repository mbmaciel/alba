import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class SystemConfigWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Configurações do Sistema")
        self.config(width=900, height=700)

        self.campos = {}
        
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

        # Create notebook with tabs for different categories
        notebook = ttkb.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Company Information Tab
        company_frame = ttkb.Frame(notebook, padding=10)
        notebook.add(company_frame, text="Informações da Empresa")
        
        # Contact Information Tab
        contact_frame = ttkb.Frame(notebook, padding=10)
        notebook.add(contact_frame, text="Contato")
        
        # System Paths Tab
        paths_frame = ttkb.Frame(notebook, padding=10)
        notebook.add(paths_frame, text="Caminhos do Sistema")
        
        # Other Settings Tab
        other_frame = ttkb.Frame(notebook, padding=10)
        notebook.add(other_frame, text="Outras Configurações")
        
        # Company Information Fields
        company_fields = [
            ("Razão Social", "nm_razao"),
            ("CNPJ", "nr_cnpj"),
            ("Inscrição Estadual", "nr_ie"),
            ("Inscrição Municipal", "nr_im")
        ]
        
        # Address Fields
        address_fields = [
            ("CEP", "cd_cep"),
            ("Número", "nr_numero"),
            ("Complemento", "nm_compl")
        ]
        
        # Contact Fields
        contact_fields = [
            ("DDD", "nr_ddd"),
            ("Telefone", "nr_fone")
        ]
        
        # System Paths Fields
        path_fields = [
            ("Caminho XML", "nm_path_xml"),
            ("Caminho Temp", "nm_path_temp"),
            ("Certificado", "nm_certificado")
        ]
        
        # Other Settings Fields
        other_fields = [
            ("Manutenção (S/N)", "fl_manutencao"),
            ("Buscar CEP", "cd_buscarcep"),
            ("Vendedor", "nm_vendedor")
        ]
        
        # Create Company Information section
        self._create_section(company_frame, "Dados da Empresa", company_fields, 0)
        self._create_section(company_frame, "Endereço", address_fields, len(company_fields) + 1)
        
        # Create Contact Information section
        self._create_section(contact_frame, "Informações de Contato", contact_fields, 0)
        
        # Create System Paths section
        self._create_section(paths_frame, "Caminhos do Sistema", path_fields, 0)
        
        # Create Other Settings section
        self._create_section(other_frame, "Outras Configurações", other_fields, 0)

        # Frame para o Treeview (área expandida) - Mostra histórico de configurações
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))

        # Label para o histórico
        ttkb.Label(tree_frame, text="Histórico de Configurações", font=("MS Sans Serif", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "razao", "cnpj", "telefone", "data_config"), show="headings", height=8)
        
        # Configuração das colunas
        self.tree.heading("id", text="COD")
        self.tree.heading("razao", text="Razão Social")
        self.tree.heading("cnpj", text="CNPJ")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("data_config", text="Data Configuração")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("razao", width=250, minwidth=200, anchor=tk.W)
        self.tree.column("cnpj", width=150, minwidth=120, anchor=tk.CENTER)
        self.tree.column("telefone", width=120, minwidth=100, anchor=tk.CENTER)
        self.tree.column("data_config", width=150, minwidth=120, anchor=tk.CENTER)
        
        # Scrollbar para o Treeview
        scrollbar_tree = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_tree.set)
        
        # Pack do Treeview e Scrollbar
        tree_container = ttkb.Frame(tree_frame)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, in_=tree_container)
        scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y, in_=tree_container)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def _create_section(self, parent, title, fields, start_row):
        """Helper method to create a section with a title and fields"""
        # Section title
        if title:
            section_label = ttkb.Label(parent, text=title, font=("MS Sans Serif", 12, "bold"))
            section_label.grid(row=start_row, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
            start_row += 1
        
        # Create fields
        for i, (label, campo) in enumerate(fields):
            row = start_row + i
            ttkb.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, padx=(5, 10), pady=3)
            entry = ttkb.Entry(parent, width=50)
            entry.grid(row=row, column=1, pady=3, padx=5, sticky=tk.W)
            self.campos[campo] = entry
        
        return start_row + len(fields)

    def novo(self):
        """Limpa os campos para nova configuração"""
        self.limpar()
        # Focar no primeiro campo da primeira aba
        if "nm_razao" in self.campos:
            self.campos["nm_razao"].focus()

    def carregar(self):
        # Carregar dados atuais
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM system LIMIT 1")
        row = cursor.fetchone()
        if row:
            colnames = [desc[0] for desc in cursor.description]
            for i, campo in enumerate(colnames):
                if campo in self.campos:
                    self.campos[campo].delete(0, tk.END)
                    self.campos[campo].insert(0, str(row[i]) if row[i] is not None else "")
        
        # Carregar histórico no treeview
        self.carregar_historico()
        conn.close()

    def carregar_historico(self):
        """Carrega o histórico de configurações no treeview"""
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT rowid, nm_razao, nr_cnpj, nr_fone, 
                   COALESCE(data_config, 'Não informado') as data_config 
            FROM system 
            ORDER BY rowid DESC
        """)
        
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def _execute_save(self):
        valores = {campo: self.campos[campo].get() for campo in self.campos}
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            # Adicionar timestamp
            valores["data_config"] = "datetime('now', 'localtime')"
            
            cursor.execute("DELETE FROM system")
            
            # Construir query com timestamp
            campos = list(valores.keys())
            valores_query = []
            for campo in campos:
                if campo == "data_config":
                    valores_query.append("datetime('now', 'localtime')")
                else:
                    valores_query.append("?")
            
            query = f"INSERT INTO system ({', '.join(campos)}) VALUES ({', '.join(valores_query)})"
            valores_sem_timestamp = [v for k, v in valores.items() if k != "data_config"]
            
            cursor.execute(query, valores_sem_timestamp)
            conn.commit()
            self.show_message("Configurações salvas com sucesso!", "success")
            self.carregar_historico()
        except Exception as e:
            self.show_message(f"Erro ao salvar configurações: {str(e)}", "error")
        finally:
            conn.close()

    def salvar(self):
        valores = {campo: self.campos[campo].get() for campo in self.campos}

        # Validação básica
        if not valores.get("nm_razao", "").strip():
            self.show_message("Razão Social é obrigatória.", "warning")
            return

        confirmation_message = f"Confirma a gravação das configurações para '{valores.get('nm_razao')}'?"
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('save')

        if not self.request_confirmation('save', confirmation_message, self._execute_save):
            return

    def _execute_removal(self):
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM system")
            conn.commit()
            self.show_message("Configurações removidas com sucesso!", "success")
            self.limpar()
            self.carregar_historico()
        except Exception as e:
            self.show_message(f"Erro ao remover configurações: {str(e)}", "error")
        finally:
            conn.close()

    def remover(self):
        """Remove a configuração atual"""
        confirmation_message = "Pressione 'Remover' novamente para apagar TODAS as configurações. Esta ação não pode ser desfeita."
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('remove')

        if not self.request_confirmation('remove', confirmation_message, self._execute_removal):
            return

    def on_select(self, event):
        """Carrega configuração selecionada no histórico"""
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        
        rowid = item["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM system WHERE rowid = ?", (rowid,))
        row = cursor.fetchone()
        
        if row:
            colnames = [desc[0] for desc in cursor.description]
            for i, campo in enumerate(colnames):
                if campo in self.campos:
                    self.campos[campo].delete(0, tk.END)
                    self.campos[campo].insert(0, str(row[i]) if row[i] is not None else "")
        conn.close()

    def limpar(self):
        """Limpa todos os campos"""
        for campo in self.campos:
            self.campos[campo].delete(0, tk.END)

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
        
