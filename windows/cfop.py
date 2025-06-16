import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow

class CfopWindow(BaseWindow):
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

        # Separador visual
        separator2 = ttkb.Separator(toolbar_frame, orient=tk.VERTICAL)
        separator2.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

        # Container para busca
        search_container = ttkb.Frame(toolbar_frame)
        search_container.pack(side=tk.LEFT, padx=(10, 0))

        self.entry_busca = ttkb.Entry(search_container, width=30)
        self.entry_busca.pack(side=tk.LEFT, padx=(0, 5))

        ttkb.Button(search_container, text="🔍", command=self.buscar, width=3).pack(side=tk.LEFT)
        ttkb.Button(search_container, text="🔄", command=self.carregar, width=3).pack(side=tk.LEFT)

        # Área de mensagem
        self.lbl_mensagem = ttkb.Label(toolbar_frame, text="", padding=5)
        self.lbl_mensagem.pack(side=tk.RIGHT)

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
            self.show_message("Código e descrição são obrigatórios.", "warning")
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
                self.show_message("CFOP atualizado com sucesso!", "success")
            else:
                # Obter o próximo recnum
                cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM cfop")
                proximo_recnum = cursor.fetchone()[0]
                
                # Inserir novo registro
                cursor.execute("""INSERT INTO cfop (recnum, cd_cfop, nm_cfop, fl_impostos, fl_kardex) 
                                VALUES (?, ?, ?, ?, ?)""",
                             (proximo_recnum, codigo, descricao, impostos, kardex))
                self.show_message("CFOP salvo com sucesso!", "success")
            
            conn.commit()
        except Exception as e:
            self.show_message(f"Erro ao salvar: {str(e)}", "danger")
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
            self.show_message("Selecione um CFOP para remover.", "warning")
            return
            
        codigo = self.tree.item(item)["values"][0]
        
        self.show_message(f"CFOP {codigo} removido com sucesso!", "success")

        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM cfop WHERE cd_cfop = ?", (codigo,))
            conn.commit()
            self.show_message("CFOP removido com sucesso!", "success")
        except Exception as e:
            self.show_message(f"Erro ao remover: {str(e)}", "danger")
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

    def show_message(self, message, message_type="info"):
        """Exibe uma mensagem na área de mensagens"""
        self.lbl_mensagem.configure(text=message)
        if message_type == "success":
            self.lbl_mensagem.configure(bootstyle="success")
        elif message_type == "danger":
            self.lbl_mensagem.configure(bootstyle="danger")
        elif message_type == "warning":
            self.lbl_mensagem.configure(bootstyle="warning")
        else:
            self.lbl_mensagem.configure(bootstyle="info")

    def buscar(self):
        """Realiza a busca com base no texto inserido"""
        termo = self.entry_busca.get().strip().lower()
        self.tree.selection_remove(*self.tree.selection())

        if not termo:
            return

        for item in self.tree.get_children():
            valores = self.tree.item(item)["values"]
            if any(str(valor).lower().find(termo) >= 0 for valor in valores):
                self.tree.selection_add(item)
                self.tree.focus(item)
                self.tree.see(item)
                break
        self.entry_kardex.insert(0, kardex or "")

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.entry_codigo.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_impostos.delete(0, tk.END)
        self.entry_kardex.delete(0, tk.END)
        
