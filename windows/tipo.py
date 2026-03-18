import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
import sqlite3
from windows.base_window import BaseWindow

class TipoWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.set_title("Cadastro de Tipos de Clientes")
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
        self.create_tooltip(self.btn_remover, "Remover")

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

        ttkb.Label(input_frame, text="COD").grid(row=0, column=0, sticky=tk.W)
        self.entry_id = ttkb.Entry(input_frame, width=10)
        self.entry_id.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Descrição").grid(row=0, column=2, sticky=tk.W)
        self.entry_nome = ttkb.Entry(input_frame, width=50)
        self.entry_nome.grid(row=0, column=3, pady=5, padx=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id_tipo", "nm_tipo"), show="headings", height=15)
            
        # Configuração das colunas - ID menor, Descrição maior
        self.tree.heading("id_tipo", text="COD")
        self.tree.heading("nm_tipo", text="Descrição")
        self.tree.column("id_tipo", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("nm_tipo", width=500, minwidth=300, anchor=tk.W)
            
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

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar()
        self.entry_id.focus()
        self.show_message("Pronto para novo registro", "info")

    def _execute_save(self):
        id_tipo = int(self.entry_id.get())
        nome = self.entry_nome.get()

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            if self.current_id is None:
                # INSERT operation - use comprehensive recnum handling
                insert_query = "INSERT INTO tipo (recnum, id_tipo, nm_tipo) VALUES (?, ?, ?)"
                params = (None, id_tipo, nome)  # recnum will be set by utility method

                success, next_recnum, error_msg = self.execute_insert_with_recnum_handling(
                    "tipo", insert_query, params, f"tipo '{nome}'"
                )

                if not success:
                    self.show_message(f"Erro ao salvar tipo: {error_msg}", "error")
                    return

                self.set_current_recnum(next_recnum)
                self.current_id = id_tipo
                self.log_recnum_operation("INSERT", "tipo", next_recnum, True)
                self.show_message("Registro inserido com sucesso!", "success")
            else:
                # UPDATE operation - use existing recnum
                cursor.execute("UPDATE tipo SET nm_tipo = ? WHERE id_tipo = ?", (nome, self.current_id))
                self.show_message("Registro atualizado com sucesso!", "success")

            conn.commit()
            self.limpar()
            self.carregar()

        except sqlite3.IntegrityError as e:
            self.show_message(f"Erro de integridade: {str(e)}", "error")
        except Exception as e:
            self.show_message(f"Erro ao salvar: {str(e)}", "error")
        finally:
            conn.close()

    def salvar(self):
        id_tipo = self.entry_id.get()
        nome = self.entry_nome.get()

        if not id_tipo or not nome:
            self.show_message("Preencha todos os campos", "warning")
            return

        try:
            id_tipo = int(id_tipo)
        except ValueError:
            self.show_message("ID deve ser um número", "error")
            return

        confirmation_message = f"Confirma a gravação do tipo '{nome}'?"
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('save')

        if not self.request_confirmation('save', confirmation_message, self._execute_save):
            return

    def remover(self):
        item = self.tree.focus()
        if not item:
            self.show_message("Selecione um registro para remover", "warning")
            return
            
        values = self.tree.item(item)["values"]
        id_tipo = values[0]
        nome_tipo = values[1]
        
        confirmation_message = f"Pressione 'Remover' novamente para excluir o tipo '{nome_tipo}'."
        
        # Setup confirmation pattern if not already done
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('remove')
        
        # Request confirmation using the new pattern
        if not self.request_confirmation('remove', confirmation_message, self._execute_removal, id_tipo, nome_tipo):
            return  # Waiting for confirmation

    def _execute_removal(self, id_tipo, nome_tipo):
        """Execute the actual removal after confirmation."""
        conn = self.conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM tipo WHERE id_tipo = ?", (id_tipo,))
            conn.commit()
            self.show_message("Registro removido com sucesso!", "success")
            self.carregar()
            self.limpar()
        except Exception as e:
            self.show_message(f"Erro ao remover: {str(e)}", "error")
        finally:
            conn.close()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_tipo, nm_tipo FROM tipo ORDER BY id_tipo")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()
        self.show_message("Dados carregados", "info")

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item or not item["values"]:
            return
        id_tipo, nome = item["values"]
        
        # Load record data into form fields
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, id_tipo)
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, nome)
        
        # Set current record state - get recnum from database
        self.current_id = id_tipo
        
        # Retrieve recnum for the selected record
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT recnum FROM tipo WHERE id_tipo = ?", (id_tipo,))
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
            
        self.show_message(f"Registro selecionado: {nome}", "info")

    def limpar(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        # Clear record state including recnum
        self.clear_record_state()
        self.show_message("Campos limpos", "info")

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
