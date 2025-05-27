import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class PessoaWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Pessoas (alba0001)")
        self.geometry("1050x650")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttkb.Label(frame, text="Tipo (F/J)").grid(row=0, column=0, sticky=tk.W)
        self.entry_tipo = ttkb.Entry(frame, width=5)
        self.entry_tipo.grid(row=0, column=1, sticky=tk.W)

        ttkb.Label(frame, text="Razão Social / Nome").grid(row=1, column=0, sticky=tk.W)
        self.entry_razao = ttkb.Entry(frame, width=40)
        self.entry_razao.grid(row=1, column=1, columnspan=2, pady=5, sticky=tk.W)

        ttkb.Label(frame, text="Nome Fantasia").grid(row=2, column=0, sticky=tk.W)
        self.entry_fantasia = ttkb.Entry(frame, width=40)
        self.entry_fantasia.grid(row=2, column=1, columnspan=2, pady=5, sticky=tk.W)

        ttkb.Label(frame, text="CNPJ/CPF").grid(row=0, column=2, sticky=tk.W)
        self.entry_doc = ttkb.Entry(frame, width=20)
        self.entry_doc.grid(row=0, column=3, sticky=tk.W)

        ttkb.Label(frame, text="Telefone").grid(row=1, column=2, sticky=tk.W)
        self.entry_tel = ttkb.Entry(frame, width=20)
        self.entry_tel.grid(row=1, column=3, sticky=tk.W)

        ttkb.Label(frame, text="Email").grid(row=2, column=2, sticky=tk.W)
        self.entry_email = ttkb.Entry(frame, width=30)
        self.entry_email.grid(row=2, column=3, sticky=tk.W)

        ttkb.Label(frame, text="Tipo de Pessoa").grid(row=3, column=0, sticky=tk.W)
        self.combo_tipo = ttkb.Combobox(frame, width=40, state="readonly")
        self.combo_tipo.grid(row=3, column=1, columnspan=2, sticky=tk.W)

        ttkb.Label(frame, text="Atividade").grid(row=4, column=0, sticky=tk.W)
        self.combo_atividade = ttkb.Combobox(frame, width=40, state="readonly")
        self.combo_atividade.grid(row=4, column=1, columnspan=2, sticky=tk.W)

        ttkb.Label(frame, text="Transportadora").grid(row=5, column=0, sticky=tk.W)
        self.combo_transp = ttkb.Combobox(frame, width=40, state="readonly")
        self.combo_transp.grid(row=5, column=1, columnspan=2, sticky=tk.W)

        self.var_cliente = tk.IntVar()
        self.var_fornec = tk.IntVar()
        self.var_transp = tk.IntVar()
        self.var_ativo = tk.IntVar()

        ttkb.Checkbutton(frame, text="Cliente", variable=self.var_cliente).grid(row=6, column=0, sticky=tk.W)
        ttkb.Checkbutton(frame, text="Fornecedor", variable=self.var_fornec).grid(row=6, column=1, sticky=tk.W)
        ttkb.Checkbutton(frame, text="Transportadora", variable=self.var_transp).grid(row=6, column=2, sticky=tk.W)
        ttkb.Checkbutton(frame, text="Ativo", variable=self.var_ativo).grid(row=6, column=3, sticky=tk.W)

        ttkb.Button(frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).grid(row=7, column=2, pady=10)
        ttkb.Button(frame, text="Remover", command=self.remover, bootstyle=DANGER).grid(row=7, column=3)

        # Frame para botões de navegação
        nav_frame = ttkb.Frame(self, padding=5)
        nav_frame.pack(fill=tk.X, padx=10)

        # Botões de navegação
        ttkb.Button(nav_frame, text="⏮ Primeiro", command=self.ir_primeiro, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="◀ Anterior", command=self.ir_anterior, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Próximo ▶", command=self.ir_proximo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Último ⏭", command=self.ir_ultimo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)

        self.tree = ttkb.Treeview(self, columns=("id", "tipo", "razao", "cnpj", "telefone", "cliente", "fornec", "ativo", "atividade", "transp", "tipo_nome"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())

        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.heading("id", text="")

        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_tipos()
        self.carregar_atividades()
        self.carregar_transportadoras()
        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def carregar_tipos(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_tipo, nm_tipo FROM tipo ORDER BY nm_tipo")
        self.tipos = cursor.fetchall()
        conn.close()
        self.combo_tipo["values"] = [nome for _, nome in self.tipos]

    def carregar_atividades(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_atividade, nm_atividade FROM ativid ORDER BY nm_atividade")
        self.atividades = cursor.fetchall()
        conn.close()
        self.combo_atividade["values"] = [nome for _, nome in self.atividades]

    def carregar_transportadoras(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_pessoa, nm_razao FROM alba0001
            WHERE fl_transp = 'S' OR fl_transp = '1'
            ORDER BY nm_razao
        """)
        self.transportadoras = cursor.fetchall()
        conn.close()
        self.combo_transp["values"] = [nome for _, nome in self.transportadoras]

    def salvar(self):
        tipo = self.entry_tipo.get().upper()
        razao = self.entry_razao.get()
        fantasia = self.entry_fantasia.get()
        cnpj = self.entry_doc.get()
        telefone = self.entry_tel.get()
        email = self.entry_email.get()

        fl_cliente = 'S' if self.var_cliente.get() else 'N'
        fl_fornec = 'S' if self.var_fornec.get() else 'N'
        fl_transp = 'S' if self.var_transp.get() else 'N'
        fl_ativo = 'S' if self.var_ativo.get() else 'N'

        nome_tipo = self.combo_tipo.get()
        id_tipo = next((id for id, nome in self.tipos if nome == nome_tipo), None)

        nome_atividade = self.combo_atividade.get()
        id_atividade = next((id for id, nome in self.atividades if nome == nome_atividade), None)

        nome_transp = self.combo_transp.get()
        id_transp = next((id for id, nome in self.transportadoras if nome == nome_transp), None)

        if not razao or not tipo:
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alba0001 (
                tp_pessoa, nm_razao, nm_fantasia, nr_cnpj_cpf,
                nr_telefone, nm_email,
                fl_cliente, fl_fornec, fl_transp, fl_ativo,
                id_tipo, id_atividade, id_transp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tipo, razao, fantasia, cnpj,
            telefone, email,
            fl_cliente, fl_fornec, fl_transp, fl_ativo,
            id_tipo, id_atividade, id_transp
        ))
        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id_pessoa, p.tp_pessoa, p.nm_razao, p.nr_cnpj_cpf,
                   p.nr_telefone, p.fl_cliente, p.fl_fornec, p.fl_ativo,
                   a.nm_atividade, t.nm_razao as transp_nome, tp.nm_tipo
            FROM alba0001 p
            LEFT JOIN ativid a ON p.id_atividade = a.id_atividade
            LEFT JOIN alba0001 t ON p.id_transp = t.id_pessoa
            LEFT JOIN tipo tp ON p.id_tipo = tp.id_tipo
        """)
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        values = item.get("values", [])
        if len(values) < 11:
            return

        _, tipo, razao, cnpj, tel, cliente, fornec, ativo, atividade, transp, tipo_nome = values

        self.entry_tipo.delete(0, tk.END)
        self.entry_tipo.insert(0, tipo)
        self.entry_razao.delete(0, tk.END)
        self.entry_razao.insert(0, razao)
        self.entry_doc.delete(0, tk.END)
        self.entry_doc.insert(0, cnpj)
        self.entry_tel.delete(0, tk.END)
        self.entry_tel.insert(0, tel)

        self.var_cliente.set(1 if cliente in ['S', '1'] else 0)
        self.var_fornec.set(1 if fornec in ['S', '1'] else 0)
        self.var_ativo.set(1 if ativo in ['S', '1'] else 0)

        self.combo_atividade.set(atividade or "")
        self.combo_transp.set(transp or "")
        self.combo_tipo.set(tipo_nome or "")

    def limpar(self):
        for entry in [self.entry_tipo, self.entry_razao, self.entry_fantasia,
                      self.entry_doc, self.entry_tel, self.entry_email]:
            entry.delete(0, tk.END)

        for combo in [self.combo_tipo, self.combo_atividade, self.combo_transp]:
            combo.set("")

        for var in [self.var_cliente, self.var_fornec, self.var_transp, self.var_ativo]:
            var.set(0)

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        id_pessoa = self.tree.item(item)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alba0001 WHERE id_pessoa = ?", (id_pessoa,))
        conn.commit()
        conn.close()
        self.carregar()
        
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