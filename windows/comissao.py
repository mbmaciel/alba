import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class ComissaoWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Faixas de Comissão")
        self.geometry("800x550")
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
        ttkb.Label(input_frame, text="Desconto Inicial (%)").grid(row=0, column=0, sticky=tk.W)
        self.entry_ini = ttkb.Entry(input_frame, width=15)
        self.entry_ini.grid(row=0, column=1, padx=5, pady=5)

        ttkb.Label(input_frame, text="Desconto Final (%)").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.entry_fim = ttkb.Entry(input_frame, width=15)
        self.entry_fim.grid(row=0, column=3, padx=5, pady=5)

        ttkb.Label(input_frame, text="Comissão (%)").grid(row=0, column=4, sticky=tk.W, padx=(20, 0))
        self.entry_comissao = ttkb.Entry(input_frame, width=15)
        self.entry_comissao.grid(row=0, column=5, padx=5, pady=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "desc_ini", "desc_fim", "comissao"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("desc_ini", text="Desconto Inicial (%)")
        self.tree.heading("desc_fim", text="Desconto Final (%)")
        self.tree.heading("comissao", text="Comissão (%)")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("desc_ini", width=200, minwidth=150, anchor=tk.CENTER)
        self.tree.column("desc_fim", width=200, minwidth=150, anchor=tk.CENTER)
        self.tree.column("comissao", width=200, minwidth=150, anchor=tk.CENTER)
        
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
        self.entry_ini.focus()

    def salvar(self):
        try:
            ini = float(self.entry_ini.get())
            fim = float(self.entry_fim.get())
            comissao = float(self.entry_comissao.get())
        except ValueError:
            messagebox.showerror("Erro", "Insira valores numéricos válidos.")
            return

        if ini < 0 or fim < 0 or comissao < 0:
            messagebox.showwarning("Atenção", "Os valores devem ser positivos.")
            return

        if ini > fim:
            messagebox.showwarning("Atenção", "O desconto inicial deve ser menor ou igual ao desconto final.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO comissao (pc_desc_ini, pc_desc_fim, pc_comissao)
            VALUES (?, ?, ?)
        """, (ini, fim, comissao))
        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()
        messagebox.showinfo("Sucesso", "Faixa de comissão salva com sucesso!")

    def remover(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione uma faixa de comissão para remover.")
            return
            
        id_comissao = self.tree.item(item)["values"][0]
        
        resposta = messagebox.askyesno("Confirmar", "Deseja realmente remover esta faixa de comissão?")
        if not resposta:
            return
            
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM comissao WHERE id_comissao = ?", (id_comissao,))
        conn.commit()
        conn.close()
        self.carregar()
        self.limpar()
        messagebox.showinfo("Sucesso", "Faixa de comissão removida com sucesso!")

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_comissao, pc_desc_ini, pc_desc_fim, pc_comissao FROM comissao ORDER BY pc_desc_ini")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        values = item["values"]
        if len(values) >= 4:
            _, ini, fim, comissao = values
            self.entry_ini.delete(0, tk.END)
            self.entry_ini.insert(0, str(ini))
            self.entry_fim.delete(0, tk.END)
            self.entry_fim.insert(0, str(fim))
            self.entry_comissao.delete(0, tk.END)
            self.entry_comissao.insert(0, str(comissao))

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.entry_ini.delete(0, tk.END)
        self.entry_fim.delete(0, tk.END)
        self.entry_comissao.delete(0, tk.END)
        
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
