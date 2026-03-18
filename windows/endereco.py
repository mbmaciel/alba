import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class EnderecoWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Cadastro de Endereços (alba0002)")
        self.config(width=900, height=550)

        self.current_recnum = None

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
        self.create_tooltip(self.btn_novo, "Novo")

        self.btn_salvar = ttkb.Button(button_container, text="💾", command=self.salvar, width=3)
        self.btn_salvar.pack(side=tk.LEFT)
        self.create_tooltip(self.btn_salvar, "Salvar")

        self.btn_remover = ttkb.Button(button_container, text="🗑️", command=self.remover, width=3)
        self.btn_remover.pack(side=tk.LEFT)
        self.create_tooltip(self.btn_remover, "Remover")

        # Separador visual
        separator = ttkb.Separator(toolbar_frame, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

        # Botões de navegação
        nav_container = ttkb.Frame(toolbar_frame)
        nav_container.pack(side=tk.LEFT, padx=(10, 0))

        btn_primeiro = ttkb.Button(nav_container, text="⏮", command=self.ir_primeiro, width=3)
        btn_primeiro.pack(side=tk.LEFT)
        self.create_tooltip(btn_primeiro, "Primeiro")
        
        btn_anterior = ttkb.Button(nav_container, text="◀", command=self.ir_anterior, width=3)
        btn_anterior.pack(side=tk.LEFT)
        self.create_tooltip(btn_anterior, "Anterior")
        
        btn_proximo = ttkb.Button(nav_container, text="▶", command=self.ir_proximo, width=3)
        btn_proximo.pack(side=tk.LEFT)
        self.create_tooltip(btn_proximo, "Próximo")
        
        btn_ultimo = ttkb.Button(nav_container, text="⏭", command=self.ir_ultimo, width=3)
        btn_ultimo.pack(side=tk.LEFT)
        self.create_tooltip(btn_ultimo, "Último")

        # Separador visual
        separator2 = ttkb.Separator(toolbar_frame, orient=tk.VERTICAL)
        separator2.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

        # Botão de refresh
        refresh_container = ttkb.Frame(toolbar_frame)
        refresh_container.pack(side=tk.LEFT, padx=(10, 0))

        btn_refresh = ttkb.Button(refresh_container, text="🔄", command=self.carregar, width=3)
        btn_refresh.pack(side=tk.LEFT)
        self.create_tooltip(btn_refresh, "Atualizar Lista")

        # Message panel frame (positioned after toolbar, before input fields)
        message_frame = ttkb.Frame(main_frame)
        message_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

        # Message frame title
        ttkb.Label(message_frame, text="Mensagens:", font=("Arial", 8, "bold")).pack(anchor=tk.W)

        # Message label with consistent styling
        self.message_label = ttkb.Label(
            message_frame, 
            text="Sistema pronto para uso", 
            foreground="blue",
            font=("Arial", 8),
            wraplength=400
        )
        self.message_label.pack(anchor=tk.W, fill=tk.BOTH, expand=True)

        # Frame para campos de entrada
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        # Primeira linha
        ttkb.Label(input_frame, text="Pessoa").grid(row=0, column=0, sticky=tk.W)
        self.combo_pessoa = ttkb.Combobox(input_frame, width=40, state="readonly")
        self.combo_pessoa.grid(row=0, column=1, columnspan=2, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Tipo").grid(row=0, column=3, sticky=tk.W)
        self.combo_tipo = ttkb.Combobox(input_frame, width=15, state="readonly")
        self.combo_tipo["values"] = ["E", "C", "F"]
        self.combo_tipo.grid(row=0, column=4, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="CEP").grid(row=0, column=5, sticky=tk.W)
        self.entry_cep = ttkb.Entry(input_frame, width=15)
        self.entry_cep.grid(row=0, column=6, pady=5, padx=5)

        # Segunda linha
        ttkb.Label(input_frame, text="Número").grid(row=1, column=0, sticky=tk.W)
        self.entry_numero = ttkb.Entry(input_frame, width=15)
        self.entry_numero.grid(row=1, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Complemento").grid(row=1, column=2, sticky=tk.W)
        self.entry_compl = ttkb.Entry(input_frame, width=40)
        self.entry_compl.grid(row=1, column=3, columnspan=4, pady=5, padx=(5, 0), sticky=tk.W+tk.E)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "pessoa", "tipo", "cep", "numero", "compl"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="COD")
        self.tree.heading("pessoa", text="Pessoa")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("cep", text="CEP")
        self.tree.heading("numero", text="Número")
        self.tree.heading("compl", text="Complemento")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("pessoa", width=250, minwidth=200, anchor=tk.W)
        self.tree.column("tipo", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column("cep", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column("numero", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("compl", width=200, minwidth=150, anchor=tk.W)
        
        # Scrollbar para o Treeview
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_pessoas()
        self.carregar()

    def create_tooltip(self, widget, text):
        """Cria um tooltip para o widget especificado"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            
            label = tk.Label(tooltip, text=text, background="lightyellow", 
                           relief="solid", borderwidth=1, font=("Arial", 8))
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar()
        self.combo_pessoa.focus()
        self.show_message("Campos limpos. Selecione a pessoa e preencha os dados do endereço.", "info")

    def carregar_pessoas(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_pessoa, nm_razao FROM alba0001 ORDER BY nm_razao")
            self.pessoas = cursor.fetchall()
            conn.close()
            self.combo_pessoa["values"] = [nome for _, nome in self.pessoas]
            self.show_message(f"Carregadas {len(self.pessoas)} pessoas", "success")
        except Exception as e:
            self.show_message(f"ERRO ao carregar pessoas: {str(e)}", "error")

    def _execute_save(self):
        try:
            nome_pessoa = self.combo_pessoa.get()
            id_pessoa = next((id for id, nome in self.pessoas if nome == nome_pessoa), None)
            tipo = self.combo_tipo.get()
            cep = self.entry_cep.get()
            numero = self.entry_numero.get()
            compl = self.entry_compl.get()

            conn = self.conectar()
            cursor = conn.cursor()

            if self.current_recnum is None:
                # Verificar se já existe um endereço do mesmo tipo para esta pessoa
                cursor.execute("""
                    SELECT COUNT(*) FROM alba0002 
                    WHERE id_pessoa = ? AND tp_ender = ?
                """, (id_pessoa, tipo))

                if cursor.fetchone()[0] > 0:
                    self.show_message(f"ERRO: Esta pessoa já possui um endereço do tipo '{tipo}'. Use a edição para alterar.", "error")
                    conn.close()
                    return

                cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM alba0002")
                self.current_recnum = cursor.fetchone()[0]
                cursor.execute("""
                    INSERT INTO alba0002 (recnum, id_pessoa, tp_ender, cd_cep, nr_numero, nm_compl)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (self.current_recnum, id_pessoa, tipo, cep, numero, compl))
                self.show_message(f"Endereço salvo com sucesso para {nome_pessoa}!", "success")
            else:
                # Para UPDATE, verificar se não está criando conflito com outro registro
                cursor.execute("""
                    SELECT COUNT(*) FROM alba0002 
                    WHERE id_pessoa = ? AND tp_ender = ? AND recnum != ?
                """, (id_pessoa, tipo, self.current_recnum))

                if cursor.fetchone()[0] > 0:
                    self.show_message(f"ERRO: Esta pessoa já possui outro endereço do tipo '{tipo}'.", "error")
                    conn.close()
                    return

                cursor.execute("""
                    UPDATE alba0002
                    SET id_pessoa=?, tp_ender=?, cd_cep=?, nr_numero=?, nm_compl=?
                    WHERE recnum=?
                """, (id_pessoa, tipo, cep, numero, compl, self.current_recnum))
                self.show_message(f"Endereço atualizado com sucesso para {nome_pessoa}!", "success")

            conn.commit()
            conn.close()
            self.limpar()
            self.carregar()
        except Exception as e:
            self.show_message(f"ERRO ao salvar: {str(e)}", "error")

    def salvar(self):
        try:
            nome_pessoa = self.combo_pessoa.get()
            id_pessoa = next((id for id, nome in self.pessoas if nome == nome_pessoa), None)
            tipo = self.combo_tipo.get()
            cep = self.entry_cep.get()
            numero = self.entry_numero.get()
            compl = self.entry_compl.get()

            if not id_pessoa or not cep:
                self.show_message("ATENÇÃO: Preencha os campos obrigatórios (Pessoa e CEP).", "warning")
                return

            if not tipo:
                self.show_message("ATENÇÃO: Selecione o tipo de endereço.", "warning")
                return

            confirmation_message = f"Confirma a gravação do endereço para '{nome_pessoa}'?"
            if not hasattr(self, '_confirmations'):
                self.setup_confirmation_pattern('save')

            if not self.request_confirmation('save', confirmation_message, self._execute_save):
                return

        except sqlite3.IntegrityError as e:
            error_msg = str(e)
            if "UNIQUE constraint failed" in error_msg and "id_pessoa" in error_msg and "tp_ender" in error_msg:
                self.show_message("ERRO: Esta pessoa já possui um endereço deste tipo. Cada pessoa pode ter apenas um endereço por tipo.", "error")
            else:
                self.show_message(f"ERRO de integridade: {error_msg}", "error")
        except Exception as e:
            self.show_message(f"ERRO ao salvar: {str(e)}", "error")

    def _execute_removal(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alba0002 WHERE recnum = ?", (self.current_recnum,))
            conn.commit()
            conn.close()
            self.show_message(f"Endereço removido com sucesso!", "success")
            self.limpar()
            self.carregar()
        except Exception as e:
            self.show_message(f"ERRO ao remover: {str(e)}", "error")

    def remover(self):
        try:
            item = self.tree.focus()
            if not item:
                self.show_message("ATENÇÃO: Selecione um registro para remover.", "warning")
                return

            item_data = self.tree.item(item)
            if not item_data.get("values"):
                self.show_message("ATENÇÃO: Selecione um registro válido para remover.", "warning")
                return

            pessoa_nome = item_data["values"][1]
            tipo_endereco = item_data["values"][2]

            confirmation_message = f"Pressione 'Remover' novamente para excluir o endereço {tipo_endereco} de {pessoa_nome}."

            if not hasattr(self, '_confirmations'):
                self.setup_confirmation_pattern('remove')

            if not self.request_confirmation('remove', confirmation_message, self._execute_removal):
                return

        except Exception as e:
            self.show_message(f"ERRO ao remover: {str(e)}", "error")

    def carregar(self):
        try:
            self.tree.delete(*self.tree.get_children())
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.recnum, e.id_pessoa, e.tp_ender, e.cd_cep, e.nr_numero, e.nm_compl, p.nm_razao
                FROM alba0002 e
                LEFT JOIN alba0001 p ON e.id_pessoa = p.id_pessoa
                ORDER BY e.recnum
            """)
            resultados = cursor.fetchall()
            for row in resultados:
                recnum, id_pessoa, tipo, cep, numero, compl, nome = row
                self.tree.insert("", "end", values=(recnum, nome or f"ID {id_pessoa}", tipo, cep, numero, compl))
            conn.close()
            self.show_message(f"Carregados {len(resultados)} endereços", "success")
        except Exception as e:
            self.show_message(f"ERRO ao carregar dados: {str(e)}", "error")

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item or not item.get("values"):
            return
        
        recnum, pessoa_nome, tipo, cep, numero, compl = item["values"]
        self.current_recnum = recnum
        
        self.combo_pessoa.set(pessoa_nome or "")
        self.combo_tipo.set(tipo or "")
        
        self.entry_cep.delete(0, tk.END)
        self.entry_cep.insert(0, cep or "")
        
        self.entry_numero.delete(0, tk.END)
        self.entry_numero.insert(0, numero or "")
        
        self.entry_compl.delete(0, tk.END)
        self.entry_compl.insert(0, compl or "")
        
        self.show_message(f"Endereço selecionado: {pessoa_nome} - {tipo}", "info")

    def show_message(self, message, msg_type="info"):
        """Enhanced message display with consistent styling and behavior"""
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
        
        # Auto-clear message after 5 seconds for non-error messages
        if msg_type != "error":
            self.after(5000, lambda: self.message_label.config(
                text="Sistema pronto para uso", 
                foreground="blue"
            ))

    def limpar(self):
        self.combo_pessoa.set("")
        self.combo_tipo.set("")
        self.entry_cep.delete(0, tk.END)
        self.entry_numero.delete(0, tk.END)
        self.entry_compl.delete(0, tk.END)
        self.current_recnum = None
        self.show_message("Campos limpos", "info")

    def ir_primeiro(self):
        if self.tree.get_children():
            primeiro = self.tree.get_children()[0]
            self.tree.selection_set(primeiro)
            self.tree.focus(primeiro)
            self.on_select(None)
            self.show_message("Primeiro registro selecionado", "info")

    def ir_ultimo(self):
        if self.tree.get_children():
            ultimo = self.tree.get_children()[-1]
            self.tree.selection_set(ultimo)
            self.tree.focus(ultimo)
            self.on_select(None)
            self.show_message("Último registro selecionado", "info")

    def ir_anterior(self):
        selecionado = self.tree.selection()
        if selecionado:
            indice = self.tree.index(selecionado[0])
            if indice > 0:
                anterior = self.tree.get_children()[indice - 1]
                self.tree.selection_set(anterior)
                self.tree.focus(anterior)
                self.on_select(None)
                self.show_message("Registro anterior selecionado", "info")
        else:
            self.ir_ultimo()

    def ir_proximo(self):
        selecionado = self.tree.selection()
        if selecionado:
            indice = self.tree.index(selecionado[0])
            if indice < len(self.tree.get_children()) - 1:
                proximo = self.tree.get_children()[indice + 1]
                self.tree.selection_set(proximo)
                self.tree.focus(proximo)
                self.on_select(None)
                self.show_message("Próximo registro selecionado", "info")
        else:
            self.ir_primeiro()
        
