import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class ItemNotaFiscalWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_id = None  # Para controlar inserção/atualização
        aplicar_estilo(self)
        self.set_title("Itens da Nota Fiscal")
        self.config(width=1200, height=650)

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
        ttkb.Label(input_frame, text="Nota Fiscal").grid(row=0, column=0, sticky=tk.W)
        self.combo_nota = ttkb.Combobox(input_frame, width=30, state="readonly")
        self.combo_nota.grid(row=0, column=1, padx=5, pady=5)

        ttkb.Label(input_frame, text="Quantidade").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.entry_qtde = ttkb.Entry(input_frame, width=12)
        self.entry_qtde.grid(row=0, column=3, padx=5, pady=5)

        ttkb.Label(input_frame, text="Valor Unitário").grid(row=0, column=4, sticky=tk.W, padx=(20, 0))
        self.entry_unit = ttkb.Entry(input_frame, width=12)
        self.entry_unit.grid(row=0, column=5, padx=5, pady=5)

        # Segunda linha
        ttkb.Label(input_frame, text="Produto").grid(row=1, column=0, sticky=tk.W)
        self.combo_produto = ttkb.Combobox(input_frame, width=30, state="readonly")
        self.combo_produto.grid(row=1, column=1, padx=5, pady=5)

        ttkb.Label(input_frame, text="Frete").grid(row=1, column=2, sticky=tk.W, padx=(20, 0))
        self.entry_frete = ttkb.Entry(input_frame, width=12)
        self.entry_frete.grid(row=1, column=3, padx=5, pady=5)

        ttkb.Label(input_frame, text="Total").grid(row=1, column=4, sticky=tk.W, padx=(20, 0))
        self.entry_total = ttkb.Entry(input_frame, width=12)
        self.entry_total.grid(row=1, column=5, padx=5, pady=5)

        # Terceira linha
        ttkb.Label(input_frame, text="CFOP").grid(row=2, column=0, sticky=tk.W)
        self.combo_cfop = ttkb.Combobox(input_frame, width=30, state="readonly")
        self.combo_cfop.grid(row=2, column=1, padx=5, pady=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id_item", "nota", "produto", "qtde", "cfop", "unit", "frete", "total"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id_item", text="COD")
        self.tree.heading("nota", text="Nota")
        self.tree.heading("produto", text="Produto")
        self.tree.heading("qtde", text="Qtde")
        self.tree.heading("cfop", text="CFOP")
        self.tree.heading("unit", text="Vl. Unit.")
        self.tree.heading("frete", text="Frete")
        self.tree.heading("total", text="Total")
        
        # Hide the id column
        self.tree.column("id_item", width=0, stretch=False)
        self.tree.column("nota", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("produto", width=200, minwidth=150, anchor=tk.W)
        self.tree.column("qtde", width=80, minwidth=60, anchor=tk.E)
        self.tree.column("cfop", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("unit", width=100, minwidth=80, anchor=tk.E)
        self.tree.column("frete", width=100, minwidth=80, anchor=tk.E)
        self.tree.column("total", width=100, minwidth=80, anchor=tk.E)
        
        # Scrollbar para o Treeview
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_notas()
        self.carregar_produtos()
        self.carregar_cfop()
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
        self.combo_nota.focus()
        self.show_message("Novo item. Preencha os campos e salve.", "info")

    def carregar_notas(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_nota, nr_nota FROM alba0012 ORDER BY id_nota")
            self.notas = cursor.fetchall()
            conn.close()
            self.combo_nota["values"] = [f"{n} - {num}" for n, num in self.notas]
        except Exception as e:
            self.show_message(f"Erro ao carregar notas: {str(e)}", "error")
            self.notas = []

    def carregar_produtos(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_produto, nm_produto FROM alba0005 ORDER BY nm_produto")
            self.produtos = cursor.fetchall()
            conn.close()
            self.combo_produto["values"] = [f"{p} - {nome}" for p, nome in self.produtos]
        except Exception as e:
            self.show_message(f"Erro ao carregar produtos: {str(e)}", "error")
            self.produtos = []

    def carregar_cfop(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT cd_cfop, nm_cfop FROM cfop ORDER BY cd_cfop")
            self.cfops = cursor.fetchall()
            conn.close()
            self.combo_cfop["values"] = [f"{c} - {desc}" for c, desc in self.cfops]
        except Exception as e:
            self.show_message(f"Erro ao carregar CFOPs: {str(e)}", "error")
            self.cfops = []

    def salvar(self):
        try:
            # Validações básicas
            if not self.combo_nota.get():
                self.show_message("Selecione uma nota fiscal.", "warning")
                return
            if not self.combo_produto.get():
                self.show_message("Selecione um produto.", "warning")
                return
            if not self.combo_cfop.get():
                self.show_message("Selecione um CFOP.", "warning")
                return

            id_nota = int(self.combo_nota.get().split(" - ")[0])
            id_produto = int(self.combo_produto.get().split(" - ")[0])
            cd_cfop = self.combo_cfop.get().split(" - ")[0]

            try:
                qtde = float(self.entry_qtde.get() or "0")
                unit = float(self.entry_unit.get() or "0")
                frete = float(self.entry_frete.get() or "0")
                total = float(self.entry_total.get() or "0")
            except ValueError:
                self.show_message("Insira valores numéricos válidos.", "error")
                return

            if qtde <= 0:
                self.show_message("A quantidade deve ser maior que zero.", "warning")
                return

            conn = self.conectar()
            cursor = conn.cursor()

            if self.current_id is None:
                # Novo registro - INSERT
                cursor.execute("""
                    INSERT INTO alba0013 (
                        id_nota, id_produto, qt_produto, cd_cfop, vl_unitario, vl_frete, vl_total
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (id_nota, id_produto, qtde, cd_cfop, unit, frete, total))
                self.show_message(f"Item incluído com sucesso!", "success")
            else:
                # Atualização - UPDATE
                cursor.execute("""
                    UPDATE alba0013 SET
                        id_nota=?, id_produto=?, qt_produto=?, cd_cfop=?, vl_unitario=?, vl_frete=?, vl_total=?
                    WHERE id_item=?
                """, (id_nota, id_produto, qtde, cd_cfop, unit, frete, total, self.current_id))
                self.show_message(f"Item atualizado com sucesso!", "success")

            conn.commit()
            conn.close()
            self.limpar()
            self.carregar()
        except Exception as e:
            self.show_message(f"Erro ao salvar: {str(e)}", "error")

    def remover(self):
        try:
            item = self.tree.focus()
            if not item:
                self.show_message("Selecione um item para remover.", "warning")
                return
            
            item_values = self.tree.item(item)["values"]
            id_item = item_values[0]
            produto = item_values[2]
            
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alba0013 WHERE id_item = ?", (id_item,))
            conn.commit()
            conn.close()
            
            self.show_message(f"Item '{produto}' removido com sucesso!", "success")
            self.carregar()
            self.limpar()
        except Exception as e:
            self.show_message(f"Erro ao remover: {str(e)}", "error")

    def carregar(self):
        try:
            self.tree.delete(*self.tree.get_children())
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.id_item, n.nr_nota, p.nm_produto, i.qt_produto, i.cd_cfop,
                       i.vl_unitario, i.vl_frete, i.vl_total
                FROM alba0013 i
                LEFT JOIN alba0012 n ON i.id_nota = n.id_nota
                LEFT JOIN alba0005 p ON i.id_produto = p.id_produto
                ORDER BY i.id_item DESC
            """)
            resultados = cursor.fetchall()
            for row in resultados:
                self.tree.insert("", "end", values=row)
            conn.close()
            self.show_message(f"Carregados {len(resultados)} itens", "success")
        except Exception as e:
            self.show_message(f"Erro ao carregar dados: {str(e)}", "error")

    def on_select(self, event):
        try:
            item = self.tree.item(self.tree.focus())
            if not item or not item.get("values"):
                return
            
            values = item["values"]
            if len(values) >= 8:
                id_item = values[0]
                self.current_id = id_item  # Armazenar ID para edição
                
                # Carregar dados completos do item
                conn = self.conectar()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT i.*, n.nr_nota, p.nm_produto
                    FROM alba0013 i
                    LEFT JOIN alba0012 n ON i.id_nota = n.id_nota
                    LEFT JOIN alba0005 p ON i.id_produto = p.id_produto
                    WHERE i.id_item = ?
                """, (id_item,))
                item_data = cursor.fetchone()
                conn.close()
                
                if item_data:
                    # Preencher combos
                    nota_text = f"{item_data[1]} - {item_data[8]}"
                    produto_text = f"{item_data[2]} - {item_data[9]}"
                    cfop_text = next((f"{c} - {desc}" for c, desc in self.cfops if c == item_data[4]), item_data[4])
                    
                    self.combo_nota.set(nota_text)
                    self.combo_produto.set(produto_text)
                    self.combo_cfop.set(cfop_text)
                    
                    # Preencher campos
                    self.entry_qtde.delete(0, tk.END)
                    self.entry_qtde.insert(0, str(item_data[3] or ""))
                    
                    self.entry_unit.delete(0, tk.END)
                    self.entry_unit.insert(0, str(item_data[5] or ""))
                    
                    self.entry_frete.delete(0, tk.END)
                    self.entry_frete.insert(0, str(item_data[6] or ""))
                    
                    self.entry_total.delete(0, tk.END)
                    self.entry_total.insert(0, str(item_data[7] or ""))
                    
                    self.show_message(f"Item selecionado para edição", "info")
        except Exception as e:
            self.show_message(f"Erro ao selecionar: {str(e)}", "error")

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.current_id = None
        for entry in [self.entry_qtde, self.entry_unit, self.entry_frete, self.entry_total]:
            entry.delete(0, tk.END)
        for cb in [self.combo_nota, self.combo_produto, self.combo_cfop]:
            cb.set("")

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
