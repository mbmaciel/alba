import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class ComissaoWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Cadastro de Faixas de Comissão")
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


    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar()
        self.entry_ini.focus()
        self.show_message("Campos limpos. Digite os dados da nova faixa de comissão.", "info")

    def salvar(self):
        try:
            ini = float(self.entry_ini.get())
            fim = float(self.entry_fim.get())
            comissao = float(self.entry_comissao.get())
        except ValueError:
            self.show_message("ERRO: Insira valores numéricos válidos.", "error")
            return

        if ini < 0 or fim < 0 or comissao < 0:
            self.show_message("ATENÇÃO: Os valores devem ser positivos.", "warning")
            return

        if ini > fim:
            self.show_message("ATENÇÃO: O desconto inicial deve ser menor ou igual ao desconto final.", "warning")
            return

        try:
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
            self.show_message(f"Faixa de comissão {ini}% - {fim}% salva com sucesso!", "success")
        except sqlite3.Error as e:
            self.show_message(f"ERRO ao salvar faixa de comissão: {str(e)}", "error")

    def remover(self):
        item = self.tree.focus()
        if not item:
            self.show_message("ATENÇÃO: Selecione uma faixa de comissão para remover.", "warning")
            return
        
        item_values = self.tree.item(item)["values"]
        id_comissao = item_values[0]
        desc_ini = item_values[1]
        desc_fim = item_values[2]
        
        # Confirmar remoção através da área de mensagens
        self.show_message(f"Pressione novamente 'Remover' para confirmar exclusão da faixa {desc_ini}% - {desc_fim}%", "warning")
        
        # Alterar temporariamente o comando do botão para confirmação
        def confirmar_remocao():
            try:
                conn = self.conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM comissao WHERE id_comissao = ?", (id_comissao,))
                conn.commit()
                conn.close()
                self.carregar()
                self.limpar()
                self.show_message(f"Faixa de comissão {desc_ini}% - {desc_fim}% removida com sucesso!", "success")
            except sqlite3.Error as e:
                self.show_message(f"ERRO ao remover faixa de comissão: {str(e)}", "error")
            finally:
                # Restaurar comando original do botão
                self.btn_remover.config(command=self.remover)
        
        # Alterar comando do botão temporariamente
        self.btn_remover.config(command=confirmar_remocao)
        
        # Restaurar comando original após 10 segundos
        self.after(10000, lambda: self.btn_remover.config(command=self.remover))

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_comissao, pc_desc_ini, pc_desc_fim, pc_comissao FROM comissao ORDER BY pc_desc_ini")
            resultados = cursor.fetchall()
            for row in resultados:
                self.tree.insert("", "end", values=row)
            conn.close()
            self.show_message(f"Carregadas {len(resultados)} faixas de comissão", "success")
        except sqlite3.Error as e:
            self.show_message(f"ERRO ao carregar faixas de comissão: {str(e)}", "error")

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
            self.show_message(f"Faixa selecionada: {ini}% - {fim}%", "info")

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.entry_ini.delete(0, tk.END)
        self.entry_fim.delete(0, tk.END)
        self.entry_comissao.delete(0, tk.END)
        
