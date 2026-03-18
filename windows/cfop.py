import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow

class CfopWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Cadastro de CFOP")
        self.config(width=1200, height=600)

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

        # Separador visual
        separator2 = ttkb.Separator(toolbar_frame, orient=tk.VERTICAL)
        separator2.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

        # Container para busca
        search_container = ttkb.Frame(toolbar_frame)
        search_container.pack(side=tk.LEFT, padx=(10, 0))

        self.entry_busca = ttkb.Entry(search_container, width=30)
        self.entry_busca.pack(side=tk.LEFT, padx=(0, 5))

        btn_buscar = ttkb.Button(search_container, text="🔍", command=self.buscar, width=3)
        btn_buscar.pack(side=tk.LEFT)
        self.create_tooltip(btn_buscar, "Buscar")
        
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

        # Primeira linha
        ttkb.Label(input_frame, text="Código CFOP").grid(row=0, column=0, sticky=tk.W)
        self.entry_codigo = ttkb.Entry(input_frame, width=15)
        self.entry_codigo.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Descrição").grid(row=0, column=2, sticky=tk.W+tk.N)
        self.entry_descricao = tk.Text(input_frame, width=50, height=3, wrap=tk.WORD)
        self.entry_descricao.grid(row=0, column=3, pady=5, padx=5, sticky=tk.W+tk.E)



        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("codigo", "descricao"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("codigo", text="Código")
        self.tree.heading("descricao", text="Descrição")
        
        self.tree.column("codigo", width=150, minwidth=120, anchor=tk.CENTER)
        self.tree.column("descricao", width=800, minwidth=600, anchor=tk.W)
        
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
        self.limpar()
        self.entry_codigo.focus()

    def salvar(self):
        codigo = self.entry_codigo.get().strip()
        descricao = self.entry_descricao.get("1.0", tk.END).strip()

        if not codigo or not descricao:
            self.show_message("Código e descrição são obrigatórios.", msg_type="warning")
            return

        confirmation_message = f"Confirma a gravação do CFOP '{codigo}'?"
        
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('save')
        
        if not self.request_confirmation('save', confirmation_message, self._execute_save):
            return

    def _execute_save(self):
        codigo = self.entry_codigo.get().strip()
        descricao = self.entry_descricao.get("1.0", tk.END).strip()

        conn = self.conectar()
        cursor = conn.cursor()
        try:
            # Verificar se o registro já existe
            cursor.execute("SELECT recnum FROM cfop WHERE cd_cfop = ?", (codigo,))
            registro_existente = cursor.fetchone()
            
            is_update = registro_existente is not None
            
            if is_update:
                # Atualizar registro existente
                cursor.execute("""UPDATE cfop 
                                SET nm_cfop = ? 
                                WHERE cd_cfop = ?""",
                             (descricao, codigo))
                self.show_message("CFOP atualizado com sucesso!", msg_type="success")
            else:
                # Obter o próximo recnum
                cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM cfop")
                proximo_recnum = cursor.fetchone()[0]
                
                # Inserir novo registro
                cursor.execute("""INSERT INTO cfop (recnum, cd_cfop, nm_cfop) 
                                VALUES (?, ?, ?)""",
                             (proximo_recnum, codigo, descricao))
                self.show_message("CFOP salvo com sucesso!", msg_type="success")
            
            conn.commit()
        except Exception as e:
            self.show_message(f"Erro ao salvar: {str(e)}", msg_type="danger")
            return
        finally:
            conn.close()

        # Recarregar a lista
        self.carregar()
        
        # Se foi uma inserção, limpar os campos
        # Se foi uma atualização, manter o registro selecionado
        if not is_update:
            self.limpar()
        else:
            # Reselecionar o item atualizado na lista
            self.selecionar_item_por_codigo(codigo)

    def selecionar_item_por_codigo(self, codigo):
        """Seleciona um item na lista pelo código CFOP"""
        for item in self.tree.get_children():
            valores = self.tree.item(item)["values"]
            if valores and str(valores[0]) == str(codigo):
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)
                break

    def _execute_removal(self, codigo, descricao):
        """Executa a remoção do registro."""
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM cfop WHERE cd_cfop = ?", (codigo,))
            conn.commit()
            self.show_message(f"CFOP '{codigo} - {descricao}' removido com sucesso!", msg_type="success")
        except Exception as e:
            self.show_message(f"Erro ao remover: {str(e)}", msg_type="danger")
        finally:
            conn.close()

        self.carregar()
        self.limpar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            self.show_message("Selecione um CFOP para remover.", msg_type="warning")
            return
            
        codigo, descricao = self.tree.item(item)["values"]
        
        confirmation_message = f"Pressione 'Remover' novamente para excluir o CFOP '{codigo} - {descricao}'."
        
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('remove')
        
        if not self.request_confirmation('remove', confirmation_message, self._execute_removal, codigo, descricao):
            return

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT cd_cfop, nm_cfop FROM cfop ORDER BY cd_cfop")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        codigo, descricao = item["values"]
        
        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, codigo or "")
        
        self.entry_descricao.delete("1.0", tk.END)
        self.entry_descricao.insert("1.0", descricao or "")

    def buscar(self):
        """Realiza a busca com base no texto inserido"""
        termo = self.entry_busca.get().strip().lower()
        self.tree.selection_remove(*self.tree.selection())

        if not termo:
            return

        for item in self.tree.get_children():
            valores = self.tree.item(item)["values"]
            if any(str(valor).lower().find(termo) >= 0 for valor in valores):
                self.tree.selection_add(item)
                self.tree.focus(item)
                self.tree.see(item)
                break

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.entry_codigo.delete(0, tk.END)
        self.entry_descricao.delete("1.0", tk.END)
        
