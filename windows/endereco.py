import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo

import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class EnderecoWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Endereços (alba0002)")
        self.geometry("750x400")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Combobox Pessoa
        ttkb.Label(frame, text="Pessoa").grid(row=0, column=0, sticky=tk.W)
        self.combo_pessoa = ttkb.Combobox(frame, width=50, state="readonly")
        self.combo_pessoa.grid(row=0, column=1, columnspan=3, pady=5)

        ttkb.Label(frame, text="Tipo").grid(row=1, column=0, sticky=tk.W)
        self.entry_tipo = ttkb.Entry(frame, width=15)
        self.entry_tipo.grid(row=1, column=1, pady=5)

        ttkb.Label(frame, text="CEP").grid(row=1, column=2, sticky=tk.W)
        self.entry_cep = ttkb.Entry(frame, width=15)
        self.entry_cep.grid(row=1, column=3, pady=5)

        ttkb.Label(frame, text="Número").grid(row=2, column=0, sticky=tk.W)
        self.entry_numero = ttkb.Entry(frame, width=10)
        self.entry_numero.grid(row=2, column=1, pady=5)

        ttkb.Label(frame, text="Complemento").grid(row=2, column=2, sticky=tk.W)
        self.entry_compl = ttkb.Entry(frame, width=30)
        self.entry_compl.grid(row=2, column=3, pady=5)

        ttkb.Button(frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).grid(row=3, column=2, pady=10)
        ttkb.Button(frame, text="Remover", command=self.remover, bootstyle=DANGER).grid(row=3, column=3)

        # Frame para botões de navegação
        nav_frame = ttkb.Frame(self, padding=5)
        nav_frame.pack(fill=tk.X, padx=10)

        # Botões de navegação
        ttkb.Button(nav_frame, text="⏮ Primeiro", command=self.ir_primeiro, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="◀ Anterior", command=self.ir_anterior, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Próximo ▶", command=self.ir_proximo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Último ⏭", command=self.ir_ultimo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)

        self.tree = ttkb.Treeview(self, columns=("id", "pessoa", "tipo", "cep", "numero", "compl"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())

        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.heading("id", text="")

        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_pessoas()
        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def carregar_pessoas(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_pessoa, nm_razao FROM alba0001 ORDER BY nm_razao")
        self.pessoas = cursor.fetchall()
        conn.close()
        self.combo_pessoa["values"] = [nome for _, nome in self.pessoas]

    def salvar(self):
        nome_pessoa = self.combo_pessoa.get()
        id_pessoa = next((id for id, nome in self.pessoas if nome == nome_pessoa), None)
        tipo = self.entry_tipo.get()
        cep = self.entry_cep.get()
        numero = self.entry_numero.get()
        compl = self.entry_compl.get()

        if not id_pessoa or not cep:
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alba0002 (id_pessoa, tp_ender, cd_cep, nr_numero, nm_compl)
            VALUES (?, ?, ?, ?, ?)
        """, (id_pessoa, tipo, cep, numero, compl))
        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        id_ender = self.tree.item(item)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alba0002 WHERE id_ender = ?", (id_ender,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id_ender, e.id_pessoa, e.tp_ender, e.cd_cep, e.nr_numero, e.nm_compl, p.nm_razao
            FROM alba0002 e
            LEFT JOIN alba0001 p ON e.id_pessoa = p.id_pessoa
        """)
        for row in cursor.fetchall():
            id_ender, id_pessoa, tipo, cep, numero, compl, nome = row
            self.tree.insert("", "end", values=(id_ender, nome or f"ID {id_pessoa}", tipo, cep, numero, compl))
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        _, pessoa_nome, tipo, cep, numero, compl = item["values"]
        self.combo_pessoa.set(pessoa_nome)
        self.entry_tipo.delete(0, tk.END)
        self.entry_tipo.insert(0, tipo)
        self.entry_cep.delete(0, tk.END)
        self.entry_cep.insert(0, cep)
        self.entry_numero.delete(0, tk.END)
        self.entry_numero.insert(0, numero)
        self.entry_compl.delete(0, tk.END)
        self.entry_compl.insert(0, compl)

    def limpar(self):
        self.combo_pessoa.set("")
        self.entry_tipo.delete(0, tk.END)
        self.entry_cep.delete(0, tk.END)
        self.entry_numero.delete(0, tk.END)
        self.entry_compl.delete(0, tk.END)
        
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
