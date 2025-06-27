import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
from windows.base_window import BaseWindow

class AtividWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Cadastro de Atividades")
        self.config(width=700, height=500)
        self.recnum = None
        self.editing_record = None  # Para controlar se estamos editando um registro existente

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
        self.limpar()
        self.recnum = None
        self.editing_record = None
        self.entry_desc.focus()
        self.show_message("Campos limpos. Digite a descrição da nova atividade.", "info")

    def salvar(self):
        desc = self.entry_desc.get()
        if not desc:
            self.show_message("ATENÇÃO: Descrição obrigatória.", "warning")
            return
            
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            if self.editing_record:
                # Estamos editando um registro existente
                # Verifica se a descrição foi alterada e se já existe outra atividade com a nova descrição
                if desc != self.editing_record:
                    cursor.execute("SELECT id_atividade FROM ativid WHERE nm_atividade = ?", (desc,))
                    row = cursor.fetchone()
                    if row:
                        self.show_message(f"ERRO: Já existe uma atividade com a descrição '{desc}'.", "error")
                        conn.close()
                        return
                
                # Atualiza o registro existente usando o ID armazenado
                cursor.execute("UPDATE ativid SET nm_atividade = ? WHERE id_atividade = ?", 
                             (desc, self.current_id))
                self.show_message(f"Atividade '{desc}' atualizada com sucesso!", "success")
            else:
                # Novo registro
                cursor.execute("SELECT id_atividade FROM ativid WHERE nm_atividade = ?", (desc,))
                row = cursor.fetchone()
                
                if row:
                    self.show_message(f"ERRO: Já existe uma atividade com a descrição '{desc}'.", "error")
                    conn.close()
                    return
                
                # Insere novo registro
                cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM ativid")
                next_recnum = cursor.fetchone()[0]
                cursor.execute("INSERT INTO ativid (recnum, nm_atividade) VALUES (?, ?)", (next_recnum, desc))
                self.show_message(f"Atividade '{desc}' salva com sucesso!", "success")

            conn.commit()
            self.editing_record = None
            self.current_id = None
            self.limpar()
            self.carregar()
            
        except Exception as e:
            conn.rollback()
            self.show_message(f"ERRO ao salvar atividade: {str(e)}", "error")
        finally:
            conn.close()

    def remover(self):
        item = self.tree.focus()
        if not item:
            self.show_message("ATENÇÃO: Selecione uma atividade para remover.", "warning")
            return

        item_data = self.tree.item(item)
        if not item_data.get("values"):
            self.show_message("ATENÇÃO: Selecione um registro válido para remover.", "warning")
            return

        id_atividade = item_data["values"][0]
        desc_atividade = item_data["values"][1]

        # Confirmar remoção através da área de mensagens
        self.show_message(f"Pressione novamente 'Remover' para confirmar exclusão de '{desc_atividade}'", "warning")
        
        # Alterar temporariamente o comando do botão para confirmação
        def confirmar_remocao():
            try:
                conn = self.conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM ativid WHERE id_atividade = ?", (id_atividade,))
                conn.commit()
                conn.close()
                self.carregar()
                self.limpar()
                self.show_message(f"Atividade '{desc_atividade}' removida com sucesso!", "success")
            except Exception as e:
                self.show_message(f"ERRO ao remover atividade: {str(e)}", "error")
            finally:
                # Restaurar comando original do botão
                self.btn_remover.config(command=self.remover)
        
        # Alterar comando do botão temporariamente
        self.btn_remover.config(command=confirmar_remocao)
        
        # Restaurar comando original após 10 segundos
        self.after(10000, lambda: self.btn_remover.config(command=self.remover))

    def carregar(self):
        try:
            self.tree.delete(*self.tree.get_children())
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_atividade, nm_atividade FROM ativid ORDER BY nm_atividade")
            resultados = cursor.fetchall()
            for row in resultados:
                self.tree.insert("", "end", values=row)
            conn.close()
            self.show_message(f"Carregadas {len(resultados)} atividades", "success")
        except Exception as e:
            self.show_message(f"ERRO ao carregar dados: {str(e)}", "error")

    def on_select(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item)["values"]
        if values:
            self.current_id = values[0]  # Armazena o ID para edição
            self.editing_record = values[1]  # Armazena a descrição original
            self.entry_desc.delete(0, tk.END)
            self.entry_desc.insert(0, values[1])
            self.show_message(f"Atividade selecionada: {values[1]}", "info")

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.entry_desc.delete(0, tk.END)
        self.recnum = None
        self.editing_record = None
        self.current_id = None

    def ir_primeiro(self):
        """Navega para o primeiro registro"""
        children = self.tree.get_children()
        if children:
            first_item = children[0]
            self.tree.selection_set(first_item)
            self.tree.focus(first_item)
            self.tree.see(first_item)
            self.on_select(None)
            self.show_message("Primeiro registro selecionado", "info")

    def ir_ultimo(self):
        """Navega para o último registro"""
        children = self.tree.get_children()
        if children:
            last_item = children[-1]
            self.tree.selection_set(last_item)
            self.tree.focus(last_item)
            self.tree.see(last_item)
            self.on_select(None)
            self.show_message("Último registro selecionado", "info")

    def ir_anterior(self):
        """Navega para o registro anterior"""
        selection = self.tree.selection()
        if not selection:
            self.ir_ultimo()
            return

        current = selection[0]
        prev_item = self.tree.prev(current)
        if prev_item:
            self.tree.selection_set(prev_item)
            self.tree.focus(prev_item)
            self.tree.see(prev_item)
            self.on_select(None)
            self.show_message("Registro anterior selecionado", "info")
        else:
            self.ir_ultimo()

    def ir_proximo(self):
        """Navega para o próximo registro"""
        selection = self.tree.selection()
        if not selection:
            self.ir_primeiro()
            return

        current = selection[0]
        next_item = self.tree.next(current)
        if next_item:
            self.tree.selection_set(next_item)
            self.tree.focus(next_item)
            self.tree.see(next_item)
            self.on_select(None)
            self.show_message("Próximo registro selecionado", "info")
        else:
            self.ir_primeiro()
