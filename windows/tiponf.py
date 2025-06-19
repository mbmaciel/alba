import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class TiponfWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_id = None
        aplicar_estilo(self)
        self.set_title("Cadastro de Tipos de Nota Fiscal")
        self.config(width=800, height=550)

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

        ttkb.Label(input_frame, text="Nome").grid(row=0, column=0, sticky=tk.W)
        self.entry_nome = ttkb.Entry(input_frame, width=40)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Tipo (fl_tiponf)").grid(row=1, column=0, sticky=tk.W)
        self.combo_tipo = ttkb.Combobox(input_frame, width=27, values=["M", "S"], state="readonly")
        self.combo_tipo.grid(row=1, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Mapa (fl_mapa)").grid(row=2, column=0, sticky=tk.W)
        self.var_mapa = tk.BooleanVar()
        self.check_mapa = ttkb.Checkbutton(input_frame, text="Ativo", variable=self.var_mapa)
        self.check_mapa.grid(row=2, column=1, pady=5, padx=(5, 20), sticky=tk.W)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "nome", "tipo", "mapa"), show="headings", height=15)

        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("mapa", text="Mapa")

        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("nome", width=300, minwidth=200, anchor=tk.W)
        self.tree.column("tipo", width=150, minwidth=100, anchor=tk.CENTER)
        self.tree.column("mapa", width=150, minwidth=100, anchor=tk.CENTER)

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
        self.current_id = None
        self.limpar()
        self.entry_nome.focus()
        self.show_message("Novo registro. Preencha os campos e salve.", "info")

    def salvar(self):
        try:
            nome = self.entry_nome.get()
            tipo = self.combo_tipo.get()
            mapa = "1" if self.var_mapa.get() else "0"

            if not nome:
                self.show_message("Nome é obrigatório.", "warning")
                return

            conn = self.conectar()
            cursor = conn.cursor()

            try:
                if self.current_id is None:
                    # Novo registro
                    cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM tiponf")
                    next_recnum = cursor.fetchone()[0]

                    cursor.execute(
                        "INSERT INTO tiponf (recnum, nm_tiponf, fl_tiponf, fl_mapa) VALUES (?, ?, ?, ?)",
                        (next_recnum, nome, tipo, mapa)
                    )
                    self.show_message(f"Tipo de NF '{nome}' incluído com sucesso!", "success")
                else:
                    # Atualização
                    cursor.execute(
                        "UPDATE tiponf SET nm_tiponf=?, fl_tiponf=?, fl_mapa=? WHERE id_tiponf=?",
                        (nome, tipo, mapa, self.current_id)
                    )
                    self.show_message(f"Tipo de NF '{nome}' atualizado com sucesso!", "success")

                conn.commit()
                self.limpar()
                self.carregar()
                self.current_id = None

            except sqlite3.Error as e:
                self.show_message(f"Erro ao salvar registro: {str(e)}", "error")
                conn.rollback()
            finally:
                conn.close()

        except Exception as e:
            self.show_message(f"Erro inesperado: {str(e)}", "error")

    def remover(self):
        try:
            item = self.tree.focus()
            if not item:
                self.show_message("Selecione um registro para remover.", "warning")
                return

            item_values = self.tree.item(item)["values"]
            id_tiponf = item_values[0]
            nome = item_values[1]
            
            # Confirmar remoção através da área de mensagens
            self.show_message(f"Pressione novamente 'Remover' para confirmar exclusão de '{nome}'", "warning")
            
            # Alterar temporariamente o comando do botão para confirmação
            def confirmar_remocao():
                try:
                    conn = self.conectar()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM tiponf WHERE id_tiponf = ?", (id_tiponf,))
                    conn.commit()
                    conn.close()
                    self.carregar()
                    self.limpar()
                    self.show_message(f"Tipo de NF '{nome}' removido com sucesso!", "success")
                except sqlite3.Error as e:
                    self.show_message(f"Erro ao remover: {str(e)}", "error")
                finally:
                    # Restaurar comando original do botão
                    self.btn_remover.config(command=self.remover)
            
            # Alterar comando do botão temporariamente
            self.btn_remover.config(command=confirmar_remocao)
            
            # Restaurar comando original após 10 segundos
            self.after(10000, lambda: self.btn_remover.config(command=self.remover))

        except Exception as e:
            self.show_message(f"Erro inesperado: {str(e)}", "error")

    def carregar(self):
        try:
            self.tree.delete(*self.tree.get_children())
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_tiponf, nm_tiponf, fl_tiponf, fl_mapa FROM tiponf ORDER BY nm_tiponf")
            resultados = cursor.fetchall()
            for row in resultados:
                self.tree.insert("", "end", values=row)
            conn.close()
            self.show_message(f"Carregados {len(resultados)} tipos de nota fiscal", "success")
        except sqlite3.Error as e:
            self.show_message(f"Erro ao carregar dados: {str(e)}", "error")

    def on_select(self, event):
        try:
            item = self.tree.item(self.tree.focus())
            if not item or not item.get("values"):
                return
            
            values = item["values"]
            if len(values) >= 4:
                id_tiponf, nome, tipo, mapa = values
                self.current_id = id_tiponf
                
                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, nome or "")
                
                self.combo_tipo.set(tipo if tipo else "")

                # Buscar o valor real do mapa no banco de dados
                conn = self.conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT fl_mapa FROM tiponf WHERE id_tiponf = ?", (self.current_id,))
                result = cursor.fetchone()
                if result:
                    mapa_value = result[0]
                    # Converter para boolean - aceita tanto string quanto número
                    self.var_mapa.set(str(mapa_value) == "1" or mapa_value == 1)
                conn.close()
                
                self.show_message(f"Tipo selecionado para edição: {nome}", "info")
        except Exception as e:
            self.show_message(f"Erro ao selecionar: {str(e)}", "error")

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.current_id = None
        self.entry_nome.delete(0, tk.END)
        self.combo_tipo.set("")
        self.var_mapa.set(False)

    def show_message(self, message, msg_type="info"):
        """Exibe mensagem na interface"""
        colors = {
            "success": "green",
            "error": "red",
            "warning": "orange",
            "info": "blue"
        }
        self.message_label.config(text=message, foreground=colors.get(msg_type, "black"))
        # Auto-limpar mensagem após 5 segundos
        self.after(5000, lambda: self.message_label.config(text="Sistema pronto para uso", foreground="blue"))

    def ir_primeiro(self):
        try:
            items = self.tree.get_children()
            if items:
                first_item = items[0]
                self.tree.selection_set(first_item)
                self.tree.focus(first_item)
                self.tree.see(first_item)
                self.on_select(None)
        except Exception as e:
            self.show_message(f"Erro ao navegar: {str(e)}", "error")

    def ir_anterior(self):
        try:
            selection = self.tree.selection()
            if not selection:
                self.ir_primeiro()
                return

            current_index = self.tree.index(selection[0])
            if current_index > 0:
                prev_item = self.tree.get_children()[current_index - 1]
                self.tree.selection_set(prev_item)
                self.tree.focus(prev_item)
                self.tree.see(prev_item)
                self.on_select(None)
        except Exception as e:
            self.show_message(f"Erro ao navegar: {str(e)}", "error")

    def ir_proximo(self):
        try:
            selection = self.tree.selection()
            if not selection:
                self.ir_primeiro()
                return

            current_index = self.tree.index(selection[0])
            items = self.tree.get_children()
            if current_index < len(items) - 1:
                next_item = items[current_index + 1]
                self.tree.selection_set(next_item)
                self.tree.focus(next_item)
                self.tree.see(next_item)
                self.on_select(None)
        except Exception as e:
            self.show_message(f"Erro ao navegar: {str(e)}", "error")

    def ir_ultimo(self):
        try:
            items = self.tree.get_children()
            if items:
                last_item = items[-1]
                self.tree.selection_set(last_item)
                self.tree.focus(last_item)
                self.tree.see(last_item)
                self.on_select(None)
        except Exception as e:
            self.show_message(f"Erro inesperado: {str(e)}", "error")
        
