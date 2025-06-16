import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow

class AtividWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Cadastro de Atividades")
        self.geometry("700x500")
        self.resizable(False, False)

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

        ttkb.Label(input_frame, text="Descrição da Atividade").grid(row=0, column=0, sticky=tk.W)
        self.entry_desc = ttkb.Entry(input_frame, width=60)
        self.entry_desc.grid(row=0, column=1, pady=5, padx=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "descricao"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("descricao", text="Descrição")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("descricao", width=600, minwidth=400, anchor=tk.W)
        
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
        self.entry_desc.focus()

    def salvar(self):
        desc = self.entry_desc.get()
        if not desc:
            self.show_message("Descrição obrigatória.", "warning")
            return
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ativid (nm_atividade) VALUES (?)", (desc,))
        conn.commit()
        conn.close()
        self.limpar()
        self.carregar()
        self.show_message("Atividade salva com sucesso!", "success")

    def remover(self):
        item = self.tree.focus()
        if not item:
            self.show_message("Selecione uma atividade para remover.", "warning")
            return
            
        id_atividade = self.tree.item(item)["values"][0]
        
        # Confirmar remoção através da área de mensagens
        self.show_message("Pressione novamente 'Remover' para confirmar exclusão", "warning")

        def confirmar_remocao():
            try:
                conn = self.conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM ativid WHERE id_atividade = ?", (id_atividade,))
                conn.commit()
                conn.close()
                self.carregar()
                self.limpar()
                self.show_message("Atividade removida com sucesso!", "success")
            except sqlite3.Error as e:
                self.show_message(f"ERRO ao remover atividade: {str(e)}", "error")
            finally:
                self.btn_remover.config(command=self.remover)

        self.btn_remover.config(command=confirmar_remocao)
        self.after(10000, lambda: self.btn_remover.config(command=self.remover))

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_atividade, nm_atividade FROM ativid ORDER BY nm_atividade")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()
        
    def on_select(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item)["values"]
        if values:
            self.entry_desc.delete(0, tk.END)
            self.entry_desc.insert(0, values[1])

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.entry_desc.delete(0, tk.END)
            
