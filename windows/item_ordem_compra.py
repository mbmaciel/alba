import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class ItemOrdemCompraWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Itens da Ordem de Compra (alba0011)")
        self.geometry("1100x650")
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
        ttkb.Label(input_frame, text="ID OC").grid(row=0, column=0, sticky=tk.W)
        self.entry_id_oc = ttkb.Entry(input_frame, width=10)
        self.entry_id_oc.grid(row=0, column=1, padx=5, pady=5)

        ttkb.Label(input_frame, text="Produto").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.combo_produto = ttkb.Combobox(input_frame, width=35, state="readonly")
        self.combo_produto.grid(row=0, column=3, padx=5, pady=5)

        ttkb.Label(input_frame, text="Qtde").grid(row=0, column=4, sticky=tk.W, padx=(20, 0))
        self.entry_qtd = ttkb.Entry(input_frame, width=10)
        self.entry_qtd.grid(row=0, column=5, padx=5, pady=5)
        self.entry_qtd.bind('<KeyRelease>', self.calcular_total_auto)

        # Segunda linha
        ttkb.Label(input_frame, text="Valor Unit.").grid(row=1, column=0, sticky=tk.W)
        self.entry_unit = ttkb.Entry(input_frame, width=12)
        self.entry_unit.grid(row=1, column=1, padx=5, pady=5)
        self.entry_unit.bind('<KeyRelease>', self.calcular_total_auto)

        ttkb.Label(input_frame, text="Desc. %").grid(row=1, column=2, sticky=tk.W, padx=(20, 0))
        self.entry_desc = ttkb.Entry(input_frame, width=10)
        self.entry_desc.grid(row=1, column=3, padx=5, pady=5)
        self.entry_desc.bind('<KeyRelease>', self.calcular_total_auto)

        ttkb.Label(input_frame, text="Total").grid(row=1, column=4, sticky=tk.W, padx=(20, 0))
        self.entry_total = ttkb.Entry(input_frame, width=15, state="readonly")
        self.entry_total.grid(row=1, column=5, padx=5, pady=5)

        # Terceira linha - Observações
        ttkb.Label(input_frame, text="Observações").grid(row=2, column=0, sticky=tk.W)
        self.entry_obs = ttkb.Entry(input_frame, width=80)
        self.entry_obs.grid(row=2, column=1, columnspan=5, padx=5, pady=5, sticky=tk.W+tk.E)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "oc", "produto", "qtde", "unit", "desc", "total"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("oc", text="OC")
        self.tree.heading("produto", text="Produto")
        self.tree.heading("qtde", text="Qtde")
        self.tree.heading("unit", text="Valor Unit.")
        self.tree.heading("desc", text="Desc. %")
        self.tree.heading("total", text="Total")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("oc", width=60, minwidth=50, anchor=tk.CENTER)
        self.tree.column("produto", width=300, minwidth=200, anchor=tk.W)
        self.tree.column("qtde", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("unit", width=100, minwidth=80, anchor=tk.E)
        self.tree.column("desc", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("total", width=120, minwidth=100, anchor=tk.E)
        
        # Scrollbar para o Treeview
        scrollbar = ttkb.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_produtos()
        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar()
        self.entry_id_oc.focus()

    def carregar_produtos(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_produto, nm_produto FROM alba0005 ORDER BY nm_produto")
        self.produtos = cursor.fetchall()
        conn.close()
        self.combo_produto["values"] = [nome for _, nome in self.produtos]

    def calcular_total_auto(self, event=None):
        """Calcula o total automaticamente quando os campos são alterados"""
        try:
            qtd = float(self.entry_qtd.get()) if self.entry_qtd.get() else 0
            valor = float(self.entry_unit.get()) if self.entry_unit.get() else 0
            desc = float(self.entry_desc.get()) if self.entry_desc.get() else 0
            
            total = qtd * valor * (1 - desc / 100)
            
            # Atualizar campo total
            self.entry_total.config(state="normal")
            self.entry_total.delete(0, tk.END)
            self.entry_total.insert(0, f"{total:.2f}")
            self.entry_total.config(state="readonly")
            
        except ValueError:
            # Se houver erro na conversão, limpar o campo total
            self.entry_total.config(state="normal")
            self.entry_total.delete(0, tk.END)
            self.entry_total.config(state="readonly")

    def calcular_total(self):
        try:
            qt = float(self.entry_qtd.get()) if self.entry_qtd.get() else 0
            valor = float(self.entry_unit.get()) if self.entry_unit.get() else 0
            desc = float(self.entry_desc.get()) if self.entry_desc.get() else 0
            total = qt * valor * (1 - desc / 100)
            return round(total, 2)
        except:
            return 0.0

    def salvar(self):
        id_oc = self.entry_id_oc.get()
        produto_nome = self.combo_produto.get()
        qtd = self.entry_qtd.get()
        unit = self.entry_unit.get()
        desc = self.entry_desc.get()
        obs = self.entry_obs.get()

        # Validações
        if not id_oc:
            messagebox.showwarning("Atenção", "ID da Ordem de Compra é obrigatório.")
            return
            
        if not produto_nome:
            messagebox.showwarning("Atenção", "Selecione um produto.")
            return
            
        if not qtd or not unit:
            messagebox.showwarning("Atenção", "Quantidade e Valor Unitário são obrigatórios.")
            return

        try:
            qtd = float(qtd)
            unit = float(unit)
            desc = float(desc) if desc else 0
        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos.")
            return

        id_produto = next((id for id, nome in self.produtos if nome == produto_nome), None)
        if not id_produto:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return

        total = self.calcular_total()

        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO alba0011 (
                    id_oc, id_produto, cd_cliente, qt_produto, vl_unitario,
                    pc_desc_coml, pc_desc_fiscal, vl_unit_final, vl_produto,
                    pc_ipi, vl_ipi, pc_icms, vl_icms, pc_icmsst, vl_icmsst,
                    vl_total, pc_comissao, vl_comissao, fl_status, tx_obs, fl_comissao
                ) VALUES (?, ?, '', ?, ?, ?, 0, ?, ?, 0, 0, 0, 0, 0, 0, ?, 0, 0, 'ATIVO', ?, 'S')
            """, (id_oc, id_produto, qtd, unit, desc, total, total, total, obs))
            conn.commit()
            messagebox.showinfo("Sucesso", "Item salvo com sucesso!")
            self.limpar()
            self.carregar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar item: {str(e)}")
        finally:
            conn.close()

    def remover(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um item para remover.")
            return
            
        id_item = self.tree.item(item)["values"][0]
        
        resposta = messagebox.askyesno("Confirmar", "Deseja realmente remover este item?")
        if not resposta:
            return
            
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM alba0011 WHERE id_item = ?", (id_item,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Item removido com sucesso!")
            self.carregar()
            self.limpar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover item: {str(e)}")
        finally:
            conn.close()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.id_item, i.id_oc, p.nm_produto, i.qt_produto, 
                   i.vl_unitario, i.pc_desc_coml, i.vl_total
            FROM alba0011 i
            LEFT JOIN alba0005 p ON i.id_produto = p.id_produto
            ORDER BY i.id_oc, p.nm_produto
        """)
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        
        values = item["values"]
        if len(values) >= 7:
            id_item, id_oc, nome_produto, qtd, unit, desc, total = values
            
            # Buscar observações do item
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT tx_obs FROM alba0011 WHERE id_item = ?", (id_item,))
            result = cursor.fetchone()
            obs = result[0] if result and result[0] else ""
            conn.close()
            
            # Preencher campos
            self.entry_id_oc.delete(0, tk.END)
            self.entry_id_oc.insert(0, str(id_oc))
            
            self.combo_produto.set(nome_produto or "")
            
            self.entry_qtd.delete(0, tk.END)
            self.entry_qtd.insert(0, str(qtd) if qtd else "")
            
            self.entry_unit.delete(0, tk.END)
            self.entry_unit.insert(0, str(unit) if unit else "")
            
            self.entry_desc.delete(0, tk.END)
            self.entry_desc.insert(0, str(desc) if desc else "")
            
            self.entry_total.config(state="normal")
            self.entry_total.delete(0, tk.END)
            self.entry_total.insert(0, str(total) if total else "")
            self.entry_total.config(state="readonly")
            
            self.entry_obs.delete(0, tk.END)
            self.entry_obs.insert(0, obs)

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.entry_id_oc.delete(0, tk.END)
        self.combo_produto.set("")
        self.entry_qtd.delete(0, tk.END)
        self.entry_unit.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.entry_total.config(state="normal")
        self.entry_total.delete(0, tk.END)
        self.entry_total.config(state="readonly")
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
