import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class NatopWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_id = None  # Para controlar inserção/atualização
        self.current_recnum = None  # Para controlar recnum do registro atual
        self.current_cfop = None  # Para controlar o CFOP original na edição
        aplicar_estilo(self)
        self.set_title("Cadastro de Naturezas da Operação (NATOP)")
        self.config(width=900, height=500)

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
        ttkb.Label(input_frame, text="Descrição").grid(row=0, column=0, sticky=tk.W)
        self.entry_desc = ttkb.Entry(input_frame, width=40)
        self.entry_desc.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="CFOP").grid(row=0, column=2, sticky=tk.W)
        self.entry_cfop = ttkb.Entry(input_frame, width=20)
        self.entry_cfop.grid(row=0, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Fluxo").grid(row=0, column=4, sticky=tk.W)
        self.var_fluxo = tk.BooleanVar()
        self.check_fluxo = ttkb.Checkbutton(input_frame, variable=self.var_fluxo)
        self.check_fluxo.grid(row=0, column=5, pady=5, padx=5, sticky=tk.W)

        # Segunda linha
        ttkb.Label(input_frame, text="Livro Entrada").grid(row=1, column=0, sticky=tk.W)
        self.var_ent = tk.BooleanVar()
        self.check_ent = ttkb.Checkbutton(input_frame, variable=self.var_ent)
        self.check_ent.grid(row=1, column=1, pady=5, padx=(5, 20), sticky=tk.W)

        ttkb.Label(input_frame, text="Livro Saída").grid(row=1, column=2, sticky=tk.W)
        self.var_sai = tk.BooleanVar()
        self.check_sai = ttkb.Checkbutton(input_frame, variable=self.var_sai)
        self.check_sai.grid(row=1, column=3, pady=5, padx=(5, 20), sticky=tk.W)

        ttkb.Label(input_frame, text="Livro Serviço").grid(row=1, column=4, sticky=tk.W)
        self.var_srv = tk.BooleanVar()
        self.check_srv = ttkb.Checkbutton(input_frame, variable=self.var_srv)
        self.check_srv.grid(row=1, column=5, pady=5, padx=5, sticky=tk.W)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas incluindo checkboxes
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "desc", "cfop", "fluxo", "ent", "sai", "srv"), show="headings", height=15)
        
        # Configuração das colunas com ordenação
        self.sort_id = True  # True = crescente, False = decrescente
        self.sort_desc = True
        self.sort_cfop = True
        
        self.tree.heading("id", text="COD ↕", command=lambda: self.ordenar_id())
        self.tree.heading("desc", text="Descrição ↕", command=lambda: self.ordenar_desc())
        self.tree.heading("cfop", text="CFOP ↕", command=lambda: self.ordenar_cfop())
        self.tree.heading("fluxo", text="Fluxo")
        self.tree.heading("ent", text="L.Ent")
        self.tree.heading("sai", text="L.Saí")
        self.tree.heading("srv", text="L.Srv")
        
        # Configurar colunas
        self.tree.column("id", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("desc", width=300, minwidth=200, anchor=tk.W)
        self.tree.column("cfop", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column("fluxo", width=60, minwidth=50, anchor=tk.CENTER)
        self.tree.column("ent", width=60, minwidth=50, anchor=tk.CENTER)
        self.tree.column("sai", width=60, minwidth=50, anchor=tk.CENTER)
        self.tree.column("srv", width=60, minwidth=50, anchor=tk.CENTER)
        
        # Scrollbar para o Treeview
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

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

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.current_id = None
        self.current_recnum = None
        self.current_cfop = None
        self.limpar()
        self.entry_desc.focus()
        self.show_message("Novo registro. Preencha os campos e salve.", "info")

    def _execute_save(self):
        try:
            desc = self.entry_desc.get()
            cfop = self.entry_cfop.get()
            fluxo = "S" if self.var_fluxo.get() else ""
            ent = "S" if self.var_ent.get() else ""
            sai = "S" if self.var_sai.get() else ""
            srv = "S" if self.var_srv.get() else ""

            conn = self.conectar()
            cursor = conn.cursor()

            try:
                if self.current_id is None:
                    # Novo registro - INSERT
                    # Verificar se CFOP já existe
                    cursor.execute("SELECT COUNT(*) FROM natop WHERE cd_cfop = ?", (cfop,))
                    existe = cursor.fetchone()[0]

                    if existe:
                        self.show_message(f"CFOP {cfop} já existe! Use um CFOP diferente.", "warning")
                        return

                    # Use comprehensive INSERT method with recnum handling
                    insert_query = """
                        INSERT INTO natop (recnum, ds_natop, cd_cfop, fl_fluxo, fl_livro_ent, fl_livro_sai, fl_livro_srv)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """
                    params = (None, desc, cfop, fluxo, ent, sai, srv)  # recnum will be set by utility method

                    success, next_recnum, error_msg = self.execute_insert_with_recnum_handling(
                        "natop", insert_query, params, f"NATOP '{desc}'"
                    )

                    if not success:
                        self.show_message(f"Erro ao salvar NATOP: {error_msg}", "error")
                        return

                    # Sincronizar recnum atual
                    self.set_current_recnum(next_recnum)
                    self.log_recnum_operation("INSERT", "natop", next_recnum, True)
                    self.show_message("NATOP incluído com sucesso!", "success")
                else:
                    # Atualização - UPDATE
                    # Verificar se CFOP já existe em outro registro somente se foi alterado
                    if self.current_cfop is None or cfop != self.current_cfop:
                        cursor.execute("SELECT COUNT(*) FROM natop WHERE cd_cfop = ? AND id_natop != ?", (cfop, self.current_id))
                        existe = cursor.fetchone()[0]

                        if existe:
                            self.show_message(f"CFOP {cfop} já existe em outro registro!", "warning")
                            return

                    cursor.execute("""
                        UPDATE natop SET ds_natop=?, cd_cfop=?, fl_fluxo=?, fl_livro_ent=?, fl_livro_sai=?, fl_livro_srv=?
                        WHERE id_natop=?""",
                        (desc, cfop, fluxo, ent, sai, srv, self.current_id)
                    )
                    self.show_message("NATOP atualizado com sucesso!", "success")

                conn.commit()
                self.limpar()
                self.carregar()

            except sqlite3.Error as e:
                self.show_message(f"Erro ao salvar: {str(e)}", "error")
                conn.rollback()
            finally:
                conn.close()

        except Exception as e:
            self.show_message(f"Erro inesperado: {str(e)}", "error")

    def salvar(self):
        try:
            desc = self.entry_desc.get()
            cfop = self.entry_cfop.get()
            fluxo = "S" if self.var_fluxo.get() else ""
            ent = "S" if self.var_ent.get() else ""
            sai = "S" if self.var_sai.get() else ""
            srv = "S" if self.var_srv.get() else ""

            if not desc or not cfop:
                self.show_message("Preencha os campos obrigatórios (Descrição e CFOP).", "warning")
                return

            confirmation_message = f"Confirma a gravação da natureza de operação '{desc}'?"
            if not hasattr(self, '_confirmations'):
                self.setup_confirmation_pattern('save')

            if not self.request_confirmation('save', confirmation_message, self._execute_save):
                return

        except Exception as e:
            self.show_message(f"Erro inesperado: {str(e)}", "error")

    def _execute_removal(self, id_natop, desc_natop):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM natop WHERE id_natop = ?", (id_natop,))
            conn.commit()
            conn.close()
            self.carregar()
            self.limpar()
            self.show_message(f"NATOP '{desc_natop}' removido com sucesso!", "success")
        except sqlite3.Error as e:
            self.show_message(f"Erro ao remover: {str(e)}", "error")

    def remover(self):
        try:
            item = self.tree.focus()
            if not item:
                self.show_message("Selecione um registro para remover.", "warning")
                return

            id_natop = self.tree.item(item)["values"][0]
            desc_natop = self.tree.item(item)["values"][1]

            confirmation_message = f"Pressione 'Remover' novamente para excluir a natureza de operação '{desc_natop}'."

            if not hasattr(self, '_confirmations'):
                self.setup_confirmation_pattern('remove')

            if not self.request_confirmation('remove', confirmation_message, self._execute_removal, id_natop, desc_natop):
                return

        except Exception as e:
            self.show_message(f"Erro inesperado: {str(e)}", "error")

    def carregar(self):
        try:
            self.tree.delete(*self.tree.get_children())
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_natop, ds_natop, cd_cfop, fl_fluxo, fl_livro_ent, fl_livro_sai, fl_livro_srv FROM natop ORDER BY ds_natop")
            for row in cursor.fetchall():
                # Converter flags para checkmarks
                id_natop, desc, cfop, fluxo, ent, sai, srv = row
                fluxo_check = "✓" if fluxo == "S" else ""
                ent_check = "✓" if ent == "S" else ""
                sai_check = "✓" if sai == "S" else ""
                srv_check = "✓" if srv == "S" else ""
                
                self.tree.insert("", "end", values=(id_natop, desc, cfop, fluxo_check, ent_check, sai_check, srv_check))
            conn.close()
        except sqlite3.Error as e:
            self.show_message(f"Erro ao carregar dados: {str(e)}", "error")

    def on_select(self, event):
        try:
            item = self.tree.item(self.tree.focus())
            if not item or not item.get("values"):
                return
                
            values = item["values"]
            id_natop, desc, cfop = values[0], values[1], values[2]
            self.current_id = id_natop  # Armazenar ID para edição
            self.current_cfop = cfop
            
            # Buscar todos os dados do registro selecionado
            try:
                conn = self.conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT recnum, fl_fluxo, fl_livro_ent, fl_livro_sai, fl_livro_srv FROM natop WHERE id_natop = ?", (id_natop,))
                result = cursor.fetchone()
                if result:
                    self.current_recnum, fluxo, ent, sai, srv = result
                else:
                    self.current_recnum = None
                    fluxo = ent = sai = srv = ""
                conn.close()
            except sqlite3.Error as e:
                self.show_message(f"Erro ao obter dados: {str(e)}", "error")
                self.current_recnum = None
                fluxo = ent = sai = srv = ""
            
            self.entry_desc.delete(0, tk.END)
            self.entry_desc.insert(0, desc or "")
            
            self.entry_cfop.delete(0, tk.END)
            self.entry_cfop.insert(0, cfop or "")
            
            # Configurar checkboxes baseado nos valores "S" ou vazio
            self.var_fluxo.set(fluxo == "S")
            self.var_ent.set(ent == "S")
            self.var_sai.set(sai == "S")
            self.var_srv.set(srv == "S")
            
            self.show_message(f"NATOP selecionado para edição: {desc}", "info")
            
        except Exception as e:
            self.show_message(f"Erro ao selecionar: {str(e)}", "error")

    def limpar(self):
        self.current_id = None
        self.current_recnum = None
        self.current_cfop = None
        self.entry_desc.delete(0, tk.END)
        self.entry_cfop.delete(0, tk.END)
        self.var_fluxo.set(False)
        self.var_ent.set(False)
        self.var_sai.set(False)
        self.var_srv.set(False)

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
            self.show_message(f"Erro ao navegar: {str(e)}", "error")
    def ordenar_desc(self):
        """Ordena por descrição"""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            order = "ASC" if self.sort_desc else "DESC"
            cursor.execute(f"SELECT id_natop, ds_natop, cd_cfop, fl_fluxo, fl_livro_ent, fl_livro_sai, fl_livro_srv FROM natop ORDER BY ds_natop {order}")
            
            self.tree.delete(*self.tree.get_children())
            for row in cursor.fetchall():
                id_natop, desc, cfop, fluxo, ent, sai, srv = row
                fluxo_check = "✓" if fluxo == "S" else ""
                ent_check = "✓" if ent == "S" else ""
                sai_check = "✓" if sai == "S" else ""
                srv_check = "✓" if srv == "S" else ""
                self.tree.insert("", "end", values=(id_natop, desc, cfop, fluxo_check, ent_check, sai_check, srv_check))
            
            icon = "↑" if self.sort_desc else "↓"
            self.tree.heading("desc", text=f"Descrição {icon}", command=lambda: self.ordenar_desc())
            self.sort_desc = not self.sort_desc
            conn.close()
        except Exception as e:
            self.show_message(f"Erro ao ordenar: {str(e)}", "error")

    def ordenar_cfop(self):
        """Ordena por CFOP"""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            order = "ASC" if self.sort_cfop else "DESC"
            cursor.execute(f"SELECT id_natop, ds_natop, cd_cfop, fl_fluxo, fl_livro_ent, fl_livro_sai, fl_livro_srv FROM natop ORDER BY CAST(cd_cfop AS INTEGER) {order}")
            
            self.tree.delete(*self.tree.get_children())
            for row in cursor.fetchall():
                id_natop, desc, cfop, fluxo, ent, sai, srv = row
                fluxo_check = "✓" if fluxo == "S" else ""
                ent_check = "✓" if ent == "S" else ""
                sai_check = "✓" if sai == "S" else ""
                srv_check = "✓" if srv == "S" else ""
                self.tree.insert("", "end", values=(id_natop, desc, cfop, fluxo_check, ent_check, sai_check, srv_check))
            
            icon = "↑" if self.sort_cfop else "↓"
            self.tree.heading("cfop", text=f"CFOP {icon}", command=lambda: self.ordenar_cfop())
            self.sort_cfop = not self.sort_cfop
            conn.close()
        except Exception as e:
            self.show_message(f"Erro ao ordenar: {str(e)}", "error")
    def ordenar_id(self):
        """Ordena por ID"""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            order = "ASC" if self.sort_id else "DESC"
            cursor.execute(f"SELECT id_natop, ds_natop, cd_cfop, fl_fluxo, fl_livro_ent, fl_livro_sai, fl_livro_srv FROM natop ORDER BY CAST(id_natop AS INTEGER) {order}")
            
            self.tree.delete(*self.tree.get_children())
            for row in cursor.fetchall():
                id_natop, desc, cfop, fluxo, ent, sai, srv = row
                fluxo_check = "✓" if fluxo == "S" else ""
                ent_check = "✓" if ent == "S" else ""
                sai_check = "✓" if sai == "S" else ""
                srv_check = "✓" if srv == "S" else ""
                self.tree.insert("", "end", values=(id_natop, desc, cfop, fluxo_check, ent_check, sai_check, srv_check))
            
            icon = "↑" if self.sort_id else "↓"
            self.tree.heading("id", text=f"COD {icon}", command=lambda: self.ordenar_id())
            self.sort_id = not self.sort_id
            conn.close()
        except Exception as e:
            self.show_message(f"Erro ao ordenar: {str(e)}", "error")
