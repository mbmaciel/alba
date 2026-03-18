import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class ComissaoWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_id = None  # Para controlar inserção/atualização
        aplicar_estilo(self)
        self.set_title("Cadastro de Faixas de Comissão")
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

        # Primeira linha
        ttkb.Label(input_frame, text="Desconto Inicial (%)").grid(row=0, column=0, sticky=tk.W)
        self.entry_ini = ttkb.Entry(input_frame, width=15)
        self.entry_ini.grid(row=0, column=1, padx=5, pady=5)

        ttkb.Label(input_frame, text="Desconto Final (%)").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.entry_fim = ttkb.Entry(input_frame, width=15)
        self.entry_fim.grid(row=0, column=3, padx=5, pady=5)

        ttkb.Label(input_frame, text="Comissão (%)").grid(row=0, column=4, sticky=tk.W, padx=(20, 0))
        self.entry_comissao = ttkb.Entry(input_frame, width=15)
        self.entry_comissao.grid(row=0, column=5, padx=5, pady=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "desc_ini", "desc_fim", "comissao"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="COD")
        self.tree.heading("desc_ini", text="Desconto Inicial (%)")
        self.tree.heading("desc_fim", text="Desconto Final (%)")
        self.tree.heading("comissao", text="Comissão (%)")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("desc_ini", width=200, minwidth=150, anchor=tk.CENTER)
        self.tree.column("desc_fim", width=200, minwidth=150, anchor=tk.CENTER)
        self.tree.column("comissao", width=200, minwidth=150, anchor=tk.CENTER)
        
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
        self.limpar()
        self.entry_ini.focus()
        self.show_message("Novo registro. Preencha os campos e salve.", "info")

    def _execute_save(self):
        try:
            ini = float(self.entry_ini.get())
            fim = float(self.entry_fim.get())
            comissao = float(self.entry_comissao.get())

            conn = self.conectar()
            cursor = conn.cursor()

            try:
                if self.current_id is None:
                    # Novo registro - INSERT
                    cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM comissao")
                    next_recnum = cursor.fetchone()[0]

                    cursor.execute("""
                        INSERT INTO comissao (recnum, pc_desc_ini, pc_desc_fim, pc_comissao)
                        VALUES (?, ?, ?, ?)
                    """, (next_recnum, ini, fim, comissao))
                    self.show_message(f"Faixa de comissão {ini}% - {fim}% incluída com sucesso!", "success")
                else:
                    # Atualização - UPDATE
                    cursor.execute("""
                        UPDATE comissao SET pc_desc_ini=?, pc_desc_fim=?, pc_comissao=?
                        WHERE id_comissao=?
                    """, (ini, fim, comissao, self.current_id))
                    self.show_message(f"Faixa de comissão {ini}% - {fim}% atualizada com sucesso!", "success")

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
            try:
                ini = float(self.entry_ini.get())
                fim = float(self.entry_fim.get())
                comissao = float(self.entry_comissao.get())
            except ValueError:
                self.show_message("Insira valores numéricos válidos.", "error")
                return

            if ini < 0 or fim < 0 or comissao < 0:
                self.show_message("Os valores devem ser positivos.", "warning")
                return

            if ini > fim:
                self.show_message("O desconto inicial deve ser menor ou igual ao desconto final.", "warning")
                return
            
            confirmation_message = f"Confirma a gravação da faixa de comissão de {ini}% a {fim}%?"
            if not hasattr(self, '_confirmations'):
                self.setup_confirmation_pattern('save')

            if not self.request_confirmation('save', confirmation_message, self._execute_save):
                return
                
        except Exception as e:
            self.show_message(f"Erro inesperado: {str(e)}", "error")

    def _execute_removal(self, id_comissao, desc_ini, desc_fim):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM comissao WHERE id_comissao = ?", (id_comissao,))
            conn.commit()
            conn.close()
            self.carregar()
            self.limpar()
            self.show_message(f"Faixa de comissão {desc_ini}% - {desc_fim}% removida com sucesso!", "success")
        except sqlite3.Error as e:
            self.show_message(f"Erro ao remover: {str(e)}", "error")

    def remover(self):
        try:
            item = self.tree.focus()
            if not item:
                self.show_message("Selecione uma faixa de comissão para remover.", "warning")
                return
            
            item_values = self.tree.item(item)["values"]
            id_comissao = item_values[0]
            desc_ini = item_values[1]
            desc_fim = item_values[2]
            
            confirmation_message = f"Pressione 'Remover' novamente para excluir a faixa {desc_ini}% - {desc_fim}%."

            if not hasattr(self, '_confirmations'):
                self.setup_confirmation_pattern('remove')

            if not self.request_confirmation('remove', confirmation_message, self._execute_removal, id_comissao, desc_ini, desc_fim):
                return

        except Exception as e:
            self.show_message(f"Erro inesperado: {str(e)}", "error")

    def carregar(self):
        try:
            self.tree.delete(*self.tree.get_children())
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_comissao, pc_desc_ini, pc_desc_fim, pc_comissao FROM comissao ORDER BY pc_desc_ini")
            resultados = cursor.fetchall()
            for row in resultados:
                self.tree.insert("", "end", values=row)
            conn.close()
            self.show_message(f"Carregadas {len(resultados)} faixas de comissão", "success")
        except sqlite3.Error as e:
            self.show_message(f"Erro ao carregar dados: {str(e)}", "error")

    def on_select(self, event):
        try:
            item = self.tree.item(self.tree.focus())
            if not item or not item.get("values"):
                return
            
            values = item["values"]
            if len(values) >= 4:
                id_comissao, ini, fim, comissao = values
                self.current_id = id_comissao  # Armazenar ID para edição
                
                self.entry_ini.delete(0, tk.END)
                self.entry_ini.insert(0, str(ini))
                self.entry_fim.delete(0, tk.END)
                self.entry_fim.insert(0, str(fim))
                self.entry_comissao.delete(0, tk.END)
                self.entry_comissao.insert(0, str(comissao))
                self.show_message(f"Faixa selecionada para edição: {ini}% - {fim}%", "info")
        except Exception as e:
            self.show_message(f"Erro ao selecionar: {str(e)}", "error")

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.current_id = None
        self.entry_ini.delete(0, tk.END)
        self.entry_fim.delete(0, tk.END)
        self.entry_comissao.delete(0, tk.END)

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
            self.show_message(f"Erro inesperado: {str(e)}", "error")
