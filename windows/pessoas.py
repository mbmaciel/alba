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
        self.geometry("1100x700")
        self.resizable(False, False)

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
        ttkb.Label(input_frame, text="Tipo (F/J)").grid(row=0, column=0, sticky=tk.W)
        self.combo_tipo_pessoa = ttkb.Combobox(input_frame, width=5, state="readonly", values=["F", "J"])
        self.combo_tipo_pessoa.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="CNPJ/CPF").grid(row=0, column=2, sticky=tk.W)
        self.entry_doc = ttkb.Entry(input_frame, width=20)
        self.entry_doc.grid(row=0, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Telefone").grid(row=0, column=4, sticky=tk.W)
        self.entry_tel = ttkb.Entry(input_frame, width=20)
        self.entry_tel.grid(row=0, column=5, pady=5, padx=5)

        # Segunda linha
        ttkb.Label(input_frame, text="Razão Social / Nome").grid(row=1, column=0, sticky=tk.W)
        self.entry_razao = ttkb.Entry(input_frame, width=50)
        self.entry_razao.grid(row=1, column=1, columnspan=3, pady=5, padx=(5, 20), sticky=tk.W+tk.E)

        ttkb.Label(input_frame, text="Email").grid(row=1, column=4, sticky=tk.W)
        self.entry_email = ttkb.Entry(input_frame, width=30)
        self.entry_email.grid(row=1, column=5, pady=5, padx=5)

        # Terceira linha
        ttkb.Label(input_frame, text="Nome Fantasia").grid(row=2, column=0, sticky=tk.W)
        self.entry_fantasia = ttkb.Entry(input_frame, width=50)
        self.entry_fantasia.grid(row=2, column=1, columnspan=5, pady=5, padx=(5, 0), sticky=tk.W+tk.E)

        # Quarta linha - Combos
        ttkb.Label(input_frame, text="Tipo de Pessoa").grid(row=3, column=0, sticky=tk.W)
        self.combo_tipo = ttkb.Combobox(input_frame, width=25, state="readonly")
        self.combo_tipo.grid(row=3, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Atividade").grid(row=3, column=2, sticky=tk.W)
        self.combo_atividade = ttkb.Combobox(input_frame, width=25, state="readonly")
        self.combo_atividade.grid(row=3, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Transportadora").grid(row=3, column=4, sticky=tk.W)
        self.combo_transp = ttkb.Combobox(input_frame, width=25, state="readonly")
        self.combo_transp.grid(row=3, column=5, pady=5, padx=5)

        # Quinta linha - Checkboxes
        checkbox_frame = ttkb.Frame(input_frame)
        checkbox_frame.grid(row=4, column=0, columnspan=6, pady=10, sticky=tk.W)

        self.var_cliente = tk.IntVar()
        self.var_fornec = tk.IntVar()
        self.var_transp = tk.IntVar()
        self.var_ativo = tk.IntVar()

        ttkb.Checkbutton(checkbox_frame, text="Cliente", variable=self.var_cliente).pack(side=tk.LEFT, padx=(0, 20))
        ttkb.Checkbutton(checkbox_frame, text="Fornecedor", variable=self.var_fornec).pack(side=tk.LEFT, padx=(0, 20))
        ttkb.Checkbutton(checkbox_frame, text="Transportadora", variable=self.var_transp).pack(side=tk.LEFT, padx=(0, 20))
        ttkb.Checkbutton(checkbox_frame, text="Ativo", variable=self.var_ativo).pack(side=tk.LEFT)

        # Configurar expansão das colunas
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "tipo", "razao", "cnpj", "telefone", "cliente", "fornec", "ativo", "atividade", "transp", "tipo_nome"), show="headings", height=15)
            
        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("razao", text="Razão Social")
        self.tree.heading("cnpj", text="CNPJ/CPF")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("fornec", text="Fornecedor")
        self.tree.heading("ativo", text="Ativo")
        self.tree.heading("atividade", text="Atividade")
        self.tree.heading("transp", text="Transportadora")
        self.tree.heading("tipo_nome", text="Tipo Pessoa")
            
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("tipo", width=60, minwidth=50, anchor=tk.CENTER)
        self.tree.column("razao", width=200, minwidth=150, anchor=tk.W)
        self.tree.column("cnpj", width=120, minwidth=100, anchor=tk.CENTER)
        self.tree.column("telefone", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column("cliente", width=60, minwidth=50, anchor=tk.CENTER)
        self.tree.column("fornec", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("ativo", width=60, minwidth=50, anchor=tk.CENTER)
        self.tree.column("atividade", width=120, minwidth=100, anchor=tk.W)
        self.tree.column("transp", width=120, minwidth=100, anchor=tk.W)
        self.tree.column("tipo_nome", width=100, minwidth=80, anchor=tk.W)
            
        # Scrollbar para o Treeview
        scrollbar = ttkb.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
            
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_tipos()
        self.carregar_atividades()
        self.carregar_transportadoras()
        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar()
        self.combo_tipo_pessoa.focus()

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
        tipo = self.combo_tipo_pessoa.get().upper()
        razao = self.entry_razao.get()
        fantasia = self.entry_fantasia.get()
        cnpj = self.entry_doc.get()
        telefone = self.entry_tel.get()
        email = self.entry_email.get()

        # Corrigido para salvar como "1" ou "0"
        fl_cliente = '1' if self.var_cliente.get() else '0'
        fl_fornec = '1' if self.var_fornec.get() else '0'
        fl_transp = '1' if self.var_transp.get() else '0'
        fl_ativo = '1' if self.var_ativo.get() else '0'

        nome_tipo = self.combo_tipo.get()
        id_tipo = next((id for id, nome in self.tipos if nome == nome_tipo), None) if nome_tipo else None

        nome_atividade = self.combo_atividade.get()
        id_atividade = next((id for id, nome in self.atividades if nome == nome_atividade), None) if nome_atividade else None

        nome_transp = self.combo_transp.get()
        id_transp = next((id for id, nome in self.transportadoras if nome == nome_transp), None) if nome_transp else None

        if not razao or not tipo:
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios (Razão Social e Tipo).")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        
        try:
            # Get the next recnum value
            cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM alba0001")
            next_recnum = cursor.fetchone()[0]
            
            # Get the next id_pessoa value
            cursor.execute("SELECT COALESCE(MAX(id_pessoa), 0) + 1 FROM alba0001")
            next_id_pessoa = cursor.fetchone()[0]
            
            # Get the next id_antigo value
            cursor.execute("SELECT COALESCE(MAX(id_antigo), 0) + 1 FROM alba0001")
            next_id_antigo = cursor.fetchone()[0]
            
            # Build the base INSERT with required fields
            columns = ["id_pessoa", "id_antigo", "recnum", "tp_pessoa", "nm_razao"]
            values = [next_id_pessoa, next_id_antigo, next_recnum, tipo, razao]
            
            # Add optional fields if they have values
            if fantasia:
                columns.append("nm_fantasia")
                values.append(fantasia)
            
            if cnpj:
                columns.append("nr_cnpj_cpf")
                values.append(cnpj)
            
            if telefone:
                columns.append("nr_telefone")
                values.append(telefone)
            
            if email:
                columns.append("nm_email")
                values.append(email)
            
            # Add flag fields
            columns.extend(["fl_cliente", "fl_fornec", "fl_transp", "fl_ativo"])
            values.extend([fl_cliente, fl_fornec, fl_transp, fl_ativo])
            
            # Add foreign key fields only if they have values
            if id_tipo is not None:
                columns.append("id_tipo")
                values.append(id_tipo)
            
            if id_atividade is not None:
                columns.append("id_atividade")
                values.append(id_atividade)
            
            if id_transp is not None:
                columns.append("id_transp")
                values.append(id_transp)
            
            placeholders = ["?" for _ in values]
            sql = f"INSERT INTO alba0001 ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
            
            cursor.execute(sql, values)
            conn.commit()
            self.limpar()
            self.carregar()
            messagebox.showinfo("Sucesso", "Pessoa salva com sucesso!")
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
        finally:
            conn.close()

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
            ORDER BY p.nm_razao
        """)
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        
        id_pessoa = item["values"][0]
        
        # Buscar todos os dados da pessoa selecionada
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.tp_pessoa, p.nm_razao, p.nm_fantasia, p.nr_cnpj_cpf,
                   p.nr_telefone, p.nm_email,
                   p.fl_cliente, p.fl_fornec, p.fl_transp, p.fl_ativo,
                   p.id_tipo, p.id_atividade, p.id_transp,
                   tp.nm_tipo, a.nm_atividade, t.nm_razao as transp_nome
            FROM alba0001 p
            LEFT JOIN tipo tp ON p.id_tipo = tp.id_tipo
            LEFT JOIN ativid a ON p.id_atividade = a.id_atividade
            LEFT JOIN alba0001 t ON p.id_transp = t.id_pessoa
            WHERE p.id_pessoa = ?
        """, (id_pessoa,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            (tipo, razao, fantasia, cnpj, telefone, email,
             fl_cliente, fl_fornec, fl_transp, fl_ativo,
             id_tipo, id_atividade, id_transp,
             nome_tipo, nome_atividade, nome_transp) = result
            
            # Preencher os campos
            self.combo_tipo_pessoa.set(tipo or "")
            
            self.entry_razao.delete(0, tk.END)
            self.entry_razao.insert(0, razao or "")
            
            self.entry_fantasia.delete(0, tk.END)
            self.entry_fantasia.insert(0, fantasia or "")
            
            self.entry_doc.delete(0, tk.END)
            self.entry_doc.insert(0, cnpj or "")
            
            self.entry_tel.delete(0, tk.END)
            self.entry_tel.insert(0, telefone or "")
            
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, email or "")
            
            # Preencher combos
            self.combo_tipo.set(nome_tipo or "")
            self.combo_atividade.set(nome_atividade or "")
            self.combo_transp.set(nome_transp or "")
            
            # Preencher checkboxes - corrigido para tratar valores "1" e "0"
            self.var_cliente.set(1 if str(fl_cliente) == '1' else 0)
            self.var_fornec.set(1 if str(fl_fornec) == '1' else 0)
            self.var_transp.set(1 if str(fl_transp) == '1' else 0)
            self.var_ativo.set(1 if str(fl_ativo) == '1' else 0)

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.combo_tipo_pessoa.set("")  # Mudança aqui
        self.entry_razao.delete(0, tk.END)
        self.entry_fantasia.delete(0, tk.END)
        self.entry_doc.delete(0, tk.END)
        self.entry_tel.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        
        self.combo_tipo.set("")
        self.combo_atividade.set("")
        self.combo_transp.set("")
        
        self.var_cliente.set(0)
        self.var_fornec.set(0)
        self.var_transp.set(0)
        self.var_ativo.set(0)

    def remover(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione uma pessoa para remover.")
            return
                
        id_pessoa = self.tree.item(item)["values"][0]
            
        resposta = messagebox.askyesno("Confirmar", "Deseja realmente remover esta pessoa?")
        if not resposta:
            return
                
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alba0001 WHERE id_pessoa = ?", (id_pessoa,))
        conn.commit()
        conn.close()
        self.carregar()
        self.limpar()
        messagebox.showinfo("Sucesso", "Pessoa removida com sucesso!")

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