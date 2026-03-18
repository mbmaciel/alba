import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow

class AtividWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Cadastro de Atividades")
        self.config(width=700, height=500)
        self.current_id = None
        self.editing_record = None  # Para controlar se estamos editando um registro existente

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

        ttkb.Label(input_frame, text="Descrição da Atividade").grid(row=0, column=0, sticky=tk.W)
        self.entry_desc = ttkb.Entry(input_frame, width=60)
        self.entry_desc.grid(row=0, column=1, pady=5, padx=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "descricao"), show="headings", height=15)

        # Configuração das colunas com ordenação
        self.sort_id = True  # True = crescente, False = decrescente
        self.sort_desc = True
        
        self.tree.heading("id", text="COD ↕", command=lambda: self.ordenar_id())
        self.tree.heading("descricao", text="Descrição ↕", command=lambda: self.ordenar_desc())

        # Make ID column visible
        self.tree.column("id", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("descricao", width=500, minwidth=400, anchor=tk.W)

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
        self.current_id = None
        self.editing_record = None
        self.limpar()
        self.entry_desc.focus()
        self.show_message("Campos limpos. Digite a descrição da nova atividade.", "info")

    def _execute_save(self):
        desc = self.entry_desc.get()
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            if self.current_id is not None:
                # Estamos editando um registro existente
                # Verifica se a descrição foi alterada e se já existe outra atividade com a nova descrição
                if desc != self.editing_record:
                    cursor.execute("SELECT id_atividade FROM ativid WHERE nm_atividade = ?", (desc,))
                    row = cursor.fetchone()
                    if row:
                        self.show_message(f"ERRO: Já existe uma atividade com a descrição '{desc}'.", "error")
                        conn.close()
                        return

                # Atualiza o registro existente usando o ID armazenado
                cursor.execute("UPDATE ativid SET nm_atividade = ? WHERE id_atividade = ?",
                               (desc, self.current_id))
                self.show_message(f"Atividade '{desc}' atualizada com sucesso!", "success")
            else:
                # Novo registro
                cursor.execute("SELECT id_atividade FROM ativid WHERE nm_atividade = ?", (desc,))
                row = cursor.fetchone()

                if row:
                    self.show_message(f"ERRO: Já existe uma atividade com a descrição '{desc}'.", "error")
                    conn.close()
                    return

                # Insere novo registro usando utility method
                next_recnum = self.get_next_recnum("ativid")
                if next_recnum is None:
                    conn.close()
                    return

                # Obter o próximo id_atividade manualmente
                cursor.execute("SELECT COALESCE(MAX(id_atividade), 0) + 1 FROM ativid")
                next_id_atividade = cursor.fetchone()[0]

                cursor.execute("INSERT INTO ativid (recnum, id_atividade, nm_atividade) VALUES (?, ?, ?)", (next_recnum, next_id_atividade, desc))
                self.set_current_recnum(next_recnum)
                self.show_message(f"Atividade '{desc}' salva com sucesso!", "success")

            conn.commit()
            self.current_id = None
            self.editing_record = None
            self.limpar()
            self.carregar()

        except Exception as e:
            conn.rollback()
            self.show_message(f"ERRO ao salvar atividade: {str(e)}", "error")
        finally:
            conn.close()

    def salvar(self):
        desc = self.entry_desc.get()
        if not desc:
            self.show_message("ATENÇÃO: Descrição obrigatória.", "warning")
            return

        confirmation_message = f"Confirma a gravação da atividade '{desc}'?"
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('save')

        if not self.request_confirmation('save', confirmation_message, self._execute_save):
            return

    def _execute_removal(self, id_atividade, desc_atividade):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ativid WHERE id_atividade = ?", (id_atividade,))
            conn.commit()
            conn.close()
            self.carregar()
            self.limpar()
            self.show_message(f"Atividade '{desc_atividade}' removida com sucesso!", "success")
        except Exception as e:
            self.show_message(f"ERRO ao remover atividade: {str(e)}", "error")

    def remover(self):
        item = self.tree.focus()
        if not item:
            self.show_message("ATENÇÃO: Selecione uma atividade para remover.", "warning")
            return

        item_data = self.tree.item(item)
        if not item_data.get("values"):
            self.show_message("ATENÇÃO: Selecione um registro válido para remover.", "warning")
            return

        id_atividade, desc_atividade = item_data["values"]

        confirmation_message = f"Pressione 'Remover' novamente para excluir a atividade '{desc_atividade}'."

        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('remove')

        if not self.request_confirmation('remove', confirmation_message, self._execute_removal, id_atividade, desc_atividade):
            return

    def carregar(self):
        try:
            self.tree.delete(*self.tree.get_children())
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_atividade, nm_atividade FROM ativid ORDER BY nm_atividade")
            resultados = cursor.fetchall()
            for row in resultados:
                self.tree.insert("", "end", values=row)
            conn.close()
            self.show_message(f"Carregadas {len(resultados)} atividades", "success")
        except Exception as e:
            self.show_message(f"ERRO ao carregar dados: {str(e)}", "error")

    def on_select(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item)["values"]
        if values:
            self.current_id = values[0]  # Armazena o ID para edição
            self.editing_record = values[1]  # Armazena a descrição original
            
            # Synchronize recnum with database
            try:
                conn = self.conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT recnum FROM ativid WHERE id_atividade = ?", (self.current_id,))
                result = cursor.fetchone()
                if result:
                    self.set_current_recnum(result[0])
                conn.close()
            except Exception as e:
                self.show_message(f"Erro ao sincronizar recnum: {str(e)}", "error")
                if 'conn' in locals():
                    conn.close()
            
            self.entry_desc.delete(0, tk.END)
            self.entry_desc.insert(0, values[1])
            self.show_message(f"Atividade selecionada: {values[1]}", "info")

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.entry_desc.delete(0, tk.END)
        self.current_id = None
        self.editing_record = None

    def ir_primeiro(self):
        """Navega para o primeiro registro"""
        children = self.tree.get_children()
        if children:
            first_item = children[0]
            self.tree.selection_set(first_item)
            self.tree.focus(first_item)
            self.tree.see(first_item)
            self.on_select(None)
            self.show_message("Primeiro registro selecionado", "info")

    def ir_ultimo(self):
        """Navega para o último registro"""
        children = self.tree.get_children()
        if children:
            last_item = children[-1]
            self.tree.selection_set(last_item)
            self.tree.focus(last_item)
            self.tree.see(last_item)
            self.on_select(None)
            self.show_message("Último registro selecionado", "info")

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
            self.show_message("Registro anterior selecionado", "info")
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
            self.show_message("Próximo registro selecionado", "info")
        else:
            self.ir_primeiro()
    def ordenar_id(self):
        """Ordena por ID"""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            order = "ASC" if self.sort_id else "DESC"
            cursor.execute(f"SELECT id_atividade, nm_atividade FROM ativid ORDER BY CAST(id_atividade AS INTEGER) {order}")
            
            self.tree.delete(*self.tree.get_children())
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            
            icon = "↑" if self.sort_id else "↓"
            self.tree.heading("id", text=f"COD {icon}", command=lambda: self.ordenar_id())
            self.sort_id = not self.sort_id
            conn.close()
        except Exception as e:
            self.show_message(f"Erro ao ordenar: {str(e)}", "error")

    def ordenar_desc(self):
        """Ordena por Descrição"""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            order = "ASC" if self.sort_desc else "DESC"
            cursor.execute(f"SELECT id_atividade, nm_atividade FROM ativid ORDER BY nm_atividade {order}")
            
            self.tree.delete(*self.tree.get_children())
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            
            icon = "↑" if self.sort_desc else "↓"
            self.tree.heading("descricao", text=f"Descrição {icon}", command=lambda: self.ordenar_desc())
            self.sort_desc = not self.sort_desc
            conn.close()
        except Exception as e:
            self.show_message(f"Erro ao ordenar: {str(e)}", "error")
