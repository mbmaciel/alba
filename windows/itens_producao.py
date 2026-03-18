import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class ItensProducaoWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Itens de Produção (alba0009)")
        self.config(width=1200, height=700)
        
        # Standardized ID pattern - separate current_id and current_recnum
        self.current_id = None          # Primary key (not used in this table, but for consistency)
        # current_recnum is already initialized by BaseWindow
        # Índice do item atual na lista de itens
        self.indice_atual = -1
        # Lista de IDs dos itens
        self.lista_ids = []

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

        btn_primeiro = ttkb.Button(nav_container, text="⏮", command=self.primeiro, width=3)
        btn_primeiro.pack(side=tk.LEFT)
        self.create_tooltip(btn_primeiro, "Primeiro")
        
        btn_anterior = ttkb.Button(nav_container, text="◀", command=self.anterior, width=3)
        btn_anterior.pack(side=tk.LEFT)
        self.create_tooltip(btn_anterior, "Anterior")
        
        btn_proximo = ttkb.Button(nav_container, text="▶", command=self.proximo, width=3)
        btn_proximo.pack(side=tk.LEFT)
        self.create_tooltip(btn_proximo, "Próximo")
        
        btn_ultimo = ttkb.Button(nav_container, text="⏭", command=self.ultimo, width=3)
        btn_ultimo.pack(side=tk.LEFT)
        self.create_tooltip(btn_ultimo, "Último")

        # Label para mostrar a posição atual
        self.lbl_posicao = ttkb.Label(nav_container, text="0/0")
        self.lbl_posicao.pack(side=tk.LEFT, padx=10)

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
        ttkb.Label(input_frame, text="Ordem de Fabricação").grid(row=0, column=0, sticky=tk.W)
        self.combo_of = ttkb.Combobox(input_frame, width=20, state="readonly")
        self.combo_of.grid(row=0, column=1, padx=5, pady=5)

        ttkb.Label(input_frame, text="Produto").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.combo_produto = ttkb.Combobox(input_frame, width=40, state="readonly")
        self.combo_produto.grid(row=0, column=3, columnspan=2, padx=5, pady=5)

        # Segunda linha
        ttkb.Label(input_frame, text="Cliente").grid(row=1, column=0, sticky=tk.W)
        self.combo_cliente = ttkb.Combobox(input_frame, width=40, state="readonly")
        self.combo_cliente.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        ttkb.Label(input_frame, text="Quantidade").grid(row=1, column=3, sticky=tk.W, padx=(20, 0))
        self.entry_qtd = ttkb.Entry(input_frame, width=10)
        self.entry_qtd.grid(row=1, column=4, padx=5)

        # Terceira linha
        ttkb.Label(input_frame, text="Valor Unit.").grid(row=2, column=0, sticky=tk.W)
        self.entry_unit = ttkb.Entry(input_frame, width=15)
        self.entry_unit.grid(row=2, column=1, padx=5)

        ttkb.Label(input_frame, text="Desc. %").grid(row=2, column=2, sticky=tk.W, padx=(20, 0))
        self.entry_desc = ttkb.Entry(input_frame, width=10)
        self.entry_desc.grid(row=2, column=3, padx=5)

        ttkb.Label(input_frame, text="Total").grid(row=2, column=4, sticky=tk.W, padx=(20, 0))
        self.entry_total = ttkb.Entry(input_frame, width=15)
        self.entry_total.grid(row=2, column=5, padx=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "of", "produto", "cliente", "qtd", "unit", "total"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="COD")
        self.tree.heading("of", text="OF")
        self.tree.heading("produto", text="PRODUTO")
        self.tree.heading("cliente", text="CLIENTE")
        self.tree.heading("qtd", text="QTD")
        self.tree.heading("unit", text="UNIT")
        self.tree.heading("total", text="TOTAL")
        
        # Configurar larguras das colunas
        self.tree.column("id", width=50)
        self.tree.column("of", width=80)
        self.tree.column("produto", width=300)
        self.tree.column("cliente", width=300)
        self.tree.column("qtd", width=80)
        self.tree.column("unit", width=80)
        self.tree.column("total", width=100)
        
        # Scrollbar para o Treeview
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Adicionar evento de seleção
        self.tree.bind("<<TreeviewSelect>>", self.item_selecionado_evento)

        # Configurar cálculo automático do total
        self.entry_qtd.bind("<KeyRelease>", self.calcular_total)
        self.entry_unit.bind("<KeyRelease>", self.calcular_total)
        self.entry_desc.bind("<KeyRelease>", self.calcular_total)

        self.carregar_produtos()
        self.carregar_clientes()
        self.carregar_of()
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

    def carregar_produtos(self):
        conn = self.conectar()
        cursor = conn.cursor()
        # Modificando para mostrar apenas o nome do produto
        cursor.execute("SELECT id_produto, nm_produto FROM alba0005 ORDER BY nm_produto")
        self.produtos = cursor.fetchall()
        conn.close()
        self.combo_produto["values"] = [nome for _, nome in self.produtos]

    def carregar_clientes(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nr_cnpj_cpf, nm_razao FROM alba0001 ORDER BY nm_razao")
        self.clientes = cursor.fetchall()
        conn.close()
        self.combo_cliente["values"] = [nome for _, nome in self.clientes]

    def carregar_of(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_contatos FROM alba0003 ORDER BY id_contatos")
        self.ordens = cursor.fetchall()
        conn.close()
        self.combo_of["values"] = [str(row[0]) for row in self.ordens]

    def safe_float_convert(self, value, default=0.0):
        """Converte string para float de forma segura"""
        if not value or value.strip() == "":
            return default
        try:
            # Remove espaços e substitui vírgula por ponto se necessário
            clean_value = str(value).strip().replace(',', '.')
            return float(clean_value)
        except (ValueError, TypeError):
            return default

    def safe_int_convert(self, value, default=0):
        """Converte string para int de forma segura"""
        if not value or value.strip() == "":
            return default
        try:
            # Remove espaços e parte decimal se houver
            clean_value = str(value).strip().replace(',', '.')
            return int(float(clean_value))
        except (ValueError, TypeError):
            return default

    def calcular_total(self, event=None):
        try:
            qtd = self.safe_float_convert(self.entry_qtd.get())
            unit = self.safe_float_convert(self.entry_unit.get())
            desc = self.safe_float_convert(self.entry_desc.get())
            total = qtd * unit * (1 - desc / 100)
            self.entry_total.delete(0, tk.END)
            self.entry_total.insert(0, f"{total:.2f}")
        except Exception as e:
            # Em caso de erro, apenas não atualiza o total
            pass

    def item_selecionado_evento(self, event):
        item = self.tree.focus()
        if not item:
            return
            
        # Obter valores do item selecionado
        valores = self.tree.item(item)["values"]
        selected_recnum = valores[0]  # ID do item (recnum)
        
        # Use standardized pattern - set current_recnum using BaseWindow method
        if self.set_current_recnum(selected_recnum):
            # Atualizar o índice atual
            if selected_recnum in self.lista_ids:
                self.indice_atual = self.lista_ids.index(selected_recnum)
                self.atualizar_posicao()
            
            # Buscar dados completos do item no banco
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.id_of, i.id_produto, i.cd_cliente, i.qt_produto, 
                       i.vl_unitario, i.pc_desc_coml, i.vl_total,
                       p.nm_produto,
                       COALESCE(NULLIF(TRIM(c.nm_razao), ''), '') AS nm_cliente
            FROM alba0009 i
            LEFT JOIN alba0005 p ON i.id_produto = p.id_produto
            LEFT JOIN alba0001 c ON i.cd_cliente = c.nr_cnpj_cpf
            WHERE i.recnum = ?
        """, (self.current_recnum,))
            
            item_data = cursor.fetchone()
            conn.close()
            
            if item_data:
                # Preencher os campos do formulário
                if item_data[0] is not None:
                    self.combo_of.set(str(item_data[0]))
                else:
                    self.combo_of.set("")
                
                if item_data[7] is not None:
                    self.combo_produto.set(item_data[7])
                else:
                    self.combo_produto.set("")
                
                self.combo_cliente.set(item_data[8] or "")
                
                self.entry_qtd.delete(0, tk.END)
                self.entry_qtd.insert(0, str(item_data[3] or ""))
                
                self.entry_unit.delete(0, tk.END)
                self.entry_unit.insert(0, str(item_data[4] or ""))
                
                self.entry_desc.delete(0, tk.END)
                self.entry_desc.insert(0, str(item_data[5] or ""))
                
                self.entry_total.delete(0, tk.END)
                self.entry_total.insert(0, str(item_data[6] or ""))

    def novo(self):
        # Clear record state using standardized pattern
        self.clear_record_state()
        self.limpar()
        self.show_message("Novo registro. Preencha os campos e salve.", "info")

    def _execute_save(self):
        try:
            id_of = self.safe_int_convert(self.combo_of.get())
            nome_produto = self.combo_produto.get()
            id_produto = next((id for id, nome in self.produtos if nome == nome_produto), None)
            nome_cliente = self.combo_cliente.get()
            cd_cliente = next((cd for cd, nome in self.clientes if nome == nome_cliente), None)
            qtd = self.safe_int_convert(self.entry_qtd.get())
            unit = self.safe_float_convert(self.entry_unit.get())
            desc = self.safe_float_convert(self.entry_desc.get())
            total = qtd * unit * (1 - desc / 100)

            conn = self.conectar()
            cursor = conn.cursor()

            try:
                if self.current_recnum is not None:
                    # Atualizar registro existente
                    cursor.execute("""
                        UPDATE alba0009 SET
                            id_of = ?, id_produto = ?, cd_cliente = ?, qt_produto = ?, 
                            vl_unitario = ?, pc_desc_coml = ?, pc_desc_fiscal = 0, 
                            vl_unit_final = ?, vl_produto = ?, vl_total = ?
                        WHERE recnum = ?
                    """, (
                        id_of, id_produto, cd_cliente, qtd, unit,
                        desc, unit, total, total, self.current_recnum
                    ))
                    self.show_message("Item atualizado com sucesso!", "success")
                else:
                    # Inserir novo registro - get next recnum using BaseWindow utility
                    next_recnum = self.get_next_recnum("alba0009")
                    if next_recnum is None:
                        self.show_message("Erro ao obter próximo número de registro.", "error")
                        return

                    cursor.execute("""
                        INSERT INTO alba0009 (
                            recnum, id_of, id_produto, cd_cliente, qt_produto, vl_unitario,
                            pc_desc_coml, pc_desc_fiscal, vl_unit_final, vl_produto,
                            vl_total, fl_status, fl_comissao
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?, 'ATIVO', 'S')
                    """, (
                        next_recnum, id_of, id_produto, cd_cliente, qtd, unit,
                        desc, unit, total, total
                    ))
                    # Set current_recnum after successful INSERT
                    self.set_current_recnum(next_recnum)
                    self.show_message("Item salvo com sucesso!", "success")

                conn.commit()
                self.limpar()
                self.carregar()

            except sqlite3.Error as e:
                self.show_message(f"Erro ao salvar no banco: {str(e)}", "error")
                conn.rollback()
            finally:
                conn.close()
        except Exception as e:
            self.show_message(f"Erro ao salvar: {str(e)}", "error")

    def salvar(self):
        try:
            # Validações básicas
            if not self.combo_of.get():
                self.show_message("Selecione uma Ordem de Fabricação.", "warning")
                return
                
            if not self.combo_produto.get():
                self.show_message("Selecione um produto.", "warning")
                return
                
            if not self.combo_cliente.get():
                self.show_message("Selecione um cliente.", "warning")
                return
                
            if not self.entry_qtd.get():
                self.show_message("Informe a quantidade.", "warning")
                return
                
            if not self.entry_unit.get():
                self.show_message("Informe o valor unitário.", "warning")
                return

            # Conversões seguras
            try:
                id_of = self.safe_int_convert(self.combo_of.get())
                if id_of == 0:
                    self.show_message("Ordem de Fabricação inválida.", "error")
                    return
            except:
                self.show_message("Ordem de Fabricação deve ser um número válido.", "error")
                return

            nome_produto = self.combo_produto.get()
            id_produto = next((id for id, nome in self.produtos if nome == nome_produto), None)
            if not id_produto:
                self.show_message("Produto não encontrado.", "error")
                return

            nome_cliente = self.combo_cliente.get()
            cd_cliente = next((cd for cd, nome in self.clientes if nome == nome_cliente), None)
            if not cd_cliente:
                self.show_message("Cliente não encontrado.", "error")
                return

            qtd = self.safe_int_convert(self.entry_qtd.get())
            if qtd <= 0:
                self.show_message("Quantidade deve ser maior que zero.", "error")
                return

            unit = self.safe_float_convert(self.entry_unit.get())
            if unit <= 0:
                self.show_message("Valor unitário deve ser maior que zero.", "error")
                return

            desc = self.safe_float_convert(self.entry_desc.get())
            if desc < 0 or desc > 100:
                self.show_message("Desconto deve estar entre 0 e 100%.", "error")
                return
            
            confirmation_message = f"Confirma a gravação do item '{self.combo_produto.get()}'?"
            if not hasattr(self, '_confirmations'):
                self.setup_confirmation_pattern('save')
    
            if not self.request_confirmation('save', confirmation_message, self._execute_save):
                return

        except Exception as e:
            self.show_message(f"Erro ao salvar: {str(e)}", "error")

    def _execute_removal(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alba0009 WHERE recnum = ?", (self.current_recnum,))
            conn.commit()
            conn.close()
            self.show_message("Item removido com sucesso!", "success")
            # Clear record state after successful removal
            self.clear_record_state()
            self.limpar()
            self.carregar()
        except sqlite3.Error as e:
            self.show_message(f"Erro ao remover: {str(e)}", "error")

    def remover(self):
        if self.current_recnum is None:
            self.show_message("Selecione um item para remover.", "warning")
            return

        # Obter nome do produto para confirmação
        item = self.tree.focus()
        if item:
            valores = self.tree.item(item)["values"]
            produto_nome = valores[2] if len(valores) > 2 else "item"

            confirmation_message = f"Pressione 'Remover' novamente para excluir o item '{produto_nome}'."

            if not hasattr(self, '_confirmations'):
                self.setup_confirmation_pattern('remove')

            if not self.request_confirmation('remove', confirmation_message, self._execute_removal):
                return

    def carregar(self):
        try:
            self.tree.delete(*self.tree.get_children())
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.recnum, i.id_of,
                       p.nm_produto, COALESCE(NULLIF(TRIM(c.nm_razao), ''), '') AS nm_cliente,
                       i.qt_produto, i.vl_unitario, i.vl_total
                FROM alba0009 i
                LEFT JOIN alba0005 p ON i.id_produto = p.id_produto
                LEFT JOIN alba0001 c ON i.cd_cliente = c.nr_cnpj_cpf
                ORDER BY i.recnum
            """)
            
            # Armazenar os IDs para navegação
            self.lista_ids = []
            rows = cursor.fetchall()
            
            for row in rows:
                self.lista_ids.append(row[0])  # Armazenar o ID (recnum)
                self.tree.insert("", "end", values=row)
                
            conn.close()
            
            # Atualizar o contador de posição
            self.indice_atual = -1 if not self.lista_ids else 0
            self.atualizar_posicao()
            
            # Se houver registros, selecionar o primeiro
            if self.lista_ids and self.indice_atual == 0:
                self.carregar_registro(self.lista_ids[0])
                
            self.show_message(f"Carregados {len(rows)} itens de produção", "success")
            
        except Exception as e:
            self.show_message(f"Erro ao carregar dados: {str(e)}", "error")

    def limpar(self):
        # Use standardized pattern - clear record state
        self.clear_record_state()
        self.combo_of.set("")
        self.combo_produto.set("")
        self.combo_cliente.set("")
        self.entry_qtd.delete(0, tk.END)
        self.entry_unit.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.entry_total.delete(0, tk.END)
    
    # Funções de navegação
    def primeiro(self):
        if not self.lista_ids:
            self.show_message("Nenhum registro encontrado.", "warning")
            return
        self.indice_atual = 0
        self.carregar_registro(self.lista_ids[self.indice_atual])
        self.atualizar_posicao()
    
    def anterior(self):
        if not self.lista_ids or self.indice_atual <= 0:
            self.show_message("Já está no primeiro registro.", "info")
            return
        self.indice_atual -= 1
        self.carregar_registro(self.lista_ids[self.indice_atual])
        self.atualizar_posicao()
    
    def proximo(self):
        if not self.lista_ids or self.indice_atual >= len(self.lista_ids) - 1:
            self.show_message("Já está no último registro.", "info")
            return
        self.indice_atual += 1
        self.carregar_registro(self.lista_ids[self.indice_atual])
        self.atualizar_posicao()
    
    def ultimo(self):
        if not self.lista_ids:
            self.show_message("Nenhum registro encontrado.", "warning")
            return
        self.indice_atual = len(self.lista_ids) - 1
        self.carregar_registro(self.lista_ids[self.indice_atual])
        self.atualizar_posicao()
    
    def atualizar_posicao(self):
        """Atualiza o texto que mostra a posição atual na navegação"""
        total = len(self.lista_ids)
        posicao = self.indice_atual + 1 if self.indice_atual >= 0 else 0
        self.lbl_posicao.config(text=f"{posicao}/{total}")
    
    def carregar_registro(self, recnum):
        """Carrega um registro específico pelo seu recnum - properly manage current_recnum field"""
        # Use standardized pattern - set current_recnum using BaseWindow method
        if not self.set_current_recnum(recnum):
            return
        
        # Buscar dados completos do item no banco
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.id_of, i.id_produto, i.cd_cliente, i.qt_produto, 
                   i.vl_unitario, i.pc_desc_coml, i.vl_total,
                   p.nm_produto,
                   c.nm_razao
            FROM alba0009 i
            LEFT JOIN alba0005 p ON i.id_produto = p.id_produto
            LEFT JOIN alba0001 c ON i.cd_cliente = c.nr_cnpj_cpf
            WHERE i.recnum = ?
        """, (self.current_recnum,))
        
        item_data = cursor.fetchone()
        conn.close()
        
        if item_data:
            # Preencher os campos do formulário
            if item_data[0] is not None:
                self.combo_of.set(str(item_data[0]))
            else:
                self.combo_of.set("")
                
            if item_data[7] is not None:
                self.combo_produto.set(item_data[7])
            else:
                self.combo_produto.set("")
                
            self.combo_cliente.set(item_data[8] or "")
                
            self.entry_qtd.delete(0, tk.END)
            self.entry_qtd.insert(0, str(item_data[3] or ""))
            
            self.entry_unit.delete(0, tk.END)
            self.entry_unit.insert(0, str(item_data[4] or ""))
            
            self.entry_desc.delete(0, tk.END)
            self.entry_desc.insert(0, str(item_data[5] or ""))
            
            self.entry_total.delete(0, tk.END)
            self.entry_total.insert(0, str(item_data[6] or ""))
            
            # Selecionar o item na treeview
            for item in self.tree.get_children():
                if self.tree.item(item)["values"][0] == recnum:
                    self.tree.selection_set(item)
                    self.tree.focus(item)
                    self.tree.see(item)
                    break
