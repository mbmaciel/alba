import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
from estilo import aplicar_estilo
from windows.base_window import BaseWindow

class OrcamentoWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_id = None
        self.current_recnum = None
        aplicar_estilo(self)
        self.set_title("Orçamentos / Ordens de Faturamento (alba0008)")
        self.config(width=1200, height=800)

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

        # Primeira linha - IDs e Datas
        ttkb.Label(input_frame, text="ID OF").grid(row=0, column=0, sticky=tk.W)
        self.entry_id_of = ttkb.Entry(input_frame, width=10, state="readonly")
        self.entry_id_of.grid(row=0, column=1, pady=5, padx=(5, 20), sticky=tk.W)

        ttkb.Label(input_frame, text="Data OF").grid(row=0, column=2, sticky=tk.W)
        self.entry_dt_of = ttkb.DateEntry(input_frame, width=12)
        self.entry_dt_of.grid(row=0, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Data Vencimento").grid(row=0, column=4, sticky=tk.W)
        self.entry_dt_vencto = ttkb.DateEntry(input_frame, width=12)
        self.entry_dt_vencto.grid(row=0, column=5, pady=5, padx=5)

        # Segunda linha - Empresa e Cliente
        ttkb.Label(input_frame, text="Empresa").grid(row=1, column=0, sticky=tk.W)
        self.combo_empresa = ttkb.Combobox(input_frame, width=30, state="readonly")
        self.combo_empresa.grid(row=1, column=1, columnspan=2, pady=5, padx=(5, 20), sticky=tk.W+tk.E)

        ttkb.Label(input_frame, text="Cliente").grid(row=1, column=3, sticky=tk.W)
        self.combo_cliente = ttkb.Combobox(input_frame, width=30, state="readonly")
        self.combo_cliente.grid(row=1, column=4, columnspan=2, pady=5, padx=5, sticky=tk.W+tk.E)

        # Terceira linha - Contato e Tipo
        ttkb.Label(input_frame, text="Contato").grid(row=2, column=0, sticky=tk.W)
        self.combo_contato = ttkb.Combobox(input_frame, width=30, state="readonly")
        self.combo_contato.grid(row=2, column=1, columnspan=2, pady=5, padx=(5, 20), sticky=tk.W+tk.E)

        ttkb.Label(input_frame, text="Tipo").grid(row=2, column=3, sticky=tk.W)
        self.combo_tipo = ttkb.Combobox(input_frame, width=25, state="readonly")
        self.combo_tipo.grid(row=2, column=4, pady=5, padx=(5, 20))

        # Quarta linha - Pedido Cliente e Transportadora
        ttkb.Label(input_frame, text="Pedido Cliente").grid(row=3, column=0, sticky=tk.W)
        self.entry_pedido_cli = ttkb.Entry(input_frame, width=30)
        self.entry_pedido_cli.grid(row=3, column=1, columnspan=2, pady=5, padx=(5, 20), sticky=tk.W+tk.E)

        ttkb.Label(input_frame, text="Transportadora").grid(row=3, column=3, sticky=tk.W)
        self.combo_transp = ttkb.Combobox(input_frame, width=25, state="readonly")
        self.combo_transp.grid(row=3, column=4, pady=5, padx=(5, 20))

        # Quinta linha - Prazo e Condições
        ttkb.Label(input_frame, text="Prazo").grid(row=4, column=0, sticky=tk.W)
        self.entry_prazo = ttkb.Entry(input_frame, width=30)
        self.entry_prazo.grid(row=4, column=1, columnspan=2, pady=5, padx=(5, 20), sticky=tk.W+tk.E)

        ttkb.Label(input_frame, text="Condições").grid(row=4, column=3, sticky=tk.W)
        self.entry_condicoes = ttkb.Entry(input_frame, width=30)
        self.entry_condicoes.grid(row=4, column=4, columnspan=2, pady=5, padx=5, sticky=tk.W+tk.E)

        # Sexta linha - Valores
        values_frame = ttkb.LabelFrame(input_frame, text="Valores", padding=10)
        values_frame.grid(row=5, column=0, columnspan=6, pady=10, padx=5, sticky=tk.W+tk.E)

        # Primeira linha de valores
        ttkb.Label(values_frame, text="Mercadoria").grid(row=0, column=0, sticky=tk.W)
        self.entry_vl_mercadoria = ttkb.Entry(values_frame, width=12)
        self.entry_vl_mercadoria.grid(row=0, column=1, pady=2, padx=(5, 20))

        ttkb.Label(values_frame, text="IPI").grid(row=0, column=2, sticky=tk.W)
        self.entry_vl_ipi = ttkb.Entry(values_frame, width=12)
        self.entry_vl_ipi.grid(row=0, column=3, pady=2, padx=(5, 20))

        ttkb.Label(values_frame, text="ICMS").grid(row=0, column=4, sticky=tk.W)
        self.entry_vl_icms = ttkb.Entry(values_frame, width=12)
        self.entry_vl_icms.grid(row=0, column=5, pady=2, padx=5)

        # Segunda linha de valores
        ttkb.Label(values_frame, text="ICMS ST").grid(row=1, column=0, sticky=tk.W)
        self.entry_vl_icmsst = ttkb.Entry(values_frame, width=12)
        self.entry_vl_icmsst.grid(row=1, column=1, pady=2, padx=(5, 20))

        ttkb.Label(values_frame, text="ISS").grid(row=1, column=2, sticky=tk.W)
        self.entry_vl_iss = ttkb.Entry(values_frame, width=12)
        self.entry_vl_iss.grid(row=1, column=3, pady=2, padx=(5, 20))

        ttkb.Label(values_frame, text="Total").grid(row=1, column=4, sticky=tk.W)
        self.entry_vl_total = ttkb.Entry(values_frame, width=12, font=("Arial", 10, "bold"))
        self.entry_vl_total.grid(row=1, column=5, pady=2, padx=5)

        # Terceira linha de valores - Comissão
        ttkb.Label(values_frame, text="% Comissão").grid(row=2, column=0, sticky=tk.W)
        self.entry_pc_comissao = ttkb.Entry(values_frame, width=12)
        self.entry_pc_comissao.grid(row=2, column=1, pady=2, padx=(5, 20))

        ttkb.Label(values_frame, text="Vl. Comissão").grid(row=2, column=2, sticky=tk.W)
        self.entry_vl_comissao = ttkb.Entry(values_frame, width=12)
        self.entry_vl_comissao.grid(row=2, column=3, pady=2, padx=(5, 20))

        ttkb.Label(values_frame, text="Qt. Itens").grid(row=2, column=4, sticky=tk.W)
        self.entry_qt_itens = ttkb.Entry(values_frame, width=12)
        self.entry_qt_itens.grid(row=2, column=5, pady=2, padx=5)

        # Sétima linha - Status e Flags
        status_frame = ttkb.Frame(input_frame)
        status_frame.grid(row=6, column=0, columnspan=6, pady=10, sticky=tk.W)

        ttkb.Label(status_frame, text="Status").pack(side=tk.LEFT)
        self.combo_status = ttkb.Combobox(status_frame, width=15, state="readonly", 
                                         values=["Aberto", "Fechado", "Cancelado"])
        self.combo_status.pack(side=tk.LEFT, padx=(5, 20))

        self.var_mapa = tk.IntVar()
        ttkb.Checkbutton(status_frame, text="Incluir no Mapa", variable=self.var_mapa).pack(side=tk.LEFT, padx=(0, 20))

        # Oitava linha - Observações
        ttkb.Label(input_frame, text="Observações").grid(row=7, column=0, sticky=tk.NW)
        self.text_obs = tk.Text(input_frame, width=80, height=3, wrap=tk.WORD)
        self.text_obs.grid(row=7, column=1, columnspan=5, pady=5, padx=(5, 0), sticky=tk.W+tk.E)
        
        # Scrollbar para observações
        scrollbar_obs = tk.Scrollbar(input_frame, orient=tk.VERTICAL, command=self.text_obs.yview)
        self.text_obs.configure(yscrollcommand=scrollbar_obs.set)
        scrollbar_obs.grid(row=7, column=6, sticky=tk.NS, pady=5)

        # Configurar expansão das colunas
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(4, weight=1)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas
        self.tree = ttkb.Treeview(tree_frame, columns=(
            "id", "empresa", "cliente", "dt_of", "dt_vencto", "pedido_cli", 
            "vl_total", "qt_itens", "status", "obs"
        ), show="headings", height=12)
        
        # Configuração das colunas
        self.tree.heading("id", text="COD")
        self.tree.heading("empresa", text="Empresa")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("dt_of", text="Data OF")
        self.tree.heading("dt_vencto", text="Vencimento")
        self.tree.heading("pedido_cli", text="Pedido Cliente")
        self.tree.heading("vl_total", text="Valor Total")
        self.tree.heading("qt_itens", text="Itens")
        self.tree.heading("status", text="Status")
        self.tree.heading("obs", text="Observações")
        
        # Configuração das larguras das colunas
        self.tree.column("id", width=0, stretch=False)  # Hidden
        self.tree.column("empresa", width=120, minwidth=100, anchor=tk.W)
        self.tree.column("cliente", width=150, minwidth=120, anchor=tk.W)
        self.tree.column("dt_of", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column("dt_vencto", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column("pedido_cli", width=120, minwidth=100, anchor=tk.W)
        self.tree.column("vl_total", width=100, minwidth=80, anchor=tk.E)
        self.tree.column("qt_itens", width=60, minwidth=50, anchor=tk.CENTER)
        self.tree.column("status", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("obs", width=200, minwidth=150, anchor=tk.W)
        
        # Scrollbar para o Treeview
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        # Carregar dados iniciais
        self.carregar_empresas()
        self.carregar_clientes()
        self.carregar_contatos()
        self.carregar_tipos()
        self.carregar_transportadoras()
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
        self.entry_dt_of.entry.focus()
        self.show_message("Campos limpos. Preencha os dados do novo orçamento.", "info")

    def carregar_empresas(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_empresa, nm_razao FROM empresas ORDER BY nm_razao")
            self.empresas = cursor.fetchall()
            conn.close()
            self.combo_empresa["values"] = [nome for _, nome in self.empresas]
        except Exception as e:
            self.show_message(f"ERRO ao carregar empresas: {str(e)}", "error")

    def carregar_clientes(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_pessoa, nm_razao FROM alba0001
                WHERE fl_cliente = '1' OR fl_cliente = 'S'
                ORDER BY nm_razao
            """)
            self.clientes = cursor.fetchall()
            conn.close()
            self.combo_cliente["values"] = [nome for _, nome in self.clientes]
        except Exception as e:
            self.show_message(f"ERRO ao carregar clientes: {str(e)}", "error")

    def carregar_contatos(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_contato, nm_contato FROM contatos ORDER BY nm_contato")
            self.contatos = cursor.fetchall()
            conn.close()
            self.combo_contato["values"] = [nome for _, nome in self.contatos]
        except Exception as e:
            self.show_message(f"ERRO ao carregar contatos: {str(e)}", "error")

    def carregar_tipos(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_tipo, nm_tipo FROM tipo ORDER BY nm_tipo")
            self.tipos = cursor.fetchall()
            conn.close()
            self.combo_tipo["values"] = [nome for _, nome in self.tipos]
        except Exception as e:
            self.show_message(f"ERRO ao carregar tipos: {str(e)}", "error")

    def carregar_transportadoras(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_pessoa, nm_razao FROM alba0001
                WHERE fl_transp = '1' OR fl_transp = 'S'
                ORDER BY nm_razao
            """)
            self.transportadoras = cursor.fetchall()
            conn.close()
            self.combo_transp["values"] = [nome for _, nome in self.transportadoras]
        except Exception as e:
            self.show_message(f"ERRO ao carregar transportadoras: {str(e)}", "error")

    def _execute_save(self):
        # Coletar dados dos campos
        dt_of = self.entry_dt_of.entry.get()
        dt_vencto = self.entry_dt_vencto.entry.get()
        pedido_cli = self.entry_pedido_cli.get().strip()
        prazo = self.entry_prazo.get().strip()
        condicoes = self.entry_condicoes.get().strip()
        obs = self.text_obs.get("1.0", tk.END).strip()

        # Valores
        try:
            vl_mercadoria = float(self.entry_vl_mercadoria.get() or "0")
            vl_ipi = float(self.entry_vl_ipi.get() or "0")
            vl_icms = float(self.entry_vl_icms.get() or "0")
            vl_icmsst = float(self.entry_vl_icmsst.get() or "0")
            vl_iss = float(self.entry_vl_iss.get() or "0")
            vl_total = float(self.entry_vl_total.get() or "0")
            pc_comissao = float(self.entry_pc_comissao.get() or "0")
            vl_comissao = float(self.entry_vl_comissao.get() or "0")
            qt_itens = int(self.entry_qt_itens.get() or "0")
        except ValueError:
            self.show_message("ERRO: Valores numéricos inválidos.", "error")
            return

        # IDs dos combos
        nome_empresa = self.combo_empresa.get().strip()
        id_empresa = next((id for id, nome in self.empresas if nome == nome_empresa), None) if nome_empresa else None

        nome_cliente = self.combo_cliente.get().strip()
        id_cliente = next((id for id, nome in self.clientes if nome == nome_cliente), None) if nome_cliente else None

        nome_contato = self.combo_contato.get().strip()
        id_contato = next((id for id, nome in self.contatos if nome == nome_contato), None) if nome_contato else None

        nome_tipo = self.combo_tipo.get().strip()
        id_tipo = next((id for id, nome in self.tipos if nome == nome_tipo), None) if nome_tipo else None

        nome_transp = self.combo_transp.get().strip()
        id_transp = next((id for id, nome in self.transportadoras if nome == nome_transp), None) if nome_transp else None

        # Status e flags
        status = self.combo_status.get()
        fl_mapa = '1' if self.var_mapa.get() else '0'

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            is_update = self.current_id is not None

            if is_update:
                # Atualizar registro existente
                sql = """UPDATE alba0008 SET
                         id_empresa = ?, id_fatura = ?, dt_of = ?, dt_recebto = ?, dt_vencto = ?,
                         id_cliente = ?, id_contato = ?, nm_contato = ?, id_tipo = ?,
                         nr_pedido_cli = ?, id_texto = ?, tx_prazo = ?, tx_condicoes = ?,
                         tx_obs = ?, id_transp = ?, tx_transp = ?, pc_comissao = ?,
                         vl_comissao = ?, vl_mercadoria = ?, vl_ipi = ?, vl_icms = ?,
                         vl_icmsst = ?, vl_iss = ?, vl_total = ?, qt_itens = ?,
                         fl_status = ?, fl_mapa = ?
                         WHERE id_of = ?"""

                cursor.execute(sql, (
                    id_empresa or 0, 0, dt_of, '0001-01-01', dt_vencto,
                    id_cliente or 0, id_contato or 0, nome_contato or '', id_tipo or 0,
                    pedido_cli, 0, prazo, condicoes, obs, id_transp or 0, '',
                    pc_comissao, vl_comissao, vl_mercadoria, vl_ipi, vl_icms,
                    vl_icmsst, vl_iss, vl_total, qt_itens, status or '', fl_mapa,
                    self.current_id
                ))

                self.show_message(f"Orçamento ID {self.current_id} atualizado com sucesso!", "success")

            else:
                # Inserir novo registro
                next_recnum = self.get_next_recnum("alba0008")
                if next_recnum is None:
                    self.show_message("ERRO: Não foi possível obter próximo recnum", "error")
                    return

                cursor.execute("SELECT COALESCE(MAX(id_of), 0) + 1 FROM alba0008")
                next_id_of = cursor.fetchone()[0]

                sql = """INSERT INTO alba0008 
                         (recnum, id_of, id_empresa, id_fatura, dt_of, dt_recebto, dt_vencto,
                          id_cliente, id_contato, nm_contato, id_tipo, nr_pedido_cli, id_texto,
                          tx_prazo, tx_condicoes, tx_obs, id_transp, tx_transp, pc_comissao,
                          vl_comissao, vl_mercadoria, vl_ipi, vl_icms, vl_icmsst, vl_iss,
                          vl_total, qt_itens, fl_status, fl_mapa)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

                cursor.execute(sql, (
                    next_recnum, next_id_of, id_empresa or 0, 0, dt_of, '0001-01-01', dt_vencto,
                    id_cliente or 0, id_contato or 0, nome_contato or '', id_tipo or 0,
                    pedido_cli, 0, prazo, condicoes, obs, id_transp or 0, '',
                    pc_comissao, vl_comissao, vl_mercadoria, vl_ipi, vl_icms,
                    vl_icmsst, vl_iss, vl_total, qt_itens, status or '', fl_mapa
                ))

                self.show_message(f"Orçamento salvo com sucesso! ID: {next_id_of}", "success")
                self.current_id = next_id_of
                self.current_recnum = next_recnum

            conn.commit()
            self.carregar()

            if is_update:
                self.selecionar_item_por_id(self.current_id)

        except sqlite3.IntegrityError as e:
            conn.rollback()
            self.show_message(f"ERRO ao salvar: {str(e)}", "error")
        except Exception as e:
            conn.rollback()
            self.show_message(f"ERRO inesperado: {str(e)}", "error")
        finally:
            conn.close()

    def salvar(self):
        # Coletar dados dos campos
        dt_of = self.entry_dt_of.entry.get()
        dt_vencto = self.entry_dt_vencto.entry.get()
        pedido_cli = self.entry_pedido_cli.get().strip()
        prazo = self.entry_prazo.get().strip()
        condicoes = self.entry_condicoes.get().strip()
        obs = self.text_obs.get("1.0", tk.END).strip()

        # IDs dos combos
        nome_empresa = self.combo_empresa.get().strip()
        id_empresa = next((id for id, nome in self.empresas if nome == nome_empresa), None) if nome_empresa else None

        nome_cliente = self.combo_cliente.get().strip()
        id_cliente = next((id for id, nome in self.clientes if nome == nome_cliente), None) if nome_cliente else None

        nome_contato = self.combo_contato.get().strip()
        id_contato = next((id for id, nome in self.contatos if nome == nome_contato), None) if nome_contato else None

        nome_tipo = self.combo_tipo.get().strip()
        id_tipo = next((id for id, nome in self.tipos if nome == nome_tipo), None) if nome_tipo else None

        nome_transp = self.combo_transp.get().strip()
        id_transp = next((id for id, nome in self.transportadoras if nome == nome_transp), None) if nome_transp else None

        # Status e flags
        status = self.combo_status.get()
        fl_mapa = '1' if self.var_mapa.get() else '0'

        if not dt_of or not id_empresa or not id_cliente:
            self.show_message("ATENÇÃO: Preencha os campos obrigatórios (Data OF, Empresa e Cliente).", "warning")
            return

        confirmation_message = f"Confirma a gravação do orçamento para '{nome_cliente}'?"
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('save')

        if not self.request_confirmation('save', confirmation_message, self._execute_save):
            return

    def carregar(self):
        try:
            self.tree.delete(*self.tree.get_children())
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.id_of, e.nm_razao as nm_empresa, c.nm_razao as cliente, o.dt_of, o.dt_vencto,
                       o.nr_pedido_cli, o.vl_total, o.qt_itens, o.fl_status, o.tx_obs
                FROM alba0008 o
                LEFT JOIN empresas e ON o.id_empresa = e.id_empresa
                LEFT JOIN alba0001 c ON o.id_cliente = c.id_pessoa
                ORDER BY o.dt_of DESC, o.id_of DESC
            """)
            resultados = cursor.fetchall()
            for row in resultados:
                # Formatar valores para exibição
                row_formatted = list(row)
                if row[3]:  # dt_of
                    row_formatted[3] = row[3][:10] if len(row[3]) > 10 else row[3]
                if row[4]:  # dt_vencto
                    row_formatted[4] = row[4][:10] if len(row[4]) > 10 else row[4]
                if row[6]:  # vl_total
                    row_formatted[6] = f"{float(row[6]):,.2f}"
                self.tree.insert("", "end", values=row_formatted)
            conn.close()
            self.show_message(f"Carregados {len(resultados)} orçamentos", "success")
        except Exception as e:
            self.show_message(f"ERRO ao carregar orçamentos: {str(e)}", "error")

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return

        id_of = item["values"][0]
        self.current_id = id_of
        
        try:
            # Buscar todos os dados do orçamento selecionado
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, e.nm_razao as nm_empresa, c.nm_razao as cliente_nome, 
                       ct.nm_contato, t.nm_tipo, tr.nm_razao as transp_nome
                FROM alba0008 o
                LEFT JOIN empresas e ON o.id_empresa = e.id_empresa
                LEFT JOIN alba0001 c ON o.id_cliente = c.id_pessoa
                LEFT JOIN contatos ct ON o.id_contato = ct.id_contato
                LEFT JOIN tipo t ON o.id_tipo = t.id_tipo
                LEFT JOIN alba0001 tr ON o.id_transp = tr.id_pessoa
                WHERE o.id_of = ?
            """, (id_of,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                # Sincronizar recnum
                self.current_recnum = result[0]  # recnum é o primeiro campo
                
                # Preencher campos básicos
                self.entry_id_of.config(state="normal")
                self.entry_id_of.delete(0, tk.END)
                self.entry_id_of.insert(0, str(result[1]))  # id_of
                self.entry_id_of.config(state="readonly")
                
                # Datas
                if result[4]:  # dt_of
                    self.entry_dt_of.entry.delete(0, tk.END)
                    self.entry_dt_of.entry.insert(0, result[4][:10])
                
                if result[6]:  # dt_vencto
                    self.entry_dt_vencto.entry.delete(0, tk.END)
                    self.entry_dt_vencto.entry.insert(0, result[6][:10])
                
                # Combos
                self.combo_empresa.set(result[29] or "")  # nm_empresa
                self.combo_cliente.set(result[30] or "")  # cliente_nome
                self.combo_contato.set(result[31] or "")  # nm_contato
                self.combo_tipo.set(result[32] or "")     # nm_tipo
                self.combo_transp.set(result[33] or "")   # transp_nome
                
                # Campos de texto
                self.entry_pedido_cli.delete(0, tk.END)
                self.entry_pedido_cli.insert(0, result[11] or "")  # nr_pedido_cli
                
                self.entry_prazo.delete(0, tk.END)
                self.entry_prazo.insert(0, result[13] or "")  # tx_prazo
                
                self.entry_condicoes.delete(0, tk.END)
                self.entry_condicoes.insert(0, result[14] or "")  # tx_condicoes
                
                # Valores
                self.entry_vl_mercadoria.delete(0, tk.END)
                self.entry_vl_mercadoria.insert(0, str(result[20] or 0))  # vl_mercadoria
                
                self.entry_vl_ipi.delete(0, tk.END)
                self.entry_vl_ipi.insert(0, str(result[21] or 0))  # vl_ipi
                
                self.entry_vl_icms.delete(0, tk.END)
                self.entry_vl_icms.insert(0, str(result[22] or 0))  # vl_icms
                
                self.entry_vl_icmsst.delete(0, tk.END)
                self.entry_vl_icmsst.insert(0, str(result[23] or 0))  # vl_icmsst
                
                self.entry_vl_iss.delete(0, tk.END)
                self.entry_vl_iss.insert(0, str(result[24] or 0))  # vl_iss
                
                self.entry_vl_total.delete(0, tk.END)
                self.entry_vl_total.insert(0, str(result[25] or 0))  # vl_total
                
                self.entry_pc_comissao.delete(0, tk.END)
                self.entry_pc_comissao.insert(0, str(result[18] or 0))  # pc_comissao
                
                self.entry_vl_comissao.delete(0, tk.END)
                self.entry_vl_comissao.insert(0, str(result[19] or 0))  # vl_comissao
                
                self.entry_qt_itens.delete(0, tk.END)
                self.entry_qt_itens.insert(0, str(result[26] or 0))  # qt_itens
                
                # Status
                self.combo_status.set(result[27] or "")  # fl_status
                
                # Flags
                self.var_mapa.set(1 if str(result[28]) == '1' else 0)  # fl_mapa
                
                # Observações
                self.text_obs.delete("1.0", tk.END)
                self.text_obs.insert("1.0", result[15] or "")  # tx_obs
                
                self.show_message(f"Orçamento selecionado: ID {id_of}", "info")
                
        except Exception as e:
            self.show_message(f"ERRO ao carregar dados do orçamento: {str(e)}", "error")

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.current_id = None
        self.current_recnum = None
        
        # Limpar ID
        self.entry_id_of.config(state="normal")
        self.entry_id_of.delete(0, tk.END)
        self.entry_id_of.config(state="readonly")
        
        # Limpar datas
        self.entry_dt_of.entry.delete(0, tk.END)
        self.entry_dt_vencto.entry.delete(0, tk.END)
        
        # Limpar combos
        self.combo_empresa.set("")
        self.combo_cliente.set("")
        self.combo_contato.set("")
        self.combo_tipo.set("")
        self.combo_transp.set("")
        self.combo_status.set("")
        
        # Limpar campos de texto
        self.entry_pedido_cli.delete(0, tk.END)
        self.entry_prazo.delete(0, tk.END)
        self.entry_condicoes.delete(0, tk.END)
        
        # Limpar valores
        self.entry_vl_mercadoria.delete(0, tk.END)
        self.entry_vl_ipi.delete(0, tk.END)
        self.entry_vl_icms.delete(0, tk.END)
        self.entry_vl_icmsst.delete(0, tk.END)
        self.entry_vl_iss.delete(0, tk.END)
        self.entry_vl_total.delete(0, tk.END)
        self.entry_pc_comissao.delete(0, tk.END)
        self.entry_vl_comissao.delete(0, tk.END)
        self.entry_qt_itens.delete(0, tk.END)
        
        # Limpar flags
        self.var_mapa.set(0)
        
        # Limpar observações
        self.text_obs.delete("1.0", tk.END)

    def selecionar_item_por_id(self, id_of):
        """Seleciona um item na lista pelo ID do orçamento"""
        for item in self.tree.get_children():
            valores = self.tree.item(item)["values"]
            if valores and str(valores[0]) == str(id_of):
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)
                break

    def _execute_removal(self, id_of):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alba0008 WHERE id_of = ?", (id_of,))
            conn.commit()
            conn.close()
            self.carregar()
            self.limpar()
            self.show_message(f"Orçamento ID {id_of} removido com sucesso!", "success")
        except Exception as e:
            self.show_message(f"ERRO ao remover orçamento: {str(e)}", "error")

    def remover(self):
        item = self.tree.focus()
        if not item:
            self.show_message("ATENÇÃO: Selecione um orçamento para remover.", "warning")
            return

        id_of = self.tree.item(item)["values"][0]

        confirmation_message = f"Pressione 'Remover' novamente para excluir o orçamento ID {id_of}."

        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('remove')

        if not self.request_confirmation('remove', confirmation_message, self._execute_removal, id_of):
            return

    # Métodos de navegação
    def ir_primeiro(self):
        children = self.tree.get_children()
        if children:
            self.tree.selection_set(children[0])
            self.tree.focus(children[0])
            self.tree.see(children[0])
            self.on_select(None)

    def ir_anterior(self):
        current = self.tree.focus()
        if current:
            prev_item = self.tree.prev(current)
            if prev_item:
                self.tree.selection_set(prev_item)
                self.tree.focus(prev_item)
                self.tree.see(prev_item)
                self.on_select(None)

    def ir_proximo(self):
        current = self.tree.focus()
        if current:
            next_item = self.tree.next(current)
            if next_item:
                self.tree.selection_set(next_item)
                self.tree.focus(next_item)
                self.tree.see(next_item)
                self.on_select(None)

    def ir_ultimo(self):
        children = self.tree.get_children()
        if children:
            self.tree.selection_set(children[-1])
            self.tree.focus(children[-1])
            self.tree.see(children[-1])
            self.on_select(None)
