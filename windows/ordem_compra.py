import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
import sqlite3
from datetime import datetime
from windows.base_window import BaseWindow

class OrdemCompraWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.set_title("Cadastro de Ordens de Compra (alba0010)")
        self.config(width=1000, height=650)
        
        # Initialize record state fields
        self.current_id = None
        self.current_recnum = None

        # Frame principal
        main_frame = ttkb.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Barra de ferramentas no topo
        toolbar_frame = ttkb.Frame(main_frame, relief="raised", borderwidth=2, padding=5)
        toolbar_frame.pack(fill=tk.X, pady=(0, 15))

        # Create standard message panel
        self.ensure_message_panel(main_frame)

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

        # Frame para campos de entrada
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        # Primeira linha
        ttkb.Label(input_frame, text="Empresa").grid(row=0, column=0, sticky=tk.W)
        self.combo_empresa = ttkb.Combobox(input_frame, width=30, state="readonly")
        self.combo_empresa.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Cliente").grid(row=0, column=2, sticky=tk.W)
        self.combo_cliente = ttkb.Combobox(input_frame, width=30, state="readonly")
        self.combo_cliente.grid(row=0, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Data (dd/mm/yyyy)").grid(row=0, column=4, sticky=tk.W)
        self.entry_data = ttkb.Entry(input_frame, width=15)
        self.entry_data.grid(row=0, column=5, pady=5, padx=5)

        # Segunda linha
        ttkb.Label(input_frame, text="Contato").grid(row=1, column=0, sticky=tk.W)
        self.combo_contato = ttkb.Combobox(input_frame, width=30, state="readonly")
        self.combo_contato.grid(row=1, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Pedido Cliente").grid(row=1, column=2, sticky=tk.W)
        self.entry_pedido = ttkb.Entry(input_frame, width=20)
        self.entry_pedido.grid(row=1, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Status").grid(row=1, column=4, sticky=tk.W)
        self.combo_status = ttkb.Combobox(input_frame, width=12, values=["F", "C"], state="readonly")
        self.combo_status.grid(row=1, column=5, pady=5, padx=5)

        # Terceira linha
        ttkb.Label(input_frame, text="Prazo").grid(row=2, column=0, sticky=tk.W)
        self.entry_prazo = ttkb.Entry(input_frame, width=30)
        self.entry_prazo.grid(row=2, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Condições").grid(row=2, column=2, sticky=tk.W)
        self.entry_condicoes = ttkb.Entry(input_frame, width=30)
        self.entry_condicoes.grid(row=2, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Valor Total").grid(row=2, column=4, sticky=tk.W)
        self.entry_total = ttkb.Entry(input_frame, width=15)
        self.entry_total.grid(row=2, column=5, pady=5, padx=5)

        # Quarta linha - Observações
        ttkb.Label(input_frame, text="Observações").grid(row=3, column=0, sticky=tk.W)
        self.entry_obs = ttkb.Entry(input_frame, width=80)
        self.entry_obs.grid(row=3, column=1, columnspan=5, pady=5, padx=(5, 0), sticky=tk.W+tk.E)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "cliente", "contato", "data", "pedido", "status", "total"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="COD")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("contato", text="Contato")
        self.tree.heading("data", text="Data")
        self.tree.heading("pedido", text="Pedido")
        self.tree.heading("status", text="Status")
        self.tree.heading("total", text="Total")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("cliente", width=200, minwidth=150, anchor=tk.W)
        self.tree.column("contato", width=150, minwidth=100, anchor=tk.W)
        self.tree.column("data", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column("pedido", width=120, minwidth=100, anchor=tk.W)
        self.tree.column("status", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column("total", width=120, minwidth=100, anchor=tk.E)
        
        # Scrollbar para o Treeview
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        # Inicializar data atual no formato dd/mm/yyyy
        self.entry_data.insert(0, datetime.today().strftime("%d/%m/%Y"))

        self.carregar_empresas()
        self.carregar_clientes()
        self.carregar_contatos()
        self.carregar()

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar()
        self.clear_record_state()
        self.combo_empresa.focus()

    def carregar_empresas(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_empresa, nm_razao FROM empresas ORDER BY nm_razao")
        self.empresas = cursor.fetchall()
        conn.close()
        self.combo_empresa['values'] = [nome for _, nome in self.empresas]

    def carregar_clientes(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_pessoa, nm_razao FROM alba0001 ORDER BY nm_razao")
        self.clientes = cursor.fetchall()
        conn.close()
        self.combo_cliente['values'] = [nome for _, nome in self.clientes]

    def carregar_contatos(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_contato, nm_contato FROM contatos ORDER BY nm_contato")
        self.contatos = cursor.fetchall()
        conn.close()
        self.combo_contato['values'] = [nome for _, nome in self.contatos]

    def converter_data_para_bd(self, data_br):
        """Converte data do formato dd/mm/yyyy para yyyy-mm-dd"""
        try:
            if data_br and "/" in data_br:
                dia, mes, ano = data_br.split("/")
                return f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"
            return data_br
        except:
            return data_br

    def converter_data_para_br(self, data_bd):
        """Converte data do formato yyyy-mm-dd para dd/mm/yyyy"""
        try:
            if data_bd and "-" in data_bd:
                ano, mes, dia = data_bd.split("-")
                return f"{dia.zfill(2)}/{mes.zfill(2)}/{ano}"
            return data_bd
        except:
            return data_bd
        
    def _execute_save(self):
        """Salva a ordem de compra com manejo adequado do recnum"""
        try:
            # Validações básicas
            if not self.combo_empresa.get():
                self.show_message("Selecione uma empresa", "warning")
                return
            if not self.combo_cliente.get():
                self.show_message("Selecione um cliente", "warning")
                return

            nome_empresa = self.combo_empresa.get()
            id_empresa = next((id for id, nome in self.empresas if nome == nome_empresa), None)

            nome_cliente = self.combo_cliente.get()
            id_cliente = next((id for id, nome in self.clientes if nome == nome_cliente), None)

            # Contato obrigatorio - guardar id e nome
            nome_contato = self.combo_contato.get()
            if nome_contato:
                id_contato = next((id for id, nome in self.contatos if nome == nome_contato), None)
            else:
                self.show_message("Selecione um contato", "warning")
                return

            # Usar o valor informado (mesma abordagem do orcamento)
            data_bd = self.entry_data.get().strip()

            conn = self.conectar()
            cursor = conn.cursor()

            if self.current_id is None:
                # INSERT - novo registro
                next_recnum = self.get_next_recnum("alba0010")
                if next_recnum is None:
                    return  # Error already shown by get_next_recnum
                
                data = (
                    next_recnum,
                    id_empresa,
                    id_cliente,
                    data_bd,
                    id_contato,
                    nome_contato or "",
                    self.entry_pedido.get(),
                    self.entry_prazo.get(),
                    self.entry_condicoes.get(),
                    self.entry_obs.get(),
                    self.entry_total.get(),
                    self.combo_status.get()
                )

                cursor.execute("""
                    INSERT INTO alba0010 (
                        recnum, id_empresa, id_cliente, dt_oc, id_contato, nm_contato, nr_pedido_cli,
                        tx_prazo, tx_condicoes, tx_obs, vl_total, fl_status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, data)
                
                # Get the new record ID and set current_recnum
                cursor.execute("SELECT last_insert_rowid()")
                self.current_id = cursor.fetchone()[0]
                self.set_current_recnum(next_recnum)
                
                self.show_message("Ordem de compra salva com sucesso!", "success")
            else:
                # UPDATE - registro existente
                data = (
                    id_empresa,
                    id_cliente,
                    data_bd,
                    id_contato,
                    nome_contato or "",
                    self.entry_pedido.get(),
                    self.entry_prazo.get(),
                    self.entry_condicoes.get(),
                    self.entry_obs.get(),
                    self.entry_total.get(),
                    self.combo_status.get(),
                    self.current_id
                )

                cursor.execute("""
                    UPDATE alba0010 SET
                        id_empresa = ?, id_cliente = ?, dt_oc = ?, id_contato = ?, nm_contato = ?, nr_pedido_cli = ?,
                        tx_prazo = ?, tx_condicoes = ?, tx_obs = ?, vl_total = ?, fl_status = ?
                    WHERE id_oc = ?
                """, data)
                
                self.show_message("Ordem de compra atualizada com sucesso!", "success")

            conn.commit()
            conn.close()
            self.carregar()

        except sqlite3.Error as e:
            if 'conn' in locals():
                conn.close()
            self.show_message(f"Erro ao salvar ordem de compra: {str(e)}", "error")
        except Exception as e:
            if 'conn' in locals():
                conn.close()
            self.show_message(f"Erro inesperado: {str(e)}", "error")

    def salvar(self):
        if not self.combo_empresa.get() or not self.combo_cliente.get():
            self.show_message("Selecione uma empresa e um cliente.", "warning")
            return

        cliente_nome = self.combo_cliente.get()
        confirmation_message = f"Confirma a gravação da ordem de compra para '{cliente_nome}'?"
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('save')

        if not self.request_confirmation('save', confirmation_message, self._execute_save):
            return

    def _execute_removal(self, id_oc):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alba0010 WHERE id_oc = ?", (id_oc,))
            conn.commit()
            conn.close()
            self.show_message("Ordem de compra removida com sucesso!", "success")
            self.carregar()
            self.limpar()
        except Exception as e:
            self.show_message(f"Erro ao remover ordem de compra: {str(e)}", "error")
            
    def remover(self):
        item = self.tree.focus()
        if not item:
            self.show_message("Selecione uma ordem de compra para remover.", "warning")
            return
            
        values = self.tree.item(item)["values"]
        id_oc = values[0]
        cliente_nome = values[1] if len(values) > 1 else "ordem de compra"

        confirmation_message = f"Pressione 'Remover' novamente para excluir a ordem de compra do cliente '{cliente_nome}'."

        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('remove')

        if not self.request_confirmation('remove', confirmation_message, self._execute_removal, id_oc):
            return

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.id_oc, c.nm_razao AS cliente, COALESCE(ct.nm_contato, o.nm_contato) AS contato, o.dt_oc,
                   o.nr_pedido_cli, o.fl_status, o.vl_total
            FROM alba0010 o
            LEFT JOIN alba0001 c ON o.id_cliente = c.id_pessoa
            LEFT JOIN contatos ct ON o.id_contato = ct.id_contato
        """)
        for row in cursor.fetchall():
            row_list = list(row)
            if row_list[2] is None:
                row_list[2] = ""
            if row_list[3]:
                row_list[3] = row_list[3][:10] if len(row_list[3]) > 10 else row_list[3]
            self.tree.insert("", "end", values=row_list)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        values = item.get("values", [])
        if len(values) < 7:
            return
        
        id_oc = values[0]
        
        # Buscar todos os dados da ordem de compra selecionada incluindo recnum
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.id_oc, o.recnum, o.id_empresa, o.id_cliente, o.dt_oc, o.id_contato, 
                   o.nr_pedido_cli, o.fl_status, o.vl_total, o.tx_prazo, 
                   o.tx_condicoes, o.tx_obs,
                   e.nm_razao AS empresa_nome,
                   c.nm_razao AS cliente_nome,
                   COALESCE(ct.nm_contato, o.nm_contato) AS contato_nome
            FROM alba0010 o
            LEFT JOIN empresas e ON o.id_empresa = e.id_empresa
            LEFT JOIN alba0001 c ON o.id_cliente = c.id_pessoa
            LEFT JOIN contatos ct ON o.id_contato = ct.id_contato
            WHERE o.id_oc = ?
        """, (id_oc,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            (id_oc, recnum, id_empresa, id_cliente, data, id_contato, pedido, status, total, 
             prazo, condicoes, obs, empresa_nome, cliente_nome, contato_nome) = result
            
            # Synchronize record state
            self.current_id = id_oc
            self.set_current_recnum(recnum)
            
            # Preencher os campos
            self.combo_empresa.set(empresa_nome or "")
            self.combo_cliente.set(cliente_nome or "")
            self.combo_contato.set(contato_nome or "")
            
            self.entry_data.delete(0, tk.END)
            data_fmt = data[:10] if data else ""
            self.entry_data.insert(0, data_fmt)
            
            self.entry_pedido.delete(0, tk.END)
            self.entry_pedido.insert(0, pedido or "")
            
            self.combo_status.set(status or "")
            
            self.entry_total.delete(0, tk.END)
            self.entry_total.insert(0, total or "")
            
            self.entry_prazo.delete(0, tk.END)
            self.entry_prazo.insert(0, prazo or "")
            
            self.entry_condicoes.delete(0, tk.END)
            self.entry_condicoes.insert(0, condicoes or "")
            
            self.entry_obs.delete(0, tk.END)
            self.entry_obs.insert(0, obs or "")

    def limpar(self):
        """Limpa os campos do formulário e o estado do registro"""
        self.combo_empresa.set("")
        self.combo_cliente.set("")
        self.combo_contato.set("")
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, datetime.today().strftime("%d/%m/%Y"))
        self.entry_pedido.delete(0, tk.END)
        self.combo_status.set("")
        self.entry_total.delete(0, tk.END)
        self.entry_prazo.delete(0, tk.END)
        self.entry_condicoes.delete(0, tk.END)
        self.entry_obs.delete(0, tk.END)
        
        # Clear record state
        self.clear_record_state()

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

    def ir_primeiro(self):
        """Navega para o primeiro registro"""
        children = self.tree.get_children()
        if children:
            first_item = children[0]
            self.tree.selection_set(first_item)
            self.tree.focus(first_item)
            self.tree.see(first_item)
            self.on_select(None)

    def ir_ultimo(self):
        """Navega para o último registro"""
        children = self.tree.get_children()
        if children:
            last_item = children[-1]
            self.tree.selection_set(last_item)
            self.tree.focus(last_item)
            self.tree.see(last_item)
            self.on_select(None)

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
        else:
            self.ir_primeiro()
        
