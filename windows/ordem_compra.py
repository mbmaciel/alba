import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

DB_PATH = "alba_zip_extracted/alba.sqlite"

class OrdemCompraWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Ordens de Compra (alba0010)")
        self.geometry("1000x550")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # ID Empresa
        ttkb.Label(frame, text="Empresa").grid(row=0, column=0, sticky=tk.W)
        self.combo_empresa = ttkb.Combobox(frame, width=40, state="readonly")
        self.combo_empresa.grid(row=0, column=1, columnspan=2, pady=5)

        # ID Cliente
        ttkb.Label(frame, text="Cliente").grid(row=0, column=3, sticky=tk.W)
        self.combo_cliente = ttkb.Combobox(frame, width=40, state="readonly")
        self.combo_cliente.grid(row=0, column=4, columnspan=2, pady=5)

        # Data
        ttkb.Label(frame, text="Data").grid(row=0, column=6, sticky=tk.W)
        self.entry_data = ttkb.Entry(frame, width=15)
        self.entry_data.grid(row=0, column=7, pady=5)
        self.entry_data.insert(0, datetime.today().strftime("%Y-%m-%d"))

        # Contato
        ttkb.Label(frame, text="Contato").grid(row=1, column=0, sticky=tk.W)
        self.combo_contato = ttkb.Combobox(frame, width=40, state="readonly")
        self.combo_contato.grid(row=1, column=1, columnspan=2, pady=5)

        # Pedido Cliente
        ttkb.Label(frame, text="Pedido Cliente").grid(row=1, column=3, sticky=tk.W)
        self.entry_pedido = ttkb.Entry(frame, width=20)
        self.entry_pedido.grid(row=1, column=4, pady=5)

        # Status
        ttkb.Label(frame, text="Status").grid(row=1, column=6, sticky=tk.W)
        self.entry_status = ttkb.Entry(frame, width=15)
        self.entry_status.grid(row=1, column=7, pady=5)

        # Prazo
        ttkb.Label(frame, text="Prazo").grid(row=2, column=0, sticky=tk.W)
        self.entry_prazo = ttkb.Entry(frame, width=25)
        self.entry_prazo.grid(row=2, column=1, columnspan=2, pady=5)

        # Condições
        ttkb.Label(frame, text="Condições").grid(row=2, column=3, sticky=tk.W)
        self.entry_condicoes = ttkb.Entry(frame, width=30)
        self.entry_condicoes.grid(row=2, column=4, columnspan=2, pady=5)

        # Observações
        ttkb.Label(frame, text="Observações").grid(row=3, column=0, sticky=tk.W)
        self.entry_obs = ttkb.Entry(frame, width=70)
        self.entry_obs.grid(row=3, column=1, columnspan=5, pady=5, sticky=tk.W)

        # Valor Total
        ttkb.Label(frame, text="Valor Total").grid(row=3, column=6, sticky=tk.W)
        self.entry_total = ttkb.Entry(frame, width=15)
        self.entry_total.grid(row=3, column=7, pady=5)

        ttkb.Button(frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).grid(row=4, column=6, pady=10, sticky=tk.E)
        ttkb.Button(frame, text="Remover", command=self.remover, bootstyle=DANGER).grid(row=4, column=7, sticky=tk.W)

        # Frame para botões de navegação
        nav_frame = ttkb.Frame(self, padding=5)
        nav_frame.pack(fill=tk.X, padx=10)

        # Botões de navegação
        ttkb.Button(nav_frame, text="⏮ Primeiro", command=self.ir_primeiro, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="◀ Anterior", command=self.ir_anterior, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Próximo ▶", command=self.ir_proximo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Último ⏭", command=self.ir_ultimo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)

        self.tree = ttkb.Treeview(self, columns=("id", "cliente", "contato", "data", "pedido", "status", "total"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
            
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.heading("id", text="")
            
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_empresas()
        self.carregar_clientes()
        self.carregar_contatos()
        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

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
        
    def salvar(self):
        nome_empresa = self.combo_empresa.get()
        id_empresa = next((id for id, nome in self.empresas if nome == nome_empresa), None)

        nome_cliente = self.combo_cliente.get()
        id_cliente = next((id for id, nome in self.clientes if nome == nome_cliente), None)

        nome_contato = self.combo_contato.get()
        id_contato = next((id for id, nome in self.contatos if nome == nome_contato), None)

        data = (
            id_empresa,
            id_cliente,
            self.entry_data.get(),
            id_contato,
            self.entry_pedido.get(),
            self.entry_prazo.get(),
            self.entry_condicoes.get(),
            self.entry_obs.get(),
            self.entry_total.get(),
            self.entry_status.get()
        )

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alba0010 (
                id_empresa, id_cliente, dt_oc, id_contato, nr_pedido_cli,
                tx_prazo, tx_condicoes, tx_obs, vl_total, fl_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

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
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        values = item.get("values", [])
        if len(values) < 7:
            return
        _, cliente_nome, contato_nome, data, pedido, status, total = values

        self.combo_cliente.set(cliente_nome or "")
        self.combo_contato.set(contato_nome or "")
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, data)
        self.entry_pedido.delete(0, tk.END)
        self.entry_pedido.insert(0, pedido)
        self.entry_status.delete(0, tk.END)
        self.entry_status.insert(0, status)
        self.entry_total.delete(0, tk.END)
        self.entry_total.insert(0, total)

    def limpar(self):
        self.combo_empresa.set("")
        self.combo_cliente.set("")
        self.combo_contato.set("")
        self.entry_data.delete(0, tk.END)
        self.entry_pedido.delete(0, tk.END)
        self.entry_status.delete(0, tk.END)
        self.entry_total.delete(0, tk.END)
        self.entry_prazo.delete(0, tk.END)
        self.entry_condicoes.delete(0, tk.END)
        self.entry_obs.delete(0, tk.END)
        
    def ir_primeiro(self):
        """Navega para o primeiro registro na lista"""
        items = self.tree.get_children()
        if items:
            primeiro_item = items[0]
            self.tree.selection_set(primeiro_item)
            self.tree.focus(primeiro_item)
            self.tree.see(primeiro_item)
            self.on_select(None)
            
    def ir_ultimo(self):
        """Navega para o último registro na lista"""
        items = self.tree.get_children()
        if items:
            ultimo_item = items[-1]
            self.tree.selection_set(ultimo_item)
            self.tree.focus(ultimo_item)
            self.tree.see(ultimo_item)
            self.on_select(None)
            
    def ir_anterior(self):
        """Navega para o registro anterior na lista"""
        selecionado = self.tree.selection()
        if not selecionado:
            self.ir_primeiro()
            return
            
        items = self.tree.get_children()
        idx = items.index(selecionado[0])
        
        if idx > 0:
            anterior = items[idx - 1]
            self.tree.selection_set(anterior)
            self.tree.focus(anterior)
            self.tree.see(anterior)
            self.on_select(None)
            
    def ir_proximo(self):
        """Navega para o próximo registro na lista"""
        selecionado = self.tree.selection()
        if not selecionado:
            self.ir_primeiro()
            return
            
        items = self.tree.get_children()
        idx = items.index(selecionado[0])
        
        if idx < len(items) - 1:
            proximo = items[idx + 1]
            self.tree.selection_set(proximo)
            self.tree.focus(proximo)
            self.tree.see(proximo)
            self.on_select(None)
