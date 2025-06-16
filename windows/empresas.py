import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class EmpresaWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Cadastro de Empresas")
        self.config(width=900, height=700)

        # Frame principal
        main_frame = ttkb.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para toolbar e mensagens
        top_frame = ttkb.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 15))

        # Barra de ferramentas no topo
        toolbar_frame = ttkb.Frame(top_frame, relief="raised", borderwidth=2, padding=5)
        toolbar_frame.pack(side=tk.LEFT, fill=tk.X)

        # Frame para mensagens
        message_frame = ttkb.Frame(top_frame, padding=5)
        message_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # Label para mensagens
        self.message_label = ttkb.Label(message_frame, text="")
        self.message_label.pack(fill=tk.X)

        # Container para os botões grudados
        button_container = ttkb.Frame(toolbar_frame)
        button_container.pack(side=tk.LEFT)

        # Botões da barra de ferramentas com ícones
        self.btn_novo = ttkb.Button(button_container, text="➕", command=self.novo, width=3)
        self.btn_novo.pack(side=tk.LEFT)

        self.btn_salvar = ttkb.Button(button_container, text="💾", command=self.salvar_empresa, width=3)
        self.btn_salvar.pack(side=tk.LEFT)

        self.btn_remover = ttkb.Button(button_container, text="🗑️", command=self.remover_empresa, width=3)
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

        # Notebook para as abas
        self.notebook = ttkb.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Aba Dados Básicos
        self.frame_basico = ttkb.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_basico, text='Dados Básicos')

        ttkb.Label(self.frame_basico, text="Razão Social").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_razao = ttkb.Entry(self.frame_basico, width=60)
        self.entry_razao.grid(row=0, column=1, columnspan=3, pady=5, padx=(5, 0), sticky=tk.W+tk.E)

        ttkb.Label(self.frame_basico, text="Nome Fantasia").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_fantasia = ttkb.Entry(self.frame_basico, width=60)
        self.entry_fantasia.grid(row=1, column=1, columnspan=3, pady=5, padx=(5, 0), sticky=tk.W+tk.E)

        ttkb.Label(self.frame_basico, text="CNPJ").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_cnpj = ttkb.Entry(self.frame_basico, width=25)
        self.entry_cnpj.grid(row=2, column=1, pady=5, padx=(5, 20))

        ttkb.Label(self.frame_basico, text="Inscrição Estadual").grid(row=2, column=2, sticky=tk.W, pady=5)
        self.entry_ie = ttkb.Entry(self.frame_basico, width=25)
        self.entry_ie.grid(row=2, column=3, pady=5, padx=(5, 0))

        ttkb.Label(self.frame_basico, text="Inscrição Municipal").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_im = ttkb.Entry(self.frame_basico, width=25)
        self.entry_im.grid(row=3, column=1, pady=5, padx=(5, 0))

        # Configurar expansão das colunas
        self.frame_basico.grid_columnconfigure(1, weight=1)
        self.frame_basico.grid_columnconfigure(3, weight=1)

        # Aba Endereço
        self.frame_endereco = ttkb.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_endereco, text='Endereço')

        ttkb.Label(self.frame_endereco, text="CEP").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_cep = ttkb.Entry(self.frame_endereco, width=15)
        self.entry_cep.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(self.frame_endereco, text="Número").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.entry_numero = ttkb.Entry(self.frame_endereco, width=10)
        self.entry_numero.grid(row=0, column=3, pady=5, padx=(5, 0))

        ttkb.Label(self.frame_endereco, text="Complemento").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_complemento = ttkb.Entry(self.frame_endereco, width=50)
        self.entry_complemento.grid(row=1, column=1, columnspan=3, pady=5, padx=(5, 0), sticky=tk.W+tk.E)

        # Configurar expansão das colunas
        self.frame_endereco.grid_columnconfigure(1, weight=1)

        # Aba JUCESP
        self.frame_jucesp = ttkb.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_jucesp, text='JUCESP')

        ttkb.Label(self.frame_jucesp, text="Nº JUCESP Cadastro").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_jucesp_cad = ttkb.Entry(self.frame_jucesp, width=25)
        self.entry_jucesp_cad.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(self.frame_jucesp, text="Data Cadastro").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.entry_dt_cad = ttkb.Entry(self.frame_jucesp, width=20)
        self.entry_dt_cad.grid(row=0, column=3, pady=5, padx=(5, 0))

        ttkb.Label(self.frame_jucesp, text="Nº JUCESP Alteração").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_jucesp_alt = ttkb.Entry(self.frame_jucesp, width=25)
        self.entry_jucesp_alt.grid(row=1, column=1, pady=5, padx=(5, 20))

        ttkb.Label(self.frame_jucesp, text="Data Alteração").grid(row=1, column=2, sticky=tk.W, pady=5)
        self.entry_dt_alt = ttkb.Entry(self.frame_jucesp, width=20)
        self.entry_dt_alt.grid(row=1, column=3, pady=5, padx=(5, 0))

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "razao", "fantasia", "cnpj"), show="headings", height=12)
            
        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("razao", text="Razão Social")
        self.tree.heading("fantasia", text="Nome Fantasia")
        self.tree.heading("cnpj", text="CNPJ")
            
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("razao", width=300, minwidth=200, anchor=tk.W)
        self.tree.column("fantasia", width=250, minwidth=150, anchor=tk.W)
        self.tree.column("cnpj", width=150, minwidth=120, anchor=tk.CENTER)
            
        # Scrollbar para o Treeview
        scrollbar = ttkb.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
            
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_empresas()

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar_campos()
        self.entry_razao.focus()

    def salvar_empresa(self):
        dados = (
            self.entry_razao.get(),
            self.entry_fantasia.get(),
            self.entry_cnpj.get(),
            self.entry_ie.get(),
            self.entry_im.get(),
            self.entry_cep.get(),
            self.entry_numero.get(),
            self.entry_complemento.get(),
            self.entry_jucesp_cad.get(),
            self.entry_dt_cad.get(),
            self.entry_jucesp_alt.get(),
            self.entry_dt_alt.get()
        )

        if not dados[0] or not dados[2]:
            self.show_message("Preencha os campos obrigatórios: Razão Social e CNPJ.", "warning")
            return

        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO empresas (nm_razao, nm_fantasia, nr_cnpj, nr_ie, nr_im, cd_cep,
                                    nr_numero, nm_complemento, nr_jucesp_cad, dt_jucesp_cad,
                                    nr_jucesp_alt, dt_jucesp_alt, recnum)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, (SELECT COALESCE(MAX(recnum), 0) + 1 FROM empresas))
            """, dados)
            conn.commit()
            conn.close()
            self.limpar_campos()
            self.carregar_empresas()
            self.show_message("Empresa salva com sucesso!", "success")
        except sqlite3.Error as e:
            self.show_message(f"Erro ao salvar empresa: {str(e)}", "error")

    def remover_empresa(self):
        selecionado = self.tree.focus()
        if not selecionado:
            self.show_message("Selecione uma empresa para remover.", "warning")
            return

        item = self.tree.item(selecionado)
        empresa_id = item["values"][0]

        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM empresas WHERE id_empresa = ?", (empresa_id,))
            conn.commit()
            conn.close()
            self.carregar_empresas()
            self.limpar_campos()
            self.show_message("Empresa removida com sucesso!", "success")
        except sqlite3.Error as e:
            self.show_message(f"Erro ao remover empresa: {str(e)}", "error")

    def carregar_empresas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_empresa, nm_razao, nm_fantasia, nr_cnpj FROM empresas ORDER BY nm_razao")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        empresa_id, razao, fantasia, cnpj = item["values"]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nm_razao, nm_fantasia, nr_cnpj, nr_ie, nr_im, cd_cep, nr_numero,
                nm_complemento, nr_jucesp_cad, dt_jucesp_cad, nr_jucesp_alt, dt_jucesp_alt
            FROM empresas WHERE id_empresa = ?
        """, (empresa_id,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            (razao, fantasia, cnpj, ie, im, cep, numero,
            complemento, jucesp_cad, dt_cad, jucesp_alt, dt_alt) = resultado
                
            self.entry_razao.delete(0, tk.END)
            self.entry_razao.insert(0, razao or "")
                
            self.entry_fantasia.delete(0, tk.END)
            self.entry_fantasia.insert(0, fantasia or "")
                
            self.entry_cnpj.delete(0, tk.END)
            self.entry_cnpj.insert(0, cnpj or "")
                
            self.entry_ie.delete(0, tk.END)
            self.entry_ie.insert(0, ie or "")
                
            self.entry_im.delete(0, tk.END)
            self.entry_im.insert(0, im or "")
                
            self.entry_cep.delete(0, tk.END)
            self.entry_cep.insert(0, cep or "")
                
            self.entry_numero.delete(0, tk.END)
            self.entry_numero.insert(0, numero or "")
                
            self.entry_complemento.delete(0, tk.END)
            self.entry_complemento.insert(0, complemento or "")
                
            self.entry_jucesp_cad.delete(0, tk.END)
            self.entry_jucesp_cad.insert(0, jucesp_cad or "")
                
            self.entry_dt_cad.delete(0, tk.END)
            self.entry_dt_cad.insert(0, dt_cad or "")
                
            self.entry_jucesp_alt.delete(0, tk.END)
            self.entry_jucesp_alt.insert(0, jucesp_alt or "")
                
            self.entry_dt_alt.delete(0, tk.END)
            self.entry_dt_alt.insert(0, dt_alt or "")

    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.entry_razao.delete(0, tk.END)
        self.entry_fantasia.delete(0, tk.END)
        self.entry_cnpj.delete(0, tk.END)
        self.entry_ie.delete(0, tk.END)
        self.entry_im.delete(0, tk.END)
        self.entry_cep.delete(0, tk.END)
        self.entry_numero.delete(0, tk.END)
        self.entry_complemento.delete(0, tk.END)
        self.entry_jucesp_cad.delete(0, tk.END)
        self.entry_dt_cad.delete(0, tk.END)
        self.entry_jucesp_alt.delete(0, tk.END)
        self.entry_dt_alt.delete(0, tk.END)

