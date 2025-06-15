import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class CfopWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de CFOP")
        self.geometry("900x600")
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
        ttkb.Label(input_frame, text="Código CFOP").grid(row=0, column=0, sticky=tk.W)
        self.entry_codigo = ttkb.Entry(input_frame, width=15)
        self.entry_codigo.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Descrição").grid(row=0, column=2, sticky=tk.W)
        self.entry_descricao = ttkb.Entry(input_frame, width=50)
        self.entry_descricao.grid(row=0, column=3, pady=5, padx=5)

        # Segunda linha
        ttkb.Label(input_frame, text="Flag Impostos").grid(row=1, column=0, sticky=tk.W)
        self.entry_impostos = ttkb.Entry(input_frame, width=15)
        self.entry_impostos.grid(row=1, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Flag Kardex").grid(row=1, column=2, sticky=tk.W)
        self.entry_kardex = ttkb.Entry(input_frame, width=15)
        self.entry_kardex.grid(row=1, column=3, pady=5, padx=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("codigo", "descricao", "impostos", "kardex"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("codigo", text="Código")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("impostos", text="Flag Impostos")
        self.tree.heading("kardex", text="Flag Kardex")
        
        self.tree.column("codigo", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column("descricao", width=400, minwidth=300, anchor=tk.W)
        self.tree.column("impostos", width=120, minwidth=100, anchor=tk.CENTER)
        self.tree.column("kardex", width=120, minwidth=100, anchor=tk.CENTER)
        
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
        self.entry_codigo.focus()

    def salvar(self):
        codigo = self.entry_codigo.get().strip()
        descricao = self.entry_descricao.get().strip()
        impostos = self.entry_impostos.get().strip()
        kardex = self.entry_kardex.get().strip()

        if not codigo or not descricao:
            messagebox.showwarning("Campos obrigatórios", "Código e descrição são obrigatórios.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        try:
            # Verificar se o registro já existe
            cursor.execute("SELECT recnum FROM cfop WHERE cd_cfop = ?", (codigo,))
            registro_existente = cursor.fetchone()
            
            is_update = registro_existente is not None
            
            if is_update:
                # Atualizar registro existente
                cursor.execute("""UPDATE cfop 
                                SET nm_cfop = ?, fl_impostos = ?, fl_kardex = ? 
                                WHERE cd_cfop = ?""",
                             (descricao, impostos, kardex, codigo))
                messagebox.showinfo("Sucesso", "CFOP atualizado com sucesso!")
            else:
                # Obter o próximo recnum
                cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM cfop")
                proximo_recnum = cursor.fetchone()[0]
                
                # Inserir novo registro
                cursor.execute("""INSERT INTO cfop (recnum, cd_cfop, nm_cfop, fl_impostos, fl_kardex) 
                                VALUES (?, ?, ?, ?, ?)""",
                             (proximo_recnum, codigo, descricao, impostos, kardex))
                messagebox.showinfo("Sucesso", "CFOP salvo com sucesso!")
            
            conn.commit()
        except Exception as e:
            messagebox.showerror("Erro ao salvar", str(e))
            return
        finally:
            conn.close()

        # Recarregar a lista
        self.carregar()
        
        # Se foi uma inserção, limpar os campos
        # Se foi uma atualização, manter o registro selecionado
        if not is_update:
            self.limpar()
        else:
            # Reselecionar o item atualizado na lista
            self.selecionar_item_por_codigo(codigo)

    def selecionar_item_por_codigo(self, codigo):
        """Seleciona um item na lista pelo código CFOP"""
        for item in self.tree.get_children():
            valores = self.tree.item(item)["values"]
            if valores and str(valores[0]) == str(codigo):
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)
                break

    def remover(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um CFOP para remover.")
            return
            
        codigo = self.tree.item(item)["values"][0]
        
        resposta = messagebox.askyesno("Confirmar", f"Deseja realmente remover o CFOP {codigo}?")
        if not resposta:
            return

        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM cfop WHERE cd_cfop = ?", (codigo,))
            conn.commit()
            messagebox.showinfo("Sucesso", "CFOP removido com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao remover", str(e))
        finally:
            conn.close()

        self.carregar()
        self.limpar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT cd_cfop, nm_cfop, fl_impostos, fl_kardex FROM cfop ORDER BY cd_cfop")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        codigo, descricao, impostos, kardex = item["values"]
        
        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, codigo or "")
        
        self.entry_descricao.delete(0, tk.END)
        self.entry_descricao.insert(0, descricao or "")
        
        self.entry_impostos.delete(0, tk.END)
        self.entry_impostos.insert(0, impostos or "")
        
        self.entry_kardex.delete(0, tk.END)
        self.entry_kardex.insert(0, kardex or "")

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.entry_codigo.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_impostos.delete(0, tk.END)
        self.entry_kardex.delete(0, tk.END)
        
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
