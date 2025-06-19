import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class NatopWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_id = None  # Para controlar inserção/atualização
        aplicar_estilo(self)
        self.set_title("Cadastro de Naturezas da Operação (NATOP)")
        self.config(width=900, height=500)

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
            wraplength=300,
        )
        self.message_label.pack(anchor=tk.W, fill=tk.BOTH, expand=True)

        # Frame para campos de entrada
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        # Primeira linha
        ttkb.Label(input_frame, text="Descrição").grid(row=0, column=0, sticky=tk.W)
        self.entry_desc = ttkb.Entry(input_frame, width=40)
        self.entry_desc.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="CFOP").grid(row=0, column=2, sticky=tk.W)
        self.entry_cfop = ttkb.Entry(input_frame, width=20)
        self.entry_cfop.grid(row=0, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Fluxo").grid(row=0, column=4, sticky=tk.W)
        self.entry_fluxo = ttkb.Entry(input_frame, width=20)
        self.entry_fluxo.grid(row=0, column=5, pady=5, padx=5)

        # Segunda linha
        ttkb.Label(input_frame, text="Livro Entrada").grid(row=1, column=0, sticky=tk.W)
        self.entry_ent = ttkb.Entry(input_frame, width=15)
        self.entry_ent.grid(row=1, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Livro Saída").grid(row=1, column=2, sticky=tk.W)
        self.entry_sai = ttkb.Entry(input_frame, width=15)
        self.entry_sai.grid(row=1, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Livro Serviço").grid(row=1, column=4, sticky=tk.W)
        self.entry_srv = ttkb.Entry(input_frame, width=15)
        self.entry_srv.grid(row=1, column=5, pady=5, padx=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "desc", "cfop", "fluxo", "ent", "sai", "srv"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("desc", text="Descrição")
        self.tree.heading("cfop", text="CFOP")
        self.tree.heading("fluxo", text="Fluxo")
        self.tree.heading("ent", text="Livro Ent.")
        self.tree.heading("sai", text="Livro Saí.")
        self.tree.heading("srv", text="Livro Srv.")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("desc", width=300, minwidth=200, anchor=tk.W)
        self.tree.column("cfop", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("fluxo", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("ent", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("sai", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("srv", width=80, minwidth=60, anchor=tk.CENTER)
        
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
        self.entry_desc.focus()
        self.show_message("Novo registro. Preencha os campos e salve.", "info")

    def salvar(self):
        try:
            desc = self.entry_desc.get()
            cfop = self.entry_cfop.get()
            fluxo = self.entry_fluxo.get()
            ent = self.entry_ent.get()
            sai = self.entry_sai.get()
            srv = self.entry_srv.get()

            if not desc or not cfop:
                self.show_message("Preencha os campos obrigatórios (Descrição e CFOP).", "warning")
                return

            conn = self.conectar()
            cursor = conn.cursor()

            try:
                if self.current_id is None:
                    # Novo registro - INSERT
                    # Verificar se CFOP já existe
                    cursor.execute("SELECT COUNT(*) FROM natop WHERE cd_cfop = ?", (cfop,))
                    existe = cursor.fetchone()[0]
                    
                    if existe:
                        self.show_message(f"CFOP {cfop} já existe! Use um CFOP diferente.", "warning")
                        return

                    cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM natop")
                    next_recnum = cursor.fetchone()[0]

                    cursor.execute("""
                        INSERT INTO natop (recnum, ds_natop, cd_cfop, fl_fluxo, fl_livro_ent, fl_livro_sai, fl_livro_srv)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (next_recnum, desc, cfop, fluxo, ent, sai, srv)
                    )
                    self.show_message("NATOP incluído com sucesso!", "success")
                else:
                    # Atualização - UPDATE
                    # Verificar se CFOP já existe em outro registro
                    cursor.execute("SELECT COUNT(*) FROM natop WHERE cd_cfop = ? AND id_natop != ?", (cfop, self.current_id))
                    existe = cursor.fetchone()[0]
                    
                    if existe:
                        self.show_message(f"CFOP {cfop} já existe em outro registro!", "warning")
                        return

                    cursor.execute("""
                        UPDATE natop SET ds_natop=?, cd_cfop=?, fl_fluxo=?, fl_livro_ent=?, fl_livro_sai=?, fl_livro_srv=?
                        WHERE id_natop=?""",
                        (desc, cfop, fluxo, ent, sai, srv, self.current_id)
                    )
                    self.show_message("NATOP atualizado com sucesso!", "success")

                conn.commit()
                self.limpar()
                self.carregar()

            except sqlite3.Error as e:
                self.show_message(f"Erro ao salvar: {str(e)}", "error")
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
                
            id_natop = self.tree.item(item)["values"][0]
            desc_natop = self.tree.item(item)["values"][1]
            
            # Confirmar remoção através da área de mensagens
            self.show_message(f"Pressione novamente 'Remover' para confirmar exclusão de '{desc_natop}'", "warning")
            
            # Alterar temporariamente o comando do botão para confirmação
            def confirmar_remocao():
                try:
                    conn = self.conectar()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM natop WHERE id_natop = ?", (id_natop,))
                    conn.commit()
                    conn.close()
                    self.carregar()
                    self.limpar()
                    self.show_message(f"NATOP '{desc_natop}' removido com sucesso!", "success")
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
            cursor.execute("SELECT id_natop, ds_natop, cd_cfop, fl_fluxo, fl_livro_ent, fl_livro_sai, fl_livro_srv FROM natop ORDER BY ds_natop")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            conn.close()
        except sqlite3.Error as e:
            self.show_message(f"Erro ao carregar dados: {str(e)}", "error")

    def on_select(self, event):
        try:
            item = self.tree.item(self.tree.focus())
            if not item or not item.get("values"):
                return
                
            id_natop, desc, cfop, fluxo, ent, sai, srv = item["values"]
            self.current_id = id_natop  # Armazenar ID para edição
            
            self.entry_desc.delete(0, tk.END)
            self.entry_desc.insert(0, desc or "")
            
            self.entry_cfop.delete(0, tk.END)
            self.entry_cfop.insert(0, cfop or "")
            
            self.entry_fluxo.delete(0, tk.END)
            self.entry_fluxo.insert(0, fluxo or "")
            
            self.entry_ent.delete(0, tk.END)
            self.entry_ent.insert(0, ent or "")
            
            self.entry_sai.delete(0, tk.END)
            self.entry_sai.insert(0, sai or "")
            
            self.entry_srv.delete(0, tk.END)
            self.entry_srv.insert(0, srv or "")
            
            self.show_message(f"NATOP selecionado para edição: {desc}", "info")
            
        except Exception as e:
            self.show_message(f"Erro ao selecionar: {str(e)}", "error")

    def limpar(self):
        self.current_id = None
        self.entry_desc.delete(0, tk.END)
        self.entry_cfop.delete(0, tk.END)
        self.entry_fluxo.delete(0, tk.END)
        self.entry_ent.delete(0, tk.END)
        self.entry_sai.delete(0, tk.END)
        self.entry_srv.delete(0, tk.END)

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

    # Métodos de navegação
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
            self.show_message(f"Erro ao navegar: {str(e)}", "error")