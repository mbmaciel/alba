import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class ContatoWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Cadastro de Contatos")
        self.config(width=900, height=600)

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

        self.btn_salvar = ttkb.Button(button_container, text="💾", command=self.salvar_contato, width=3)
        self.btn_salvar.pack(side=tk.LEFT)

        self.btn_remover = ttkb.Button(button_container, text="🗑️", command=self.remover_contato, width=3)
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

        ttkb.Button(search_container, text="🔍", command=self.buscar_contato, width=3).pack(side=tk.LEFT)
        ttkb.Button(search_container, text="🔄", command=self.carregar_contatos, width=3).pack(side=tk.LEFT)

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
        ttkb.Label(input_frame, text="Nome do Contato").grid(row=0, column=0, sticky=tk.W)
        self.entry_nome = ttkb.Entry(input_frame, width=45)
        self.entry_nome.grid(row=0, column=1, columnspan=2, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Departamento").grid(row=0, column=3, sticky=tk.W)
        self.entry_depto = ttkb.Entry(input_frame, width=30)
        self.entry_depto.grid(row=0, column=4, pady=5, padx=5)

        # Segunda linha
        ttkb.Label(input_frame, text="DDD").grid(row=1, column=0, sticky=tk.W)
        self.entry_ddd = ttkb.Entry(input_frame, width=10)
        self.entry_ddd.grid(row=1, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Telefone").grid(row=1, column=2, sticky=tk.W)
        self.entry_telefone = ttkb.Entry(input_frame, width=20)
        self.entry_telefone.grid(row=1, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Ramal").grid(row=1, column=4, sticky=tk.W)
        self.entry_ramal = ttkb.Entry(input_frame, width=15)
        self.entry_ramal.grid(row=1, column=5, pady=5, padx=5)

        # Terceira linha
        ttkb.Label(input_frame, text="DDD Celular").grid(row=2, column=0, sticky=tk.W)
        self.entry_ddd_cel = ttkb.Entry(input_frame, width=10)
        self.entry_ddd_cel.grid(row=2, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Celular").grid(row=2, column=2, sticky=tk.W)
        self.entry_celular = ttkb.Entry(input_frame, width=20)
        self.entry_celular.grid(row=2, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Email").grid(row=2, column=4, sticky=tk.W)
        self.entry_email = ttkb.Entry(input_frame, width=30)
        self.entry_email.grid(row=2, column=5, pady=5, padx=5)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "nome", "ddd", "telefone", "celular", "depto", "email"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("ddd", text="DDD")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("celular", text="Celular")
        self.tree.heading("depto", text="Departamento")
        self.tree.heading("email", text="Email")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("nome", width=200, minwidth=150, anchor=tk.W)
        self.tree.column("ddd", width=60, minwidth=50, anchor=tk.CENTER)
        self.tree.column("telefone", width=120, minwidth=100, anchor=tk.CENTER)
        self.tree.column("celular", width=120, minwidth=100, anchor=tk.CENTER)
        self.tree.column("depto", width=150, minwidth=100, anchor=tk.W)
        self.tree.column("email", width=200, minwidth=150, anchor=tk.W)
        
        # Scrollbar para o Treeview
        scrollbar = ttkb.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_contatos()


    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar_campos()
        self.entry_nome.focus()
        self.show_message("Campos limpos. Digite os dados do novo contato.", "info")

    def buscar_contato(self):
        nome_busca = self.entry_nome.get()
        if not nome_busca:
            self.carregar_contatos()
            self.show_message("Busca limpa. Mostrando todos os contatos.", "info")
            return
            
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_contato, nm_contato, nr_ddd_fone, nr_telefone, nr_celular, nm_depto, nm_email
            FROM contatos 
            WHERE nm_contato LIKE ?
            ORDER BY nm_contato
        """, (f'%{nome_busca}%',))
        
        resultados = cursor.fetchall()
        for row in resultados:
            # Formatar celular com DDD
            id_contato, nome, ddd, telefone, celular, depto, email = row
            celular_formatado = f"{row[4] or ''}"  # nr_celular já pode conter DDD
            self.tree.insert("", "end", values=(id_contato, nome, ddd, telefone, celular_formatado, depto, email))
        
        conn.close()
        
        if resultados:
            self.show_message(f"Encontrados {len(resultados)} contato(s) com '{nome_busca}'", "success")
        else:
            self.show_message(f"Nenhum contato encontrado com '{nome_busca}'", "warning")

    def salvar_contato(self):
        nome = self.entry_nome.get()
        ddd = self.entry_ddd.get()
        telefone = self.entry_telefone.get()
        ramal = self.entry_ramal.get()
        ddd_cel = self.entry_ddd_cel.get()
        celular = self.entry_celular.get()
        depto = self.entry_depto.get()
        email = self.entry_email.get()

        if not nome or not telefone:
            self.show_message("ATENÇÃO: Preencha os campos obrigatórios: Nome e Telefone.", "warning")
            return

        conn = self.conectar()
        try:
            cursor = conn.cursor()
            
            # Get next recnum value
            cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM contatos")
            next_recnum = cursor.fetchone()[0]
            
            # Insert without specifying id_contato (let it auto-increment)
            cursor.execute("""
                INSERT INTO contatos (recnum, nm_contato, nr_ddd_fone, nr_telefone, nr_ramal, nr_ddd_cel, nr_celular, nm_depto, nm_email) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (next_recnum, nome, ddd, telefone, ramal, ddd_cel, celular, depto, email))
            
            conn.commit()
            self.limpar_campos()
            self.carregar_contatos()
            self.show_message(f"Contato '{nome}' salvo com sucesso!", "success")
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            if "UNIQUE constraint failed" in str(e):
                self.show_message("ERRO: Já existe um contato com estes dados.", "error")
            else:
                self.show_message(f"ERRO de integridade: {str(e)}", "error")
        except sqlite3.Error as e:
            conn.rollback()
            self.show_message(f"ERRO ao salvar contato: {str(e)}", "error")
        finally:
            conn.close()

    def remover_contato(self):
        selecionado = self.tree.focus()
        if not selecionado:
            self.show_message("ATENÇÃO: Selecione um contato para remover.", "warning")
            return
        
        item = self.tree.item(selecionado)
        contato_id = item["values"][0]
        nome_contato = item["values"][1]
        
        # Confirmar remoção através da área de mensagens
        self.show_message(f"Pressione novamente 'Remover' para confirmar exclusão de '{nome_contato}'", "warning")
        
        # Alterar temporariamente o comando do botão para confirmação
        def confirmar_remocao():
            try:
                conn = self.conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM contatos WHERE id_contato = ?", (contato_id,))
                conn.commit()
                conn.close()
                self.carregar_contatos()
                self.limpar_campos()
                self.show_message(f"Contato '{nome_contato}' removido com sucesso!", "success")
            except sqlite3.Error as e:
                self.show_message(f"ERRO ao remover contato: {str(e)}", "error")
            finally:
                # Restaurar comando original do botão
                self.btn_remover.config(command=self.remover_contato)
        
        # Alterar comando do botão temporariamente
        self.btn_remover.config(command=confirmar_remocao)
        
        # Restaurar comando original após 10 segundos
        self.after(10000, lambda: self.btn_remover.config(command=self.remover_contato))

    def carregar_contatos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_contato, nm_contato, nr_ddd_fone, nr_telefone, nr_celular, nm_depto, nm_email 
                FROM contatos 
                ORDER BY nm_contato
            """)
            
            resultados = cursor.fetchall()
            for row in resultados:
                # Formatar celular com DDD
                id_contato, nome, ddd, telefone, celular, depto, email = row
                celular_formatado = f"{celular or ''}"
                self.tree.insert("", "end", values=(id_contato, nome, ddd, telefone, celular_formatado, depto, email))
            
            conn.close()
            self.show_message(f"Carregados {len(resultados)} contatos", "success")
            
        except sqlite3.Error as e:
            self.show_message(f"ERRO ao carregar contatos: {str(e)}", "error")

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        
        contato_id = item["values"][0]
        nome_selecionado = item["values"][1]
        
        try:
            # Buscar todos os dados do contato selecionado
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT nm_contato, nr_ddd_fone, nr_telefone, nr_ramal, nr_ddd_cel, nr_celular, nm_depto, nm_email
                FROM contatos 
                WHERE id_contato = ?
            """, (contato_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                nome, ddd, telefone, ramal, ddd_cel, celular, depto, email = result
                
                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, nome or "")
                
                self.entry_ddd.delete(0, tk.END)
                self.entry_ddd.insert(0, ddd or "")
                
                self.entry_telefone.delete(0, tk.END)
                self.entry_telefone.insert(0, telefone or "")
                
                self.entry_ramal.delete(0, tk.END)
                self.entry_ramal.insert(0, ramal or "")
                
                self.entry_ddd_cel.delete(0, tk.END)
                self.entry_ddd_cel.insert(0, ddd_cel or "")
                
                self.entry_celular.delete(0, tk.END)
                self.entry_celular.insert(0, celular or "")
                
                self.entry_depto.delete(0, tk.END)
                self.entry_depto.insert(0, depto or "")
                
                self.entry_email.delete(0, tk.END)
                self.entry_email.insert(0, email or "")
                
                self.show_message(f"Contato selecionado: {nome_selecionado}", "info")
                
        except sqlite3.Error as e:
            self.show_message(f"ERRO ao carregar dados do contato: {str(e)}", "error")

    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.entry_nome.delete(0, tk.END)
        self.entry_ddd.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_ramal.delete(0, tk.END)
        self.entry_ddd_cel.delete(0, tk.END)
        self.entry_celular.delete(0, tk.END)
        self.entry_depto.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

