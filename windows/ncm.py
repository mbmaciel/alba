import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class NcmWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Consulta de NCM")
        self.config(width=700, height=500)
        
        # Variável para controlar se estamos editando um registro existente
        self.editing_record = None

        # Frame principal
        main_frame = ttkb.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para barra de ferramentas e mensagens
        top_frame = ttkb.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 15))

        # Barra de ferramentas no topo (lado esquerdo)
        toolbar_frame = ttkb.Frame(top_frame, relief="raised", borderwidth=2, padding=5)
        toolbar_frame.pack(side=tk.LEFT, fill=tk.Y)

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

        # Botão de busca
        search_container = ttkb.Frame(toolbar_frame)
        search_container.pack(side=tk.LEFT, padx=(10, 0))

        ttkb.Button(search_container, text="🔍", command=self.buscar_ncm, width=3).pack(side=tk.LEFT)
        ttkb.Button(search_container, text="🔄", command=self.carregar, width=3).pack(side=tk.LEFT)

        # Área de mensagens (lado direito)
        message_frame = ttkb.Frame(top_frame, relief="sunken", borderwidth=2, padding=5)
        message_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        ttkb.Label(message_frame, text="Mensagens:", font=("Arial", 8, "bold")).pack(anchor=tk.W)
        
        self.message_label = ttkb.Label(
            message_frame, 
            text="Sistema pronto para uso", 
            font=("Arial", 9),
            foreground="blue",
            wraplength=300
        )
        self.message_label.pack(anchor=tk.W, fill=tk.BOTH, expand=True)

        # Frame para campos de entrada
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        ttkb.Label(input_frame, text="Código NCM").grid(row=0, column=0, sticky=tk.W)
        self.entry_codigo = ttkb.Entry(input_frame, width=15)
        self.entry_codigo.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Descrição").grid(row=0, column=2, sticky=tk.W)
        self.entry_descricao = ttkb.Entry(input_frame, width=60)
        self.entry_descricao.grid(row=0, column=3, pady=5, padx=5)

        # Frame para busca
        search_frame = ttkb.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 15))

        ttkb.Label(search_frame, text="Buscar código NCM").grid(row=0, column=0, sticky=tk.W)
        self.entry_busca = ttkb.Entry(search_frame, width=30)
        self.entry_busca.grid(row=0, column=1, pady=5, padx=(5, 10))
        self.entry_busca.bind("<Return>", lambda e: self.buscar_ncm())

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("codigo", "descricao"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("codigo", text="Código")
        self.tree.heading("descricao", text="Descrição")
        self.tree.column("codigo", width=120, minwidth=100, anchor=tk.CENTER)
        self.tree.column("descricao", width=500, minwidth=300, anchor=tk.W)
        
        # Scrollbar para o Treeview
        scrollbar = ttkb.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def show_message(self, message, msg_type="info"):
        """Exibe mensagem na área de mensagens com cores baseadas no tipo"""
        colors = {
            "info": "blue",
            "success": "green", 
            "warning": "orange",
            "error": "red"
        }
        
        self.message_label.config(
            text=message,
            foreground=colors.get(msg_type, "blue")
        )

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.editing_record = None  # Reset do controle de edição
        self.limpar()
        self.entry_codigo.focus()
        self.show_message("Campos limpos. Digite os dados do novo NCM.", "info")

    def salvar(self):
        codigo = self.entry_codigo.get()
        descricao = self.entry_descricao.get()

        if not codigo or not descricao:
            self.show_message("ATENÇÃO: Preencha todos os campos obrigatórios.", "warning")
            return

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            if self.editing_record:
                # Estamos editando um registro existente
                # Verifica se o código foi alterado e se já existe outro registro com o novo código
                if codigo != self.editing_record:
                    cursor.execute("SELECT COUNT(*) FROM ncm WHERE cd_ncm = ?", (codigo,))
                    existe = cursor.fetchone()[0]
                    if existe:
                        self.show_message(f"ERRO: Já existe um registro com o código NCM '{codigo}'.", "error")
                        conn.close()
                        return
                
                # Atualiza o registro existente
                cursor.execute("UPDATE ncm SET cd_ncm = ?, nm_ncm = ? WHERE cd_ncm = ?", 
                             (codigo, descricao, self.editing_record))
                self.show_message(f"NCM '{codigo}' atualizado com sucesso!", "success")
            else:
                # Novo registro
                cursor.execute("SELECT COUNT(*) FROM ncm WHERE cd_ncm = ?", (codigo,))
                existe = cursor.fetchone()[0]
                
                if existe:
                    self.show_message(f"ERRO: Já existe um registro com o código NCM '{codigo}'.", "error")
                    conn.close()
                    return
                
                # Obter o próximo valor de recnum
                cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM ncm")
                next_recnum = cursor.fetchone()[0]
                cursor.execute("INSERT INTO ncm (recnum, cd_ncm, nm_ncm) VALUES (?, ?, ?)", 
                             (next_recnum, codigo, descricao))
                self.show_message(f"NCM '{codigo}' salvo com sucesso!", "success")

            conn.commit()
            self.editing_record = None  # Reset do controle de edição
            self.limpar()
            self.carregar()
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            if "UNIQUE constraint failed" in str(e):
                self.show_message("ERRO: Já existe um NCM com estes dados.", "error")
            else:
                self.show_message(f"ERRO de integridade: {str(e)}", "error")
        except sqlite3.Error as e:
            conn.rollback()
            self.show_message(f"ERRO ao salvar NCM: {str(e)}", "error")
        finally:
            conn.close()

    def remover(self):
        item = self.tree.focus()
        if not item:
            self.show_message("ATENÇÃO: Selecione um registro para remover.", "warning")
            return
            
        item_data = self.tree.item(item)
        if not item_data.get("values"):
            self.show_message("ATENÇÃO: Selecione um registro válido para remover.", "warning")
            return
            
        codigo = item_data["values"][0]
        descricao = item_data["values"][1]
        
        # Confirmar remoção através da área de mensagens
        self.show_message(f"Pressione novamente 'Remover' para confirmar exclusão do NCM '{codigo}'", "warning")
        
        # Alterar temporariamente o comando do botão para confirmação
        def confirmar_remocao():
            try:
                conn = self.conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM ncm WHERE cd_ncm = ?", (codigo,))
                conn.commit()
                conn.close()
                self.editing_record = None  # Reset do controle de edição
                self.limpar()
                self.carregar()
                self.show_message(f"NCM '{codigo}' removido com sucesso!", "success")
            except sqlite3.Error as e:
                self.show_message(f"ERRO ao remover NCM: {str(e)}", "error")
            finally:
                # Restaurar comando original do botão
                self.btn_remover.config(command=self.remover)
        
        # Alterar comando do botão temporariamente
        self.btn_remover.config(command=confirmar_remocao)
        
        # Restaurar comando original após 10 segundos
        self.after(10000, lambda: self.btn_remover.config(command=self.remover))

    def buscar_ncm(self):
        codigo = self.entry_busca.get()
        if not codigo:
            self.carregar()
            self.show_message("Busca limpa. Mostrando todos os NCMs.", "info")
            return
            
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT cd_ncm, nm_ncm FROM ncm WHERE cd_ncm LIKE ? OR nm_ncm LIKE ? ORDER BY cd_ncm", 
                      (f"%{codigo}%", f"%{codigo}%"))
        resultados = cursor.fetchall()
        conn.close()

        self.tree.delete(*self.tree.get_children())
        for row in resultados:
            self.tree.insert("", "end", values=row)
            
        if resultados:
            self.show_message(f"Encontrados {len(resultados)} NCM(s) com '{codigo}'", "success")
        else:
            self.show_message(f"Nenhum NCM encontrado com '{codigo}'", "warning")

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT cd_ncm, nm_ncm FROM ncm ORDER BY cd_ncm")
            resultados = cursor.fetchall()
            for row in resultados:
                self.tree.insert("", "end", values=row)
            conn.close()
            self.show_message(f"Carregados {len(resultados)} NCMs", "success")
        except sqlite3.Error as e:
            self.show_message(f"ERRO ao carregar NCMs: {str(e)}", "error")

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item or not item.get("values"):
            return
            
        codigo, descricao = item["values"]
        
        # Armazena o código original para controle de edição
        self.editing_record = codigo
        
        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, codigo)
        self.entry_descricao.delete(0, tk.END)
        self.entry_descricao.insert(0, descricao)
        self.show_message(f"NCM selecionado: {codigo}", "info")

    def limpar(self):
        self.entry_codigo.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_busca.delete(0, tk.END)
        self.editing_record = None

    # Métodos de navegação (podem ser implementados posteriormente)
    def ir_primeiro(self):
        items = self.tree.get_children()
        if items:
            self.tree.selection_set(items[0])
            self.tree.focus(items[0])
            self.on_select(None)
            self.show_message("Primeiro registro selecionado", "info")

    def ir_anterior(self):
        current = self.tree.focus()
        if current:
            prev_item = self.tree.prev(current)
            if prev_item:
                self.tree.selection_set(prev_item)
                self.tree.focus(prev_item)
                self.on_select(None)
                self.show_message("Registro anterior selecionado", "info")

    def ir_proximo(self):
        current = self.tree.focus()
        if current:
            next_item = self.tree.next(current)
            if next_item:
                self.tree.selection_set(next_item)
                self.tree.focus(next_item)
                self.on_select(None)
                self.show_message("Próximo registro selecionado", "info")

    def ir_ultimo(self):
        items = self.tree.get_children()
        if items:
            self.tree.selection_set(items[-1])
            self.tree.focus(items[-1])
            self.on_select(None)
            self.show_message("Último registro selecionado", "info")
