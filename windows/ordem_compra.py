import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from windows.base_window import BaseWindow

class OrdemCompraWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.set_title("Cadastro de Ordens de Compra (alba0010)")
        self.config(width=1000, height=650)

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

        self.btn_salvar = ttkb.Button(button_container, text="💾", command=self.salvar, width=3)
        self.btn_salvar.pack(side=tk.LEFT)

        self.btn_remover = ttkb.Button(button_container, text="🗑️", command=self.remover, width=3)
        self.btn_remover.pack(side=tk.LEFT)

        # Separador visual
        separator = ttkb.Separator(toolbar_frame, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

        # Botões de navegação
        nav_container = ttkb.Frame(toolbar_frame)
        nav_container.pack(side=tk.LEFT, padx=(10, 0))

        ttkb.Button(nav_container, text="⏮", command=self.ir_primeiro, width=3).pack(side=tk.LEFT)
        ttkb.Button(nav_container, text="◀", command=self.ir_anterior, width=3).pack(side=tk.LEFT)
        ttkb.Button(nav_container, text="▶", command=self.ir_proximo, width=3).pack(side=tk.LEFT)
        ttkb.Button(nav_container, text="⏭", command=self.ir_ultimo, width=3).pack(side=tk.LEFT)

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
        self.tree.heading("id", text="ID")
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
        scrollbar = ttkb.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
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
        
    def salvar(self):
        try:
            # Validações básicas
            if not self.combo_empresa.get():
                messagebox.showerror("Erro", "Selecione uma empresa")
                return
            if not self.combo_cliente.get():
                messagebox.showerror("Erro", "Selecione um cliente")
                return

            nome_empresa = self.combo_empresa.get()
            id_empresa = next((id for id, nome in self.empresas if nome == nome_empresa), None)

            nome_cliente = self.combo_cliente.get()
            id_cliente = next((id for id, nome in self.clientes if nome == nome_cliente), None)

            # Tratar contato como opcional - se não selecionado, usar None ou um valor padrão
            nome_contato = self.combo_contato.get()
            if nome_contato:
                id_contato = next((id for id, nome in self.contatos if nome == nome_contato), None)
            else:
                # Se o campo é obrigatório no banco, você pode:
                # 1. Criar um contato padrão ou
                # 2. Exigir seleção de contato
                # Por enquanto, vamos exigir a seleção:
                messagebox.showerror("Erro", "Selecione um contato")
                return

            # Converter data para formato do banco
            data_bd = self.converter_data_para_bd(self.entry_data.get())

            # Obter próximo recnum
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM alba0010")
            recnum = cursor.fetchone()[0]

            data = (
                recnum,
                id_empresa,
                id_cliente,
                data_bd,
                id_contato,  # Agora sempre terá um valor válido
                self.entry_pedido.get(),
                self.entry_prazo.get(),
                self.entry_condicoes.get(),
                self.entry_obs.get(),
                self.entry_total.get(),
                self.combo_status.get()
            )

            cursor.execute("""
                INSERT INTO alba0010 (
                    recnum, id_empresa, id_cliente, dt_oc, id_contato, nr_pedido_cli,
                    tx_prazo, tx_condicoes, tx_obs, vl_total, fl_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Ordem de compra salva com sucesso!")
            self.limpar()
            self.carregar()

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar ordem de compra: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        id_oc = self.tree.item(item)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alba0010 WHERE id_oc = ?", (id_oc,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.id_oc, c.nm_razao AS cliente, ct.nm_contato, o.dt_oc,
                   o.nr_pedido_cli, o.fl_status, o.vl_total
            FROM alba0010 o
            LEFT JOIN alba0001 c ON o.id_cliente = c.id_pessoa
            LEFT JOIN contatos ct ON o.id_contato = ct.id_contato
        """)
        for row in cursor.fetchall():
            # Converter data para formato brasileiro na exibição
            row_list = list(row)
            if row_list[3]:  # Se tem data
                row_list[3] = self.converter_data_para_br(row_list[3])
            self.tree.insert("", "end", values=row_list)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        values = item.get("values", [])
        if len(values) < 7:
            return
        
        id_oc = values[0]
        
        # Buscar todos os dados da ordem de compra selecionada
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.id_empresa, o.id_cliente, o.dt_oc, o.id_contato, 
                   o.nr_pedido_cli, o.fl_status, o.vl_total, o.tx_prazo, 
                   o.tx_condicoes, o.tx_obs,
                   e.nm_razao AS empresa_nome,
                   c.nm_razao AS cliente_nome,
                   ct.nm_contato AS contato_nome
            FROM alba0010 o
            LEFT JOIN empresas e ON o.id_empresa = e.id_empresa
            LEFT JOIN alba0001 c ON o.id_cliente = c.id_pessoa
            LEFT JOIN contatos ct ON o.id_contato = ct.id_contato
            WHERE o.id_oc = ?
        """, (id_oc,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            (id_empresa, id_cliente, data, id_contato, pedido, status, total, 
             prazo, condicoes, obs, empresa_nome, cliente_nome, contato_nome) = result
            
            # Preencher os campos
            self.combo_empresa.set(empresa_nome or "")
            self.combo_cliente.set(cliente_nome or "")
            self.combo_contato.set(contato_nome or "")
            
            self.entry_data.delete(0, tk.END)
            # Converter data para formato brasileiro
            data_br = self.converter_data_para_br(data) if data else ""
            self.entry_data.insert(0, data_br)
            
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
        
