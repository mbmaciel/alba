import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class NcmWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Consulta de NCM")
        self.config(width=700, height=500)
        
        # Initialize record state management
        self.current_id = None
        self.current_recnum = None
        
        # Variável para controlar se estamos editando um registro existente
        self.editing_record = None

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

        btn_buscar = ttkb.Button(search_container, text="🔍", command=self.buscar_ncm, width=3)
        btn_buscar.pack(side=tk.LEFT)
        self.create_tooltip(btn_buscar, "Buscar NCM")
        
        btn_recarregar = ttkb.Button(search_container, text="🔄", command=self.carregar, width=3)
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

        ttkb.Label(input_frame, text="Código NCM").grid(row=0, column=0, sticky=tk.W)
        self.entry_codigo = ttkb.Entry(input_frame, width=15)
        self.entry_codigo.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Descrição").grid(row=0, column=2, sticky=tk.W)
        self.entry_descricao = ttkb.Entry(input_frame, width=60)
        self.entry_descricao.grid(row=0, column=3, pady=5, padx=5)

        # Frame para busca
        search_frame = ttkb.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 15))

        ttkb.Label(search_frame, text="Buscar código NCM").grid(row=0, column=0, sticky=tk.W)
        self.entry_busca = ttkb.Entry(search_frame, width=30)
        self.entry_busca.grid(row=0, column=1, pady=5, padx=(5, 10))
        self.entry_busca.bind("<Return>", lambda e: self.buscar_ncm())

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("codigo", "descricao"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("codigo", text="Código")
        self.tree.heading("descricao", text="Descrição")
        self.tree.column("codigo", width=120, minwidth=100, anchor=tk.CENTER)
        self.tree.column("descricao", width=500, minwidth=300, anchor=tk.W)
        
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
        self.clear_record_state()
        self.editing_record = None  # Reset do controle de edição
        self.limpar()
        self.entry_codigo.focus()
        self.show_message("Campos limpos. Digite os dados do novo NCM.", "info")

    def _execute_save(self):
        codigo = self.entry_codigo.get()
        descricao = self.entry_descricao.get()
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            if self.editing_record:
                # Estamos editando um registro existente
                # Verifica se o código foi alterado e se já existe outro registro com o novo código
                if codigo != self.editing_record:
                    cursor.execute("SELECT COUNT(*) FROM ncm WHERE cd_ncm = ?", (codigo,))
                    existe = cursor.fetchone()[0]
                    if existe:
                        self.show_message(f"ERRO: Já existe um registro com o código NCM '{codigo}'.", "error")
                        conn.close()
                        return

                # Atualiza o registro existente
                cursor.execute("UPDATE ncm SET cd_ncm = ?, nm_ncm = ? WHERE cd_ncm = ?",
                               (codigo, descricao, self.editing_record))
                self.show_message(f"NCM '{codigo}' atualizado com sucesso!", "success")
            else:
                # Novo registro - use consistent recnum pattern
                cursor.execute("SELECT COUNT(*) FROM ncm WHERE cd_ncm = ?", (codigo,))
                existe = cursor.fetchone()[0]

                if existe:
                    self.show_message(f"ERRO: Já existe um registro com o código NCM '{codigo}'.", "error")
                    conn.close()
                    return

                # Get next recnum using BaseWindow utility method
                next_recnum = self.get_next_recnum("ncm")
                if next_recnum is None:
                    conn.close()
                    return

                cursor.execute("INSERT INTO ncm (recnum, cd_ncm, nm_ncm) VALUES (?, ?, ?)",
                               (next_recnum, codigo, descricao))

                # Set current recnum for the new record
                self.set_current_recnum(next_recnum)
                self.show_message(f"NCM '{codigo}' salvo com sucesso!", "success")

            conn.commit()
            self.clear_record_state()
            self.editing_record = None  # Reset do controle de edição
            self.limpar()
            self.carregar()

        except sqlite3.IntegrityError as e:
            conn.rollback()
            if "UNIQUE constraint failed" in str(e):
                self.show_message("ERRO: Já existe um NCM com estes dados.", "error")
            else:
                self.show_message(f"ERRO de integridade: {str(e)}", "error")
        except sqlite3.Error as e:
            conn.rollback()
            self.show_message(f"ERRO ao salvar NCM: {str(e)}", "error")
        finally:
            conn.close()

    def salvar(self):
        codigo = self.entry_codigo.get()
        descricao = self.entry_descricao.get()

        if not codigo or not descricao:
            self.show_message("ATENÇÃO: Preencha todos os campos obrigatórios.", "warning")
            return

        confirmation_message = f"Confirma a gravação do NCM '{codigo}'?"
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('save')

        if not self.request_confirmation('save', confirmation_message, self._execute_save):
            return

    def _execute_removal(self, codigo):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ncm WHERE cd_ncm = ?", (codigo,))
            conn.commit()
            conn.close()
            self.editing_record = None  # Reset do controle de edição
            self.limpar()
            self.carregar()
            self.show_message(f"NCM '{codigo}' removido com sucesso!", "success")
        except sqlite3.Error as e:
            self.show_message(f"ERRO ao remover NCM: {str(e)}", "error")

    def remover(self):
        item = self.tree.focus()
        if not item:
            self.show_message("ATENÇÃO: Selecione um registro para remover.", "warning")
            return

        item_data = self.tree.item(item)
        if not item_data.get("values"):
            self.show_message("ATENÇÃO: Selecione um registro válido para remover.", "warning")
            return

        codigo, descricao = item_data["values"]

        confirmation_message = f"Pressione 'Remover' novamente para excluir o NCM '{codigo} - {descricao}'."

        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('remove')

        if not self.request_confirmation('remove', confirmation_message, self._execute_removal, codigo):
            return

    def buscar_ncm(self):
        codigo = self.entry_busca.get()
        if not codigo:
            self.carregar()
            self.show_message("Busca limpa. Mostrando todos os NCMs.", "info")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT cd_ncm, nm_ncm FROM ncm WHERE cd_ncm LIKE ? OR nm_ncm LIKE ? ORDER BY cd_ncm", 
                      (f"%{codigo}%", f"%{codigo}%"))
        resultados = cursor.fetchall()
        conn.close()

        self.tree.delete(*self.tree.get_children())
        for row in resultados:
            self.tree.insert("", "end", values=row)
            
        if resultados:
            self.show_message(f"Encontrados {len(resultados)} NCM(s) com '{codigo}'", "success")
        else:
            self.show_message(f"Nenhum NCM encontrado com '{codigo}'", "warning")

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT cd_ncm, nm_ncm FROM ncm ORDER BY cd_ncm")
            resultados = cursor.fetchall()
            for row in resultados:
                self.tree.insert("", "end", values=row)
            conn.close()
            self.show_message(f"Carregados {len(resultados)} NCMs", "success")
        except sqlite3.Error as e:
            self.show_message(f"ERRO ao carregar NCMs: {str(e)}", "error")

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item or not item.get("values"):
            return
            
        codigo, descricao = item["values"]
        
        # Get the recnum for the selected record from database
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT recnum FROM ncm WHERE cd_ncm = ?", (codigo,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                self.set_current_recnum(result[0])
            else:
                self.set_current_recnum(None)
                
        except sqlite3.Error as e:
            self.show_message(f"ERRO ao obter recnum: {str(e)}", "error")
            self.set_current_recnum(None)
        
        # Armazena o código original para controle de edição
        self.editing_record = codigo
        
        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, codigo)
        self.entry_descricao.delete(0, tk.END)
        self.entry_descricao.insert(0, descricao)
        self.show_message(f"NCM selecionado: {codigo}", "info")

    def limpar(self):
        self.entry_codigo.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_busca.delete(0, tk.END)
        self.clear_record_state()
        self.editing_record = None

    # Métodos de navegação (podem ser implementados posteriormente)
    def ir_primeiro(self):
        items = self.tree.get_children()
        if items:
            self.tree.selection_set(items[0])
            self.tree.focus(items[0])
            self.on_select(None)
            self.show_message("Primeiro registro selecionado", "info")

    def ir_anterior(self):
        current = self.tree.focus()
        if current:
            prev_item = self.tree.prev(current)
            if prev_item:
                self.tree.selection_set(prev_item)
                self.tree.focus(prev_item)
                self.on_select(None)
                self.show_message("Registro anterior selecionado", "info")

    def ir_proximo(self):
        current = self.tree.focus()
        if current:
            next_item = self.tree.next(current)
            if next_item:
                self.tree.selection_set(next_item)
                self.tree.focus(next_item)
                self.on_select(None)
                self.show_message("Próximo registro selecionado", "info")

    def ir_ultimo(self):
        items = self.tree.get_children()
        if items:
            self.tree.selection_set(items[-1])
            self.tree.focus(items[-1])
            self.on_select(None)
            self.show_message("Último registro selecionado", "info")
