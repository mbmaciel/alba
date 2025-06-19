import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import sqlite3
from windows.base_window import BaseWindow

class TipoWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.set_title("Cadastro de Tipos de Clientes")
        self.config(width=700, height=500)

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

        # Área de mensagens ao lado dos comandos
        self.message_label = ttkb.Label(
            toolbar_frame, 
            text="", 
            font=("Arial", 9),
            padding=(10, 0)
        )
        self.message_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Frame para campos de entrada
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        ttkb.Label(input_frame, text="ID Tipo").grid(row=0, column=0, sticky=tk.W)
        self.entry_id = ttkb.Entry(input_frame, width=10)
        self.entry_id.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Nome do Tipo").grid(row=0, column=2, sticky=tk.W)
        self.entry_nome = ttkb.Entry(input_frame, width=50)
        self.entry_nome.grid(row=0, column=3, pady=5, padx=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id_tipo", "nm_tipo"), show="headings", height=15)
            
        # Configuração das colunas - ID menor, Descrição maior
        self.tree.heading("id_tipo", text="ID")
        self.tree.heading("nm_tipo", text="Descrição")
        self.tree.column("id_tipo", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("nm_tipo", width=500, minwidth=300, anchor=tk.W)
            
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
            "error": "red",
            "danger": "red"
        }
        
        self.message_label.config(
            text=message,
            foreground=colors.get(msg_type, "blue")
        )

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar()
        self.entry_id.focus()
        self.show_message("Pronto para novo registro", "info")

    def salvar(self):
        id_tipo = self.entry_id.get()
        nome = self.entry_nome.get()

        if not id_tipo or not nome:
            self.show_message("Preencha todos os campos", "warning")
            return

        try:
            id_tipo = int(id_tipo)
        except ValueError:
            self.show_message("ID deve ser um número", "error")
            return

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            # Verifica se já existe
            cursor.execute("SELECT COUNT(*) FROM tipo WHERE id_tipo = ?", (id_tipo,))
            existe = cursor.fetchone()[0]

            if existe:
                cursor.execute("UPDATE tipo SET nm_tipo = ? WHERE id_tipo = ?", (nome, id_tipo))
                self.show_message("Registro atualizado com sucesso!", "success")
            else:
                # Para INSERT, precisamos obter o próximo recnum
                cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM tipo")
                proximo_recnum = cursor.fetchone()[0]
                
                cursor.execute("INSERT INTO tipo (recnum, id_tipo, nm_tipo) VALUES (?, ?, ?)", 
                             (proximo_recnum, id_tipo, nome))
                self.show_message("Registro inserido com sucesso!", "success")

            conn.commit()
            self.limpar()
            self.carregar()
            
        except sqlite3.IntegrityError as e:
            self.show_message(f"Erro de integridade: {str(e)}", "error")
        except Exception as e:
            self.show_message(f"Erro ao salvar: {str(e)}", "error")
        finally:
            conn.close()

    def remover(self):
        item = self.tree.focus()
        if not item:
            self.show_message("Selecione um registro para remover", "warning")
            return
            
        values = self.tree.item(item)["values"]
        id_tipo = values[0]
        nome_tipo = values[1]
        
        # Usar messagebox apenas para confirmação (diálogo interativo)
        resposta = messagebox.askyesno("Confirmar", f"Deseja realmente remover o tipo '{nome_tipo}'?")
        if not resposta:
            self.show_message("Operação cancelada", "info")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM tipo WHERE id_tipo = ?", (id_tipo,))
            conn.commit()
            self.show_message("Registro removido com sucesso!", "success")
            self.carregar()
            self.limpar()
        except Exception as e:
            self.show_message(f"Erro ao remover: {str(e)}", "error")
        finally:
            conn.close()

    def carregar(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_tipo, nm_tipo FROM tipo ORDER BY id_tipo")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()
        self.show_message("Dados carregados", "info")

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item or not item["values"]:
            return
        id_tipo, nome = item["values"]
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, id_tipo)
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, nome)
        self.show_message(f"Registro selecionado: {nome}", "info")

    def limpar(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.show_message("Campos limpos", "info")
