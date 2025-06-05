import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class TextosWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Textos")
        self.geometry("900x700")
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

        # Frame para campos de entrada
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        # Primeira linha - ID e Descrição
        ttkb.Label(input_frame, text="ID Texto").grid(row=0, column=0, sticky=tk.W)
        self.entry_id = ttkb.Entry(input_frame, width=10)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        ttkb.Label(input_frame, text="Descrição").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.entry_desc = ttkb.Entry(input_frame, width=50)
        self.entry_desc.grid(row=0, column=3, padx=5, pady=5)

        # Segunda linha - Tipo (Combobox)
        ttkb.Label(input_frame, text="Tipo de Texto").grid(row=1, column=0, sticky=tk.W)
        self.combo_tipo = ttkb.Combobox(input_frame, width=17, values=["F", "N"], state="readonly")
        self.combo_tipo.grid(row=1, column=1, padx=5, pady=5)

        # Frame para campos de texto multilinha
        text_frame = ttkb.Frame(main_frame)
        text_frame.pack(fill=tk.X, pady=(0, 15))

        # Prazo - Text widget multilinha
        ttkb.Label(text_frame, text="Prazo").grid(row=0, column=0, sticky=tk.NW, pady=(5, 0))
        self.text_prazo = tk.Text(text_frame, width=80, height=3, wrap=tk.WORD)
        self.text_prazo.grid(row=0, column=1, padx=5, pady=5)
            
        # Scrollbar para Prazo
        scroll_prazo = ttkb.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_prazo.yview)
        self.text_prazo.configure(yscrollcommand=scroll_prazo.set)
        scroll_prazo.grid(row=0, column=2, sticky=tk.NS, pady=5)

        # Condições - Text widget multilinha
        ttkb.Label(text_frame, text="Condições").grid(row=1, column=0, sticky=tk.NW, pady=(5, 0))
        self.text_condicoes = tk.Text(text_frame, width=80, height=3, wrap=tk.WORD)
        self.text_condicoes.grid(row=1, column=1, padx=5, pady=5)
            
        # Scrollbar para Condições
        scroll_condicoes = ttkb.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_condicoes.yview)
        self.text_condicoes.configure(yscrollcommand=scroll_condicoes.set)
        scroll_condicoes.grid(row=1, column=2, sticky=tk.NS, pady=5)

        # Observações - Text widget multilinha
        ttkb.Label(text_frame, text="Observações").grid(row=2, column=0, sticky=tk.NW, pady=(5, 0))
        self.text_obs = tk.Text(text_frame, width=80, height=3, wrap=tk.WORD)
        self.text_obs.grid(row=2, column=1, padx=5, pady=5)
            
        # Scrollbar para Observações
        scroll_obs = ttkb.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_obs.yview)
        self.text_obs.configure(yscrollcommand=scroll_obs.set)
        scroll_obs.grid(row=2, column=2, sticky=tk.NS, pady=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id_texto", "nm_descricao", "tp_tipo"), show="headings", height=12)
            
        # Configuração das colunas
        self.tree.heading("id_texto", text="ID")
        self.tree.heading("nm_descricao", text="Descrição")
        self.tree.heading("tp_tipo", text="Tipo")
        self.tree.column("id_texto", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("nm_descricao", width=400, minwidth=300, anchor=tk.W)
        self.tree.column("tp_tipo", width=200, minwidth=150, anchor=tk.W)
            
        # Scrollbar para o Treeview
        scrollbar = ttkb.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
            
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar()
        self.entry_id.focus()

    def salvar(self):
        id_texto = self.entry_id.get()
        desc = self.entry_desc.get()
        prazo = self.text_prazo.get("1.0", tk.END).strip()
        cond = self.text_condicoes.get("1.0", tk.END).strip()
        obs = self.text_obs.get("1.0", tk.END).strip()
        tipo = self.combo_tipo.get()

        if not id_texto or not desc:
            messagebox.showwarning("Atenção", "Preencha ao menos ID e Descrição.")
            return

        try:
            id_texto = int(id_texto)
        except ValueError:
            messagebox.showwarning("Erro", "ID deve ser um número.")
            return

        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM textos WHERE id_texto = ?", (id_texto,))
        existe = cursor.fetchone()[0]

        if existe:
            cursor.execute("""
                UPDATE textos SET
                    nm_descricao = ?, tx_prazo = ?, tx_condicoes = ?,
                    tx_obs = ?, tp_tipo = ?
                WHERE id_texto = ?
            """, (desc, prazo, cond, obs, tipo, id_texto))
        else:
            cursor.execute("""
                INSERT INTO textos (
                    id_texto, nm_descricao, tx_prazo, tx_condicoes, tx_obs, tp_tipo
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (id_texto, desc, prazo, cond, obs, tipo))

        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        id_texto = self.tree.item(item)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM textos WHERE id_texto = ?", (id_texto,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_texto, nm_descricao, tp_tipo FROM textos ORDER BY id_texto")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        id_texto, desc, tipo = item["values"]

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tx_prazo, tx_condicoes, tx_obs FROM textos WHERE id_texto = ?
        """, (id_texto,))
        result = cursor.fetchone()
        conn.close()

        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, id_texto)

        self.entry_desc.delete(0, tk.END)
        self.entry_desc.insert(0, desc)

        self.combo_tipo.set(tipo or "")

        self.text_prazo.delete("1.0", tk.END)
        self.text_prazo.insert("1.0", result[0] if result and result[0] else "")

        self.text_condicoes.delete("1.0", tk.END)
        self.text_condicoes.insert("1.0", result[1] if result and result[1] else "")

        self.text_obs.delete("1.0", tk.END)
        self.text_obs.insert("1.0", result[2] if result and result[2] else "")

    def limpar(self):
        self.entry_id.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.combo_tipo.set("")
        self.text_prazo.delete("1.0", tk.END)
        self.text_condicoes.delete("1.0", tk.END)
        self.text_obs.delete("1.0", tk.END)
