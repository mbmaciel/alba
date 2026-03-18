import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class UsuarioWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Cadastro de Usuários")
        self.config(width=700, height=500)
        
        # Initialize record state fields
        self.current_id = None
        self.current_recnum = None

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

        # Frame para campos de entrada
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        # Primeira linha
        ttkb.Label(input_frame, text="Nome do Usuário").grid(row=0, column=0, sticky=tk.W)
        self.entry_nome = ttkb.Entry(input_frame, width=50)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=(5, 20))

        # Segunda linha - Campos adicionais para usuários
        ttkb.Label(input_frame, text="Login").grid(row=1, column=0, sticky=tk.W)
        self.entry_login = ttkb.Entry(input_frame, width=30)
        self.entry_login.grid(row=1, column=1, pady=5, padx=(5, 20), sticky=tk.W)

        # Terceira linha
        ttkb.Label(input_frame, text="Email").grid(row=2, column=0, sticky=tk.W)
        self.entry_email = ttkb.Entry(input_frame, width=50)
        self.entry_email.grid(row=2, column=1, pady=5, padx=(5, 20))

        # Quarta linha
        ttkb.Label(input_frame, text="Perfil").grid(row=3, column=0, sticky=tk.W)
        self.combo_perfil = ttkb.Combobox(input_frame, width=25, state="readonly")
        self.combo_perfil["values"] = ["Administrador", "Usuário", "Vendedor", "Operador", "Consulta"]
        self.combo_perfil.grid(row=3, column=1, pady=5, padx=(5, 20), sticky=tk.W)

        # Quinta linha
        ttkb.Label(input_frame, text="Status").grid(row=4, column=0, sticky=tk.W)
        self.combo_status = ttkb.Combobox(input_frame, width=15, state="readonly")
        self.combo_status["values"] = ["Ativo", "Inativo", "Bloqueado"]
        self.combo_status.grid(row=4, column=1, pady=5, padx=(5, 20), sticky=tk.W)
        self.combo_status.set("Ativo")  # Valor padrão

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "nome", "login", "email", "perfil", "status"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("login", text="Login")
        self.tree.heading("email", text="Email")
        self.tree.heading("perfil", text="Perfil")
        self.tree.heading("status", text="Status")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("nome", width=200, minwidth=150, anchor=tk.W)
        self.tree.column("login", width=120, minwidth=100, anchor=tk.W)
        self.tree.column("email", width=180, minwidth=150, anchor=tk.W)
        self.tree.column("perfil", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column("status", width=80, minwidth=60, anchor=tk.CENTER)
        
        # Scrollbar para o Treeview
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar_campos()
        self.current_id = None
        self.current_recnum = None
        self.entry_nome.focus()

    def _execute_save(self):
        nome = self.entry_nome.get().strip()
        login = self.entry_login.get().strip()
        email = self.entry_email.get().strip()
        perfil = self.combo_perfil.get()
        status = self.combo_status.get()

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            if self.current_id is None:
                # INSERT - New record
                # Verificar se o login já existe
                cursor.execute("SELECT COUNT(*) FROM usuario WHERE nm_login = ?", (login,))
                if cursor.fetchone()[0] > 0:
                    self.show_message("Este login já está sendo usado por outro usuário.", "warning")
                    return

                # Get next id_usuario
                cursor.execute("SELECT COALESCE(MAX(id_usuario), 0) + 1 FROM usuario")
                next_id = cursor.fetchone()[0]

                # Use comprehensive INSERT method with recnum handling
                insert_query = """
                    INSERT INTO usuario (recnum, id_usuario, nm_nome, nm_login, nm_email, nm_perfil, fl_status, login, senha) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, '')
                """
                params = (None, next_id, nome, login, email, perfil, status, login)  # recnum will be set by utility method

                success, next_recnum, error_msg = self.execute_insert_with_recnum_handling(
                    "usuario", insert_query, params, f"usuário '{nome}'"
                )

                if not success:
                    self.show_message(f"Erro ao salvar usuário: {error_msg}", "error")
                    return

                # Update current state
                self.current_id = next_id
                self.set_current_recnum(next_recnum)

                # Log the operation
                self.log_recnum_operation("INSERT", "usuario", next_recnum, True)

                self.show_message("Usuário salvo com sucesso!", "success")
            else:
                # UPDATE - Existing record
                # Verificar se o login já existe para outro usuário
                cursor.execute("SELECT COUNT(*) FROM usuario WHERE nm_login = ? AND id_usuario != ?", (login, self.current_id))
                if cursor.fetchone()[0] > 0:
                    self.show_message("Este login já está sendo usado por outro usuário.", "warning")
                    return

                # Update existing user (preserve recnum)
                cursor.execute("""
                    UPDATE usuario SET 
                        nm_login = ?, nm_email = ?, nm_perfil = ?, fl_status = ?
                    WHERE id_usuario = ?
                """, (login, email, perfil, status, self.current_id))

                self.show_message("Usuário atualizado com sucesso!", "success")

            conn.commit()
            self.carregar()

        except Exception as e:
            self.show_message(f"Erro ao salvar: {str(e)}", "error")
        finally:
            conn.close()

    def salvar(self):
        nome = self.entry_nome.get().strip()
        login = self.entry_login.get().strip()
        email = self.entry_email.get().strip()
        perfil = self.combo_perfil.get()
        status = self.combo_status.get()

        if not nome:
            self.show_message("Nome do usuário é obrigatório.", "warning")
            return

        if not login:
            self.show_message("Login é obrigatório.", "warning")
            return

        # Validação básica de email
        if email and "@" not in email:
            self.show_message("Digite um email válido.", "warning")
            return

        confirmation_message = f"Confirma a gravação do usuário '{nome}'?"
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('save')

        if not self.request_confirmation('save', confirmation_message, self._execute_save):
            return

    def _execute_removal(self, id_usuario, nome_usuario):
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
            conn.commit()
            self.show_message(f"Usuário '{nome_usuario}' removido com sucesso!", "success")
            self.carregar()
            self.limpar_campos()
        except Exception as e:
            self.show_message(f"Erro ao remover: {str(e)}", "error")
        finally:
            conn.close()
            
    def remover(self):
        item = self.tree.focus()
        if not item:
            self.show_message("Selecione um usuário para remover.", "warning")
            return

        values = self.tree.item(item)["values"]
        id_usuario = values[0]
        nome_usuario = values[1]

        confirmation_message = f"Pressione 'Remover' novamente para excluir o usuário '{nome_usuario}'."

        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('remove')

        if not self.request_confirmation('remove', confirmation_message, self._execute_removal, id_usuario, nome_usuario):
            return

    def carregar(self):
        # Limpar treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        conn = self.conectar()
        cursor = conn.cursor()
        
        try:
            # Verificar se as colunas existem, se não, criá-las
            cursor.execute("PRAGMA table_info(usuario)")
            colunas = [col[1] for col in cursor.fetchall()]
            
            if 'nm_login' not in colunas:
                cursor.execute("ALTER TABLE usuario ADD COLUMN nm_login TEXT")
            if 'nm_email' not in colunas:
                cursor.execute("ALTER TABLE usuario ADD COLUMN nm_email TEXT")
            if 'nm_perfil' not in colunas:
                cursor.execute("ALTER TABLE usuario ADD COLUMN nm_perfil TEXT DEFAULT 'Usuário'")
            if 'fl_status' not in colunas:
                cursor.execute("ALTER TABLE usuario ADD COLUMN fl_status TEXT DEFAULT 'Ativo'")
            
            conn.commit()
            
            # Carregar dados
            cursor.execute("""
                SELECT id_usuario, nm_nome, 
                       COALESCE(nm_login, '') as nm_login,
                       COALESCE(nm_email, '') as nm_email,
                       COALESCE(nm_perfil, 'Usuário') as nm_perfil,
                       COALESCE(fl_status, 'Ativo') as fl_status
                FROM usuario 
                ORDER BY nm_nome
            """)
            
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
                
        except Exception as e:
            self.show_message(f"Erro ao carregar: {str(e)}", "error")
        finally:
            conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
            
        values = item["values"]
        if len(values) >= 6:
            id_usuario, nome, login, email, perfil, status = values
            
            # Update current record state
            self.current_id = id_usuario
            
            # Get recnum from database for synchronization
            conn = self.conectar()
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT recnum FROM usuario WHERE id_usuario = ?", (id_usuario,))
                result = cursor.fetchone()
                if result:
                    self.current_recnum = result[0]
                else:
                    self.current_recnum = None
            except Exception as e:
                self.show_message(f"Erro ao obter recnum: {str(e)}", "error")
                self.current_recnum = None
            finally:
                conn.close()
            
            # Update form fields
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, nome or "")
            
            self.entry_login.delete(0, tk.END)
            self.entry_login.insert(0, login or "")
            
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, email or "")
            
            self.combo_perfil.set(perfil or "Usuário")
            self.combo_status.set(status or "Ativo")

    def limpar_campos(self):
        """Limpa todos os campos do formulário e estado do registro"""
        self.entry_nome.delete(0, tk.END)
        self.entry_login.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.combo_perfil.set("")
        self.combo_status.set("Ativo")
        
        # Clear record state
        self.current_id = None
        self.current_recnum = None

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
        
