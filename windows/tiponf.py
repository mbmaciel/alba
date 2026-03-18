import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class TiponfWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_id = None
        self.current_recnum = None
        aplicar_estilo(self)
        self.set_title("Cadastro de Tipos de Nota Fiscal")
        self.config(width=800, height=550)

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

        ttkb.Label(input_frame, text="Nome").grid(row=0, column=0, sticky=tk.W)
        self.entry_nome = ttkb.Entry(input_frame, width=40)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Tipo (fl_tiponf)").grid(row=1, column=0, sticky=tk.W)
        self.combo_tipo = ttkb.Combobox(input_frame, width=27, values=["M", "S"], state="readonly")
        self.combo_tipo.grid(row=1, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Mapa (fl_mapa)").grid(row=2, column=0, sticky=tk.W)
        self.var_mapa = tk.BooleanVar()
        self.check_mapa = ttkb.Checkbutton(input_frame, text="Ativo", variable=self.var_mapa)
        self.check_mapa.grid(row=2, column=1, pady=5, padx=(5, 20), sticky=tk.W)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas (removendo colunas Tipo e Mapa)
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "nome"), show="headings", height=15)

        # Configuração das colunas com ordenação
        self.sort_id = True  # True = crescente, False = decrescente
        self.sort_nome = True
        
        self.tree.heading("id", text="COD ↕", command=lambda: self.ordenar_id())
        self.tree.heading("nome", text="Nome ↕", command=lambda: self.ordenar_nome())

        # Configurar coluna ID visível
        self.tree.column("id", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("nome", width=500, minwidth=300, anchor=tk.W)

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
        self.clear_record_state()
        self.limpar()
        self.entry_nome.focus()
        self.show_message("Novo registro. Preencha os campos e salve.", "info")

    def _execute_save(self):
        try:
            nome = self.entry_nome.get()
            tipo = self.combo_tipo.get()
            mapa = "1" if self.var_mapa.get() else "0"

            conn = self.conectar()
            cursor = conn.cursor()

            try:
                if self.current_id is None:
                    # Novo registro - usar utility method para obter próximo recnum
                    next_recnum = self.get_next_recnum("tiponf")
                    if next_recnum is None:
                        return  # Error message already shown by get_next_recnum

                    cursor.execute(
                        "INSERT INTO tiponf (recnum, nm_tiponf, fl_tiponf, fl_mapa) VALUES (?, ?, ?, ?)",
                        (next_recnum, nome, tipo, mapa)
                    )

                    # Sincronizar recnum após INSERT bem-sucedido
                    self.set_current_recnum(next_recnum)
                    self.show_message(f"Tipo de NF '{nome}' incluído com sucesso!", "success")
                else:
                    # Atualização - preservar recnum existente
                    cursor.execute(
                        "UPDATE tiponf SET nm_tiponf=?, fl_tiponf=?, fl_mapa=? WHERE id_tiponf=?",
                        (nome, tipo, mapa, self.current_id)
                    )
                    self.show_message(f"Tipo de NF '{nome}' atualizado com sucesso!", "success")

                conn.commit()
                self.limpar()
                self.carregar()
                self.clear_record_state()

            except sqlite3.Error as e:
                self.show_message(f"Erro ao salvar registro: {str(e)}", "error")
                conn.rollback()
            finally:
                conn.close()
        except Exception as e:
            self.show_message(f"Erro inesperado: {str(e)}", "error")

    def salvar(self):
        try:
            nome = self.entry_nome.get()
            tipo = self.combo_tipo.get()
            mapa = "1" if self.var_mapa.get() else "0"

            if not nome:
                self.show_message("Nome é obrigatório.", "warning")
                return

            confirmation_message = f"Confirma a gravação do tipo de nota fiscal '{nome}'?"
            if not hasattr(self, '_confirmations'):
                self.setup_confirmation_pattern('save')

            if not self.request_confirmation('save', confirmation_message, self._execute_save):
                return

        except Exception as e:
            self.show_message(f"Erro inesperado: {str(e)}", "error")

    def _execute_removal(self, id_tiponf, nome):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tiponf WHERE id_tiponf = ?", (id_tiponf,))
            conn.commit()
            conn.close()
            self.carregar()
            self.limpar()
            self.show_message(f"Tipo de NF '{nome}' removido com sucesso!", "success")
        except sqlite3.Error as e:
            self.show_message(f"Erro ao remover: {str(e)}", "error")

    def remover(self):
        try:
            item = self.tree.focus()
            if not item:
                self.show_message("Selecione um registro para remover.", "warning")
                return

            item_values = self.tree.item(item)["values"]
            id_tiponf = item_values[0]
            nome = item_values[1]
            
            confirmation_message = f"Pressione 'Remover' novamente para excluir o tipo de nota fiscal '{nome}'."

            if not hasattr(self, '_confirmations'):
                self.setup_confirmation_pattern('remove')

            if not self.request_confirmation('remove', confirmation_message, self._execute_removal, id_tiponf, nome):
                return

        except Exception as e:
            self.show_message(f"Erro inesperado: {str(e)}", "error")

    def carregar(self):
        try:
            self.tree.delete(*self.tree.get_children())
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_tiponf, nm_tiponf FROM tiponf ORDER BY nm_tiponf")
            resultados = cursor.fetchall()
            for row in resultados:
                self.tree.insert("", "end", values=row)
            conn.close()
            self.show_message(f"Carregados {len(resultados)} tipos de nota fiscal", "success")
        except sqlite3.Error as e:
            self.show_message(f"Erro ao carregar dados: {str(e)}", "error")

    def on_select(self, event):
        try:
            item = self.tree.item(self.tree.focus())
            if not item or not item.get("values"):
                return
            
            values = item["values"]
            if len(values) >= 2:
                id_tiponf, nome = values
                self.current_id = id_tiponf
                
                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, nome or "")
                
                # Buscar os valores completos do banco de dados
                conn = self.conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT fl_tiponf, fl_mapa, recnum FROM tiponf WHERE id_tiponf = ?", (self.current_id,))
                result = cursor.fetchone()
                if result:
                    tipo_value, mapa_value, recnum_value = result
                    
                    self.combo_tipo.set(tipo_value if tipo_value else "")
                    
                    # Converter para boolean - aceita tanto string quanto número
                    self.var_mapa.set(str(mapa_value) == "1" or mapa_value == 1)
                    
                    # Sincronizar recnum com o registro selecionado
                    self.set_current_recnum(recnum_value)
                conn.close()
                
                self.show_message(f"Tipo selecionado para edição: {nome}", "info")
        except Exception as e:
            self.show_message(f"Erro ao selecionar: {str(e)}", "error")

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.clear_record_state()
        self.entry_nome.delete(0, tk.END)
        self.combo_tipo.set("")
        self.var_mapa.set(False)

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
        
    def ordenar_id(self):
        """Ordena por ID"""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            order = "ASC" if self.sort_id else "DESC"
            cursor.execute(f"SELECT id_tiponf, nm_tiponf FROM tiponf ORDER BY CAST(id_tiponf AS INTEGER) {order}")
            
            self.tree.delete(*self.tree.get_children())
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            
            icon = "↑" if self.sort_id else "↓"
            self.tree.heading("id", text=f"COD {icon}", command=lambda: self.ordenar_id())
            self.sort_id = not self.sort_id
            conn.close()
        except Exception as e:
            self.show_message(f"Erro ao ordenar: {str(e)}", "error")

    def ordenar_nome(self):
        """Ordena por Nome"""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            order = "ASC" if self.sort_nome else "DESC"
            cursor.execute(f"SELECT id_tiponf, nm_tiponf FROM tiponf ORDER BY nm_tiponf {order}")
            
            self.tree.delete(*self.tree.get_children())
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            
            icon = "↑" if self.sort_nome else "↓"
            self.tree.heading("nome", text=f"Nome {icon}", command=lambda: self.ordenar_nome())
            self.sort_nome = not self.sort_nome
            conn.close()
        except Exception as e:
            self.show_message(f"Erro ao ordenar: {str(e)}", "error")
