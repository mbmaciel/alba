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
        self.geometry("950x500")
        self.resizable(False, False)

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttkb.Label(frame, text="ID OC").grid(row=0, column=0, sticky=tk.W)
        self.entry_id_oc = ttkb.Entry(frame, width=10)
        self.entry_id_oc.grid(row=0, column=1, padx=5, pady=5)

        ttkb.Label(frame, text="Produto").grid(row=0, column=2, sticky=tk.W)
        self.combo_produto = ttkb.Combobox(frame, width=40, state="readonly")
        self.combo_produto.grid(row=0, column=3, columnspan=2, padx=5, pady=5)

        ttkb.Label(frame, text="Qtde").grid(row=0, column=5, sticky=tk.W)
        self.entry_qtd = ttkb.Entry(frame, width=10)
        self.entry_qtd.grid(row=0, column=6, padx=5, pady=5)

        ttkb.Label(frame, text="Valor Unit.").grid(row=1, column=0, sticky=tk.W)
        self.entry_unit = ttkb.Entry(frame, width=10)
        self.entry_unit.grid(row=1, column=1, padx=5, pady=5)

        ttkb.Label(frame, text="Desc. %").grid(row=1, column=2, sticky=tk.W)
        self.entry_desc = ttkb.Entry(frame, width=10)
        self.entry_desc.grid(row=1, column=3, padx=5, pady=5)

        ttkb.Label(frame, text="Total").grid(row=1, column=4, sticky=tk.W)
        self.entry_total = ttkb.Entry(frame, width=15)
        self.entry_total.grid(row=1, column=5, padx=5, pady=5)

        ttkb.Label(frame, text="Obs").grid(row=2, column=0, sticky=tk.W)
        self.entry_obs = ttkb.Entry(frame, width=60)
        self.entry_obs.grid(row=2, column=1, columnspan=5, padx=5, pady=5)

        ttkb.Button(frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).grid(row=3, column=4, pady=10)
        ttkb.Button(frame, text="Remover", command=self.remover, bootstyle=DANGER).grid(row=3, column=5)

        # Frame para botões de navegação
        nav_frame = ttkb.Frame(self, padding=5)
        nav_frame.pack(fill=tk.X, padx=10)

        # Botões de navegação
        ttkb.Button(nav_frame, text="⏮ Primeiro", command=self.ir_primeiro, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="◀ Anterior", command=self.ir_anterior, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Próximo ▶", command=self.ir_proximo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(nav_frame, text="Último ⏭", command=self.ir_ultimo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)

        self.tree = ttkb.Treeview(self, columns=("id", "oc", "produto", "qtde", "unit", "total"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_produtos()
        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def carregar_produtos(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_produto, nm_produto FROM alba0005 ORDER BY nm_produto")
        self.produtos = cursor.fetchall()
        conn.close()
        self.combo_produto["values"] = [nome for _, nome in self.produtos]

    def calcular_total(self):
        try:
            qt = int(self.entry_qtd.get())
            valor = float(self.entry_unit.get())
            desc = float(self.entry_desc.get()) if self.entry_desc.get() else 0
            total = qt * valor * (1 - desc / 100)
            return round(total, 2)
        except:
            return 0.0

    def salvar(self):
        id_oc = self.entry_id_oc.get()
        produto_nome = self.combo_produto.get()
        id_produto = next((id for id, nome in self.produtos if nome == produto_nome), None)
        qtd = self.entry_qtd.get()
        unit = self.entry_unit.get()
        desc = self.entry_desc.get()
        total = self.calcular_total()

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alba0011 (
                id_oc, id_produto, cd_cliente, qt_produto, vl_unitario,
                pc_desc_coml, pc_desc_fiscal, vl_unit_final, vl_produto,
                pc_ipi, vl_ipi, pc_icms, vl_icms, pc_icmsst, vl_icmsst,
                vl_total, pc_comissao, vl_comissao, fl_status, tx_obs, fl_comissao
            ) VALUES (?, ?, '', ?, ?, ?, 0, ?, ?, 0, 0, 0, 0, 0, 0, ?, 0, 0, 'ATIVO', ?, 'S')
        """, (id_oc, id_produto, qtd, unit, desc, total, total, total, self.entry_obs.get()))
        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()

    def remover(self):
        item = self.tree.focus()
        if not item:
            return
        id_item = self.tree.item(item)["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alba0011 WHERE id_item = ?", (id_item,))
        conn.commit()
        conn.close()
        self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.id_item, i.id_oc, i.id_produto, i.qt_produto, i.vl_unitario, i.vl_total, p.nm_produto
            FROM alba0011 i
            LEFT JOIN alba0005 p ON i.id_produto = p.id_produto
        """)
        for row in cursor.fetchall():
            id_item, id_oc, id_produto, qtd, unit, total, nome = row
            self.tree.insert("", "end", values=(id_item, id_oc, nome or f"ID {id_produto}", qtd, unit, total))
        conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        _, id_oc, nome_produto, qtd, unit, total = item["values"]
        self.entry_id_oc.delete(0, tk.END)
        self.entry_id_oc.insert(0, id_oc)
        self.combo_produto.set(nome_produto)
        self.entry_qtd.delete(0, tk.END)
        self.entry_qtd.insert(0, qtd)
        self.entry_unit.delete(0, tk.END)
        self.entry_unit.insert(0, unit)
        self.entry_total.delete(0, tk.END)
        self.entry_total.insert(0, total)

    def limpar(self):
        self.entry_id_oc.delete(0, tk.END)
        self.combo_produto.set("")
        self.entry_qtd.delete(0, tk.END)
        self.entry_unit.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.entry_total.delete(0, tk.END)
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
