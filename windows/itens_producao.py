import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class ItensProducaoWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Itens de Produção (alba0009)")
        self.geometry("1000x550")
        self.resizable(False, False)
        
        # Variável para armazenar o ID do item selecionado para edição
        self.item_selecionado = None
        # Índice do item atual na lista de itens
        self.indice_atual = -1
        # Lista de IDs dos itens
        self.lista_ids = []

        frame = ttkb.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # ID Ordem de Fabricação
        ttkb.Label(frame, text="Ordem de Fabricação").grid(row=0, column=0, sticky=tk.W)
        self.combo_of = ttkb.Combobox(frame, width=20, state="readonly")
        self.combo_of.grid(row=0, column=1, padx=5, pady=5)

        # Produto
        ttkb.Label(frame, text="Produto").grid(row=0, column=2, sticky=tk.W)
        self.combo_produto = ttkb.Combobox(frame, width=40, state="readonly")
        self.combo_produto.grid(row=0, column=3, columnspan=2, padx=5, pady=5)

        # Cliente
        ttkb.Label(frame, text="Cliente").grid(row=1, column=0, sticky=tk.W)
        self.combo_cliente = ttkb.Combobox(frame, width=40, state="readonly")
        self.combo_cliente.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        ttkb.Label(frame, text="Quantidade").grid(row=1, column=3, sticky=tk.W)
        self.entry_qtd = ttkb.Entry(frame, width=10)
        self.entry_qtd.grid(row=1, column=4, padx=5)

        ttkb.Label(frame, text="Valor Unit.").grid(row=2, column=0, sticky=tk.W)
        self.entry_unit = ttkb.Entry(frame, width=15)
        self.entry_unit.grid(row=2, column=1, padx=5)

        ttkb.Label(frame, text="Desc. %").grid(row=2, column=2, sticky=tk.W)
        self.entry_desc = ttkb.Entry(frame, width=10)
        self.entry_desc.grid(row=2, column=3, padx=5)

        ttkb.Label(frame, text="Total").grid(row=2, column=4, sticky=tk.W)
        self.entry_total = ttkb.Entry(frame, width=15)
        self.entry_total.grid(row=2, column=5, padx=5)

        # Botões de ação
        btn_frame = ttkb.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=6, pady=10)
        
        ttkb.Button(btn_frame, text="Novo", command=self.novo, bootstyle=INFO).pack(side=tk.LEFT, padx=5)
        ttkb.Button(btn_frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).pack(side=tk.LEFT, padx=5)
        ttkb.Button(btn_frame, text="Remover", command=self.remover, bootstyle=DANGER).pack(side=tk.LEFT, padx=5)

        # Botões de navegação
        nav_frame = ttkb.Frame(self)
        nav_frame.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        ttkb.Button(nav_frame, text="<<", command=self.primeiro, width=3, bootstyle=SECONDARY).pack(side=tk.LEFT, padx=2)
        ttkb.Button(nav_frame, text="<", command=self.anterior, width=3, bootstyle=SECONDARY).pack(side=tk.LEFT, padx=2)
        ttkb.Button(nav_frame, text=">", command=self.proximo, width=3, bootstyle=SECONDARY).pack(side=tk.LEFT, padx=2)
        ttkb.Button(nav_frame, text=">>", command=self.ultimo, width=3, bootstyle=SECONDARY).pack(side=tk.LEFT, padx=2)
        
        # Label para mostrar a posição atual
        self.lbl_posicao = ttkb.Label(nav_frame, text="0/0")
        self.lbl_posicao.pack(side=tk.LEFT, padx=10)
        
        # Configurar o Treeview
        self.tree = ttkb.Treeview(self, columns=("id", "of", "produto", "cliente", "qtd", "unit", "total"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("of", text="OF")
        self.tree.heading("produto", text="PRODUTO")
        self.tree.heading("cliente", text="CLIENTE")
        self.tree.heading("qtd", text="QTD")
        self.tree.heading("unit", text="UNIT")
        self.tree.heading("total", text="TOTAL")
        
        # Configurar larguras das colunas
        self.tree.column("id", width=50)
        self.tree.column("of", width=80)
        self.tree.column("produto", width=300)
        self.tree.column("cliente", width=300)
        self.tree.column("qtd", width=80)
        self.tree.column("unit", width=80)
        self.tree.column("total", width=100)
        
        # Adicionar evento de seleção
        self.tree.bind("<<TreeviewSelect>>", self.item_selecionado_evento)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configurar cálculo automático do total
        self.entry_qtd.bind("<KeyRelease>", self.calcular_total)
        self.entry_unit.bind("<KeyRelease>", self.calcular_total)
        self.entry_desc.bind("<KeyRelease>", self.calcular_total)

        self.carregar_produtos()
        self.carregar_clientes()
        self.carregar_of()
        self.carregar()

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def carregar_produtos(self):
        conn = self.conectar()
        cursor = conn.cursor()
        # Modificando para mostrar apenas o nome do produto
        cursor.execute("SELECT id_produto, nm_produto FROM alba0005 ORDER BY nm_produto")
        self.produtos = cursor.fetchall()
        conn.close()
        self.combo_produto["values"] = [nome for _, nome in self.produtos]

    def carregar_clientes(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nr_cnpj_cpf, nm_razao FROM alba0001 ORDER BY nm_razao")
        self.clientes = cursor.fetchall()
        conn.close()
        self.combo_cliente["values"] = [nome for _, nome in self.clientes]

    def carregar_of(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_contatos FROM alba0003 ORDER BY id_contatos")
        self.ordens = cursor.fetchall()
        conn.close()
        self.combo_of["values"] = [str(row[0]) for row in self.ordens]

    def calcular_total(self, event=None):
        try:
            qtd = float(self.entry_qtd.get() or 0)
            unit = float(self.entry_unit.get() or 0)
            desc = float(self.entry_desc.get() or 0)
            total = qtd * unit * (1 - desc / 100)
            self.entry_total.delete(0, tk.END)
            self.entry_total.insert(0, f"{total:.2f}")
        except ValueError:
            pass

    def item_selecionado_evento(self, event):
        item = self.tree.focus()
        if not item:
            return
            
        # Obter valores do item selecionado
        valores = self.tree.item(item)["values"]
        self.item_selecionado = valores[0]  # ID do item (recnum)
        
        # Atualizar o índice atual
        if self.item_selecionado in self.lista_ids:
            self.indice_atual = self.lista_ids.index(self.item_selecionado)
            self.atualizar_posicao()
        
        # Buscar dados completos do item no banco
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.id_of, i.id_produto, i.cd_cliente, i.qt_produto, 
                   i.vl_unitario, i.pc_desc_coml, i.vl_total,
                   p.nm_produto,
                   c.nm_razao
            FROM alba0009 i
            LEFT JOIN alba0005 p ON i.id_produto = p.id_produto
            LEFT JOIN alba0001 c ON i.cd_cliente = c.nr_cnpj_cpf
            WHERE i.recnum = ?
        """, (self.item_selecionado,))
        
        item_data = cursor.fetchone()
        conn.close()
        
        if item_data:
            # Preencher os campos do formulário
            if item_data[0] is not None:
                self.combo_of.set(str(item_data[0]))
            else:
                self.combo_of.set("")
            
            if item_data[7] is not None:
                self.combo_produto.set(item_data[7])
            else:
                self.combo_produto.set("")
            
            if item_data[8] is not None:
                self.combo_cliente.set(item_data[8])
            else:
                self.combo_cliente.set("")
            
            self.entry_qtd.delete(0, tk.END)
            self.entry_qtd.insert(0, str(item_data[3] or ""))
            
            self.entry_unit.delete(0, tk.END)
            self.entry_unit.insert(0, str(item_data[4] or ""))
            
            self.entry_desc.delete(0, tk.END)
            self.entry_desc.insert(0, str(item_data[5] or ""))
            
            self.entry_total.delete(0, tk.END)
            self.entry_total.insert(0, str(item_data[6] or ""))

    def novo(self):
        # Limpar formulário para novo registro
        self.item_selecionado = None
        self.limpar()

    def salvar(self):
        try:
            id_of = int(self.combo_of.get())
            nome_produto = self.combo_produto.get()
            id_produto = next((id for id, nome in self.produtos if nome == nome_produto), None)

            nome_cliente = self.combo_cliente.get()
            cd_cliente = next((cd for cd, nome in self.clientes if nome == nome_cliente), None)

            qtd = int(self.entry_qtd.get())
            unit = float(self.entry_unit.get())
            desc = float(self.entry_desc.get())
            total = qtd * unit * (1 - desc / 100)

            conn = self.conectar()
            cursor = conn.cursor()
            
            if self.item_selecionado:
                # Atualizar registro existente
                cursor.execute("""
                    UPDATE alba0009 SET
                        id_of = ?, id_produto = ?, cd_cliente = ?, qt_produto = ?, 
                        vl_unitario = ?, pc_desc_coml = ?, pc_desc_fiscal = 0, 
                        vl_unit_final = ?, vl_produto = ?, vl_total = ?
                    WHERE recnum = ?
                """, (
                    id_of, id_produto, cd_cliente, qtd, unit,
                    desc, unit, total, total, self.item_selecionado
                ))
                messagebox.showinfo("Sucesso", "Item atualizado com sucesso!")
            else:
                # Inserir novo registro
                cursor.execute("""
                    INSERT INTO alba0009 (
                        id_of, id_produto, cd_cliente, qt_produto, vl_unitario,
                        pc_desc_coml, pc_desc_fiscal, vl_unit_final, vl_produto,
                        vl_total, fl_status, fl_comissao
                    ) VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?, ?, 'ATIVO', 'S')
                """, (
                    id_of, id_produto, cd_cliente, qtd, unit,
                    desc, unit, total, total
                ))
                messagebox.showinfo("Sucesso", "Item salvo com sucesso!")
                
            conn.commit()
            conn.close()
            self.limpar()
            self.carregar()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def remover(self):
        if not self.item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para remover")
            return
            
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este item?"):
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alba0009 WHERE recnum = ?", (self.item_selecionado,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Item removido com sucesso!")
            self.limpar()
            self.carregar()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.recnum, i.id_of,
                   p.nm_produto, c.nm_razao,
                   i.qt_produto, i.vl_unitario, i.vl_total
            FROM alba0009 i
            LEFT JOIN alba0005 p ON i.id_produto = p.id_produto
            LEFT JOIN alba0001 c ON i.cd_cliente = c.nr_cnpj_cpf
        """)
        
        # Armazenar os IDs para navegação
        self.lista_ids = []
        rows = cursor.fetchall()
        
        for row in rows:
            self.lista_ids.append(row[0])  # Armazenar o ID (recnum)
            self.tree.insert("", "end", values=row)
            
        conn.close()
        
        # Atualizar o contador de posição
        self.indice_atual = -1 if not self.lista_ids else 0
        self.atualizar_posicao()
        
        # Se houver registros, selecionar o primeiro
        if self.lista_ids and self.indice_atual == 0:
            self.carregar_registro(self.lista_ids[0])

    def limpar(self):
        self.item_selecionado = None
        self.combo_of.set("")
        self.combo_produto.set("")
        self.combo_cliente.set("")
        self.entry_qtd.delete(0, tk.END)
        self.entry_unit.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.entry_total.delete(0, tk.END)
    
    # Funções de navegação
    def primeiro(self):
        if not self.lista_ids:
            return
        self.indice_atual = 0
        self.carregar_registro(self.lista_ids[self.indice_atual])
        self.atualizar_posicao()
    
    def anterior(self):
        if not self.lista_ids or self.indice_atual <= 0:
            return
        self.indice_atual -= 1
        self.carregar_registro(self.lista_ids[self.indice_atual])
        self.atualizar_posicao()
    
    def proximo(self):
        if not self.lista_ids or self.indice_atual >= len(self.lista_ids) - 1:
            return
        self.indice_atual += 1
        self.carregar_registro(self.lista_ids[self.indice_atual])
        self.atualizar_posicao()
    
    def ultimo(self):
        if not self.lista_ids:
            return
        self.indice_atual = len(self.lista_ids) - 1
        self.carregar_registro(self.lista_ids[self.indice_atual])
        self.atualizar_posicao()
    
    def atualizar_posicao(self):
        """Atualiza o texto que mostra a posição atual na navegação"""
        total = len(self.lista_ids)
        posicao = self.indice_atual + 1 if self.indice_atual >= 0 else 0
        self.lbl_posicao.config(text=f"{posicao}/{total}")
    
    def carregar_registro(self, recnum):
        """Carrega um registro específico pelo seu recnum"""
        self.item_selecionado = recnum
        
        # Buscar dados completos do item no banco
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.id_of, i.id_produto, i.cd_cliente, i.qt_produto, 
                   i.vl_unitario, i.pc_desc_coml, i.vl_total,
                   p.nm_produto,
                   c.nm_razao
            FROM alba0009 i
            LEFT JOIN alba0005 p ON i.id_produto = p.id_produto
            LEFT JOIN alba0001 c ON i.cd_cliente = c.nr_cnpj_cpf
            WHERE i.recnum = ?
        """, (recnum,))
        
        item_data = cursor.fetchone()
        conn.close()
        
        if item_data:
            # Preencher os campos do formulário
            if item_data[0] is not None:
                self.combo_of.set(str(item_data[0]))
            else:
                self.combo_of.set("")
                
            if item_data[7] is not None:
                self.combo_produto.set(item_data[7])
            else:
                self.combo_produto.set("")
                
            if item_data[8] is not None:
                self.combo_cliente.set(item_data[8])
            else:
                self.combo_cliente.set("")
                
            self.entry_qtd.delete(0, tk.END)
            self.entry_qtd.insert(0, str(item_data[3] or ""))
            
            self.entry_unit.delete(0, tk.END)
            self.entry_unit.insert(0, str(item_data[4] or ""))
            
            self.entry_desc.delete(0, tk.END)
            self.entry_desc.insert(0, str(item_data[5] or ""))
            
            self.entry_total.delete(0, tk.END)
            self.entry_total.insert(0, str(item_data[6] or ""))
            
            # Selecionar o item na treeview
            for item in self.tree.get_children():
                if self.tree.item(item)["values"][0] == recnum:
                    self.tree.selection_set(item)
                    self.tree.focus(item)
                    self.tree.see(item)
                    break
