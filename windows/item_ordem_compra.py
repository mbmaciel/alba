import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class ItemOrdemCompraWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Itens da Ordem de Compra (alba0011)")
        self.config(width=1100, height=650)
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
        ttkb.Label(input_frame, text="ID OC").grid(row=0, column=0, sticky=tk.W)
        self.entry_id_oc = ttkb.Entry(input_frame, width=10)
        self.entry_id_oc.grid(row=0, column=1, padx=5, pady=5)

        ttkb.Label(input_frame, text="Produto").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.combo_produto = ttkb.Combobox(input_frame, width=35, state="readonly")
        self.combo_produto.grid(row=0, column=3, padx=5, pady=5)

        ttkb.Label(input_frame, text="Qtde").grid(row=0, column=4, sticky=tk.W, padx=(20, 0))
        self.entry_qtd = ttkb.Entry(input_frame, width=10)
        self.entry_qtd.grid(row=0, column=5, padx=5, pady=5)
        self.entry_qtd.bind('<KeyRelease>', self.calcular_total_auto)

        # Segunda linha
        ttkb.Label(input_frame, text="Valor Unit.").grid(row=1, column=0, sticky=tk.W)
        self.entry_unit = ttkb.Entry(input_frame, width=12)
        self.entry_unit.grid(row=1, column=1, padx=5, pady=5)
        self.entry_unit.bind('<KeyRelease>', self.calcular_total_auto)

        ttkb.Label(input_frame, text="Desc. %").grid(row=1, column=2, sticky=tk.W, padx=(20, 0))
        self.entry_desc = ttkb.Entry(input_frame, width=10)
        self.entry_desc.grid(row=1, column=3, padx=5, pady=5)
        self.entry_desc.bind('<KeyRelease>', self.calcular_total_auto)

        ttkb.Label(input_frame, text="Total").grid(row=1, column=4, sticky=tk.W, padx=(20, 0))
        self.entry_total = ttkb.Entry(input_frame, width=15, state="readonly")
        self.entry_total.grid(row=1, column=5, padx=5, pady=5)

        # Terceira linha - Observações
        ttkb.Label(input_frame, text="Observações").grid(row=2, column=0, sticky=tk.W)
        self.entry_obs = ttkb.Entry(input_frame, width=80)
        self.entry_obs.grid(row=2, column=1, columnspan=5, padx=5, pady=5, sticky=tk.W+tk.E)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "oc", "produto", "qtde", "unit", "desc", "total"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="COD")
        self.tree.heading("oc", text="OC")
        self.tree.heading("produto", text="Produto")
        self.tree.heading("qtde", text="Qtde")
        self.tree.heading("unit", text="Valor Unit.")
        self.tree.heading("desc", text="Desc. %")
        self.tree.heading("total", text="Total")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("oc", width=60, minwidth=50, anchor=tk.CENTER)
        self.tree.column("produto", width=300, minwidth=200, anchor=tk.W)
        self.tree.column("qtde", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("unit", width=100, minwidth=80, anchor=tk.E)
        self.tree.column("desc", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("total", width=120, minwidth=100, anchor=tk.E)
        
        # Scrollbar para o Treeview
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)


        self.carregar_produtos()
        self.carregar()

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
        self.current_id = None
        self.current_recnum = None
        self.entry_id_oc.focus()
        self.show_message("Pronto para novo item", "info")

    def carregar_produtos(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_produto, nm_produto FROM alba0005 ORDER BY nm_produto")
        self.produtos = cursor.fetchall()
        conn.close()
        self.combo_produto["values"] = [nome for _, nome in self.produtos]

    def calcular_total_auto(self, event=None):
        """Calcula o total automaticamente quando os campos são alterados"""
        try:
            qtd = float(self.entry_qtd.get()) if self.entry_qtd.get() else 0
            valor = float(self.entry_unit.get()) if self.entry_unit.get() else 0
            desc = float(self.entry_desc.get()) if self.entry_desc.get() else 0
            
            total = qtd * valor * (1 - desc / 100)
            
            # Atualizar campo total
            self.entry_total.config(state="normal")
            self.entry_total.delete(0, tk.END)
            self.entry_total.insert(0, f"{total:.2f}")
            self.entry_total.config(state="readonly")
            
        except ValueError:
            # Se houver erro na conversão, limpar o campo total
            self.entry_total.config(state="normal")
            self.entry_total.delete(0, tk.END)
            self.entry_total.config(state="readonly")

    def calcular_total(self):
        try:
            qt = float(self.entry_qtd.get()) if self.entry_qtd.get() else 0
            valor = float(self.entry_unit.get()) if self.entry_unit.get() else 0
            desc = float(self.entry_desc.get()) if self.entry_desc.get() else 0
            total = qt * valor * (1 - desc / 100)
            return round(total, 2)
        except:
            return 0.0

    def _execute_save(self):
        id_oc = self.entry_id_oc.get()
        produto_nome = self.combo_produto.get()
        qtd = self.entry_qtd.get()
        unit = self.entry_unit.get()
        desc = self.entry_desc.get()
        obs = self.entry_obs.get()

        id_produto = next((id for id, nome in self.produtos if nome == produto_nome), None)
        total = self.calcular_total()

        conn = self.conectar()
        cursor = conn.cursor()
        try:
            if self.current_id is None:
                # INSERT - get next recnum using BaseWindow utility method
                next_recnum = self.get_next_recnum("alba0011")
                if next_recnum is None:
                    return  # Error message already shown by get_next_recnum

                # Get next id_item (primary key)
                cursor.execute("SELECT COALESCE(MAX(id_item), 0) + 1 FROM alba0011")
                next_id_item = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO alba0011 (
                        recnum, id_item, id_oc, id_produto, cd_cliente, qt_produto, vl_unitario,
                        pc_desc_coml, pc_desc_fiscal, vl_unit_final, vl_produto,
                        pc_ipi, vl_ipi, pc_icms, vl_icms, pc_icmsst, vl_icmsst,
                        vl_total, pc_comissao, vl_comissao, fl_status, tx_obs, fl_comissao
                    ) VALUES (?, ?, ?, ?, '', ?, ?, ?, 0, ?, ?, 0, 0, 0, 0, 0, 0, ?, 0, 0, 'ATIVO', ?, 'S')
                """, (
                    next_recnum, next_id_item, id_oc, id_produto, float(qtd), float(unit), float(desc or 0),
                    total, total, total, obs
                ))

                # Update current state
                self.current_id = next_id_item
                self.current_recnum = next_recnum
                self.show_message("Item salvo com sucesso!", "success")
            else:
                # UPDATE - use existing recnum
                cursor.execute("""
                    UPDATE alba0011 SET
                        id_oc = ?, id_produto = ?, qt_produto = ?, vl_unitario = ?,
                        pc_desc_coml = ?, vl_unit_final = ?, vl_produto = ?, tx_obs = ?
                    WHERE id_item = ?
                """, (id_oc, id_produto, float(qtd), float(unit), float(desc or 0), total, total, obs, self.current_id))
                self.show_message("Item atualizado com sucesso!", "success")

            conn.commit()
            self.carregar()
        except Exception as e:
            self.show_message(f"Erro ao salvar item: {str(e)}", "error")
        finally:
            conn.close()

    def salvar(self):
        id_oc = self.entry_id_oc.get()
        produto_nome = self.combo_produto.get()
        qtd = self.entry_qtd.get()
        unit = self.entry_unit.get()
        desc = self.entry_desc.get()
        obs = self.entry_obs.get()

        # Validações
        if not id_oc:
            self.show_message("ID da Ordem de Compra é obrigatório", "warning")
            return

        if not produto_nome:
            self.show_message("Selecione um produto", "warning")
            return

        if not qtd or not unit:
            self.show_message("Quantidade e Valor Unitário são obrigatórios", "warning")
            return

        try:
            qtd = float(qtd)
            unit = float(unit)
            desc = float(desc) if desc else 0
        except ValueError:
            self.show_message("Valores numéricos inválidos", "error")
            return

        id_produto = next((id for id, nome in self.produtos if nome == produto_nome), None)
        if not id_produto:
            self.show_message("Produto não encontrado", "error")
            return

        confirmation_message = f"Confirma a gravação do item '{produto_nome}'?"
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('save')

        if not self.request_confirmation('save', confirmation_message, self._execute_save):
            return

    def remover(self):
        item = self.tree.focus()
        if not item:
            self.show_message("Selecione um item para remover", "warning")
            return
            
        id_item = self.tree.item(item)["values"][0]
        produto_nome = self.tree.item(item)["values"][2]

        # Use two-step confirmation pattern instead of messagebox
        confirmation_message = f"Pressione 'Remover' novamente para excluir o item '{produto_nome}'."
        
        # Setup confirmation pattern if not already done
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('remove')
        
        # Request confirmation using the new pattern
        if not self.request_confirmation('remove', confirmation_message, self._execute_removal, id_item):
            return  # Waiting for confirmation

    def _execute_removal(self, id_item):
        """Execute the actual removal after confirmation."""
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM alba0011 WHERE id_item = ?", (id_item,))
            conn.commit()
            self.show_message("Item removido com sucesso!", "success")
            self.carregar()
            self.limpar()
        except Exception as e:
            self.show_message(f"Erro ao remover item: {str(e)}", "error")
        finally:
            conn.close()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.id_item, i.id_oc, p.nm_produto, i.qt_produto, 
                   i.vl_unitario, i.pc_desc_coml, i.vl_total
            FROM alba0011 i
            LEFT JOIN alba0005 p ON i.id_produto = p.id_produto
            ORDER BY i.id_oc, p.nm_produto
        """)
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()
        self.show_message("Dados carregados", "info")

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        
        values = item["values"]
        if len(values) >= 7:
            id_item, id_oc, nome_produto, qtd, unit, desc, total = values
            
            # Buscar observações e recnum do item
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT tx_obs, recnum FROM alba0011 WHERE id_item = ?", (id_item,))
            result = cursor.fetchone()
            obs = result[0] if result and result[0] else ""
            recnum = result[1] if result and result[1] else None
            conn.close()
            
            # Update current state with proper recnum synchronization
            self.current_id = id_item
            self.current_recnum = recnum
            
            # Preencher campos
            self.entry_id_oc.delete(0, tk.END)
            self.entry_id_oc.insert(0, str(id_oc))
            
            self.combo_produto.set(nome_produto or "")
            
            self.entry_qtd.delete(0, tk.END)
            self.entry_qtd.insert(0, str(qtd) if qtd else "")
            
            self.entry_unit.delete(0, tk.END)
            self.entry_unit.insert(0, str(unit) if unit else "")
            
            self.entry_desc.delete(0, tk.END)
            self.entry_desc.insert(0, str(desc) if desc else "")
            
            self.entry_total.config(state="normal")
            self.entry_total.delete(0, tk.END)
            self.entry_total.insert(0, str(total) if total else "")
            self.entry_total.config(state="readonly")
            
            self.entry_obs.delete(0, tk.END)
            self.entry_obs.insert(0, obs)
            
            self.show_message(f"Item selecionado: {nome_produto}", "info")

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.current_id = None
        self.current_recnum = None
        self.entry_id_oc.delete(0, tk.END)
        self.combo_produto.set("")
        self.entry_qtd.delete(0, tk.END)
        self.entry_unit.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.entry_total.config(state="normal")
        self.entry_total.delete(0, tk.END)
        self.entry_total.config(state="readonly")
        self.entry_obs.delete(0, tk.END)
        self.show_message("Campos limpos", "info")

    # Métodos de navegação (implementação básica)
    def ir_primeiro(self):
        children = self.tree.get_children()
        if children:
            self.tree.selection_set(children[0])
            self.tree.focus(children[0])
            self.tree.see(children[0])
            # Simular evento de seleção
            event = type('Event', (), {})()
            self.on_select(event)
            self.show_message("Primeiro registro", "info")

    def ir_anterior(self):
        current = self.tree.focus()
        if current:
            children = self.tree.get_children()
            try:
                current_index = children.index(current)
                if current_index > 0:
                    prev_item = children[current_index - 1]
                    self.tree.selection_set(prev_item)
                    self.tree.focus(prev_item)
                    self.tree.see(prev_item)
                    # Simular evento de seleção
                    event = type('Event', (), {})()
                    self.on_select(event)
                    self.show_message("Registro anterior", "info")
                else:
                    self.show_message("Já está no primeiro registro", "warning")
            except ValueError:
                pass

    def ir_proximo(self):
        current = self.tree.focus()
        if current:
            children = self.tree.get_children()
            try:
                current_index = children.index(current)
                if current_index < len(children) - 1:
                    next_item = children[current_index + 1]
                    self.tree.selection_set(next_item)
                    self.tree.focus(next_item)
                    self.tree.see(next_item)
                    # Simular evento de seleção
                    event = type('Event', (), {})()
                    self.on_select(event)
                    self.show_message("Próximo registro", "info")
                else:
                    self.show_message("Já está no último registro", "warning")
            except ValueError:
                pass

    def ir_ultimo(self):
        children = self.tree.get_children()
        if children:
            last_item = children[-1]
            self.tree.selection_set(last_item)
            self.tree.focus(last_item)
            self.tree.see(last_item)
            # Simular evento de seleção
            event = type('Event', (), {})()
            self.on_select(event)
            self.show_message("Último registro", "info")
