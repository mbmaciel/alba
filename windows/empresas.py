import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class EmpresaWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Empresas")
        self.geometry("750x600")
        self.resizable(False, False)

        notebook = ttkb.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frame_basico = ttkb.Frame(notebook)
        self.frame_endereco = ttkb.Frame(notebook)
        self.frame_jucesp = ttkb.Frame(notebook)

        notebook.add(self.frame_basico, text='Dados Básicos')
        notebook.add(self.frame_endereco, text='Endereço')
        notebook.add(self.frame_jucesp, text='JUCESP')

        # Aba Dados Básicos
        ttkb.Label(self.frame_basico, text="Razão Social").grid(row=0, column=0, sticky=tk.W)
        self.entry_razao = ttkb.Entry(self.frame_basico, width=50)
        self.entry_razao.grid(row=0, column=1, columnspan=2, pady=5)

        ttkb.Label(self.frame_basico, text="Nome Fantasia").grid(row=1, column=0, sticky=tk.W)
        self.entry_fantasia = ttkb.Entry(self.frame_basico, width=50)
        self.entry_fantasia.grid(row=1, column=1, columnspan=2, pady=5)

        ttkb.Label(self.frame_basico, text="CNPJ").grid(row=2, column=0, sticky=tk.W)
        self.entry_cnpj = ttkb.Entry(self.frame_basico, width=30)
        self.entry_cnpj.grid(row=2, column=1, pady=5)

        ttkb.Label(self.frame_basico, text="Inscrição Estadual").grid(row=3, column=0, sticky=tk.W)
        self.entry_ie = ttkb.Entry(self.frame_basico, width=30)
        self.entry_ie.grid(row=3, column=1, pady=5)

        ttkb.Label(self.frame_basico, text="Inscrição Municipal").grid(row=4, column=0, sticky=tk.W)
        self.entry_im = ttkb.Entry(self.frame_basico, width=30)
        self.entry_im.grid(row=4, column=1, pady=5)

        # Aba Endereço
        ttkb.Label(self.frame_endereco, text="CEP").grid(row=0, column=0, sticky=tk.W)
        self.entry_cep = ttkb.Entry(self.frame_endereco, width=15)
        self.entry_cep.grid(row=0, column=1, pady=5)

        ttkb.Label(self.frame_endereco, text="Número").grid(row=1, column=0, sticky=tk.W)
        self.entry_numero = ttkb.Entry(self.frame_endereco, width=10)
        self.entry_numero.grid(row=1, column=1, pady=5)

        ttkb.Label(self.frame_endereco, text="Complemento").grid(row=2, column=0, sticky=tk.W)
        self.entry_complemento = ttkb.Entry(self.frame_endereco, width=40)
        self.entry_complemento.grid(row=2, column=1, pady=5)

        # Aba JUCESP
        ttkb.Label(self.frame_jucesp, text="Nº JUCESP Cadastro").grid(row=0, column=0, sticky=tk.W)
        self.entry_jucesp_cad = ttkb.Entry(self.frame_jucesp, width=20)
        self.entry_jucesp_cad.grid(row=0, column=1, pady=5)

        ttkb.Label(self.frame_jucesp, text="Data Cadastro").grid(row=1, column=0, sticky=tk.W)
        self.entry_dt_cad = ttkb.Entry(self.frame_jucesp, width=20)
        self.entry_dt_cad.grid(row=1, column=1, pady=5)

        ttkb.Label(self.frame_jucesp, text="Nº JUCESP Alteração").grid(row=2, column=0, sticky=tk.W)
        self.entry_jucesp_alt = ttkb.Entry(self.frame_jucesp, width=20)
        self.entry_jucesp_alt.grid(row=2, column=1, pady=5)

        ttkb.Label(self.frame_jucesp, text="Data Alteração").grid(row=3, column=0, sticky=tk.W)
        self.entry_dt_alt = ttkb.Entry(self.frame_jucesp, width=20)
        self.entry_dt_alt.grid(row=3, column=1, pady=5)

        # Botões principais (abaixo do notebook)
        frame_botoes = ttkb.Frame(self)
        frame_botoes.pack(fill=tk.X, padx=10, pady=(0,10))
        ttkb.Button(frame_botoes, text="Salvar", command=self.salvar_empresa, bootstyle=SUCCESS).pack(side=tk.RIGHT, padx=5)
        ttkb.Button(frame_botoes, text="Remover", command=self.remover_empresa, bootstyle=DANGER).pack(side=tk.RIGHT, padx=5)

        # Treeview para exibir empresas
        self.tree = ttkb.Treeview(self, columns=("id", "razao", "fantasia", "cnpj"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.column("id", width=0, stretch=False)
        self.tree.heading("id", text="")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_empresas()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

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
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios: Razão Social e CNPJ.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO empresas (nm_razao, nm_fantasia, nr_cnpj, nr_ie, nr_im, cd_cep,
                                  nr_numero, nm_complemento, nr_jucesp_cad, dt_jucesp_cad,
                                  nr_jucesp_alt, dt_jucesp_alt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, dados)
        conn.commit()
        conn.close()
        self.limpar_campos()
        self.carregar_empresas()

    def remover_empresa(self):
        selecionado = self.tree.focus()
        if not selecionado:
            return
        item = self.tree.item(selecionado)
        empresa_id = item["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM empresas WHERE id_empresa = ?", (empresa_id,))
        conn.commit()
        conn.close()
        self.carregar_empresas()

    def carregar_empresas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_empresa, nm_razao, nm_fantasia, nr_cnpj FROM empresas")
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
            self.entry_razao.insert(0, razao)
            self.entry_fantasia.delete(0, tk.END)
            self.entry_fantasia.insert(0, fantasia)
            self.entry_cnpj.delete(0, tk.END)
            self.entry_cnpj.insert(0, cnpj)
            self.entry_ie.delete(0, tk.END)
            self.entry_ie.insert(0, ie)
            self.entry_im.delete(0, tk.END)
            self.entry_im.insert(0, im)
            self.entry_cep.delete(0, tk.END)
            self.entry_cep.insert(0, cep)
            self.entry_numero.delete(0, tk.END)
            self.entry_numero.insert(0, numero)
            self.entry_complemento.delete(0, tk.END)
            self.entry_complemento.insert(0, complemento)
            self.entry_jucesp_cad.delete(0, tk.END)
            self.entry_jucesp_cad.insert(0, jucesp_cad)
            self.entry_dt_cad.delete(0, tk.END)
            self.entry_dt_cad.insert(0, dt_cad)
            self.entry_jucesp_alt.delete(0, tk.END)
            self.entry_jucesp_alt.insert(0, jucesp_alt)
            self.entry_dt_alt.delete(0, tk.END)
            self.entry_dt_alt.insert(0, dt_alt)

    def limpar_campos(self):
        for entry in [
            self.entry_razao, self.entry_fantasia, self.entry_cnpj, self.entry_ie,
            self.entry_im, self.entry_cep, self.entry_numero, self.entry_complemento,
            self.entry_jucesp_cad, self.entry_dt_cad, self.entry_jucesp_alt, self.entry_dt_alt
        ]:
            entry.delete(0, tk.END)
