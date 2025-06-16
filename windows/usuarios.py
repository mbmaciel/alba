import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class UsuarioWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Cadastro de Usuários")
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

        # Botões de navegação
        nav_container = ttkb.Frame(toolbar_frame)
        nav_container.pack(side=tk.LEFT, padx=(10, 0))

        ttkb.Button(nav_container, text="⏮", command=self.ir_primeiro, width=3).pack(side=tk.LEFT)
        ttkb.Button(nav_container, text="◀", command=self.ir_anterior, width=3).pack(side=tk.LEFT)
        ttkb.Button(nav_container, text="▶", command=self.ir_proximo, width=3).pack(side=tk.LEFT)
        ttkb.Button(nav_container, text="⏭", command=self.ir_ultimo, width=3).pack(side=tk.LEFT)

        # Frame para campos de entrada
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        # Primeira linha
        ttkb.Label(input_frame, text="Nome do Usuário").grid(row=0, column=0, sticky=tk.W)
        self.entry_nome = ttkb.Entry(input_frame, width=50)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=(5, 20))

        # Segunda linha - Campos adicionais para usuários
        ttkb.Label(input_frame, text="Login").grid(row=1, column=0, sticky=tk.W)
        self.entry_login = ttkb.Entry(input_frame, width=30)
        self.entry_login.grid(row=1, column=1, pady=5, padx=(5, 20), sticky=tk.W)

        # Terceira linha
        ttkb.Label(input_frame, text="Email").grid(row=2, column=0, sticky=tk.W)
        self.entry_email = ttkb.Entry(input_frame, width=50)
        self.entry_email.grid(row=2, column=1, pady=5, padx=(5, 20))

        # Quarta linha
        ttkb.Label(input_frame, text="Perfil").grid(row=3, column=0, sticky=tk.W)
        self.combo_perfil = ttkb.Combobox(input_frame, width=25, state="readonly")
        self.combo_perfil["values"] = ["Administrador", "Usuário", "Vendedor", "Operador", "Consulta"]
        self.combo_perfil.grid(row=3, column=1, pady=5, padx=(5, 20), sticky=tk.W)

        # Quinta linha
        ttkb.Label(input_frame, text="Status").grid(row=4, column=0, sticky=tk.W)
        self.combo_status = ttkb.Combobox(input_frame, width=15, state="readonly")
        self.combo_status["values"] = ["Ativo", "Inativo", "Bloqueado"]
        self.combo_status.grid(row=4, column=1, pady=5, padx=(5, 20), sticky=tk.W)
        self.combo_status.set("Ativo")  # Valor padrão

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "nome", "login", "email", "perfil", "status"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("login", text="Login")
        self.tree.heading("email", text="Email")
        self.tree.heading("perfil", text="Perfil")
        self.tree.heading("status", text="Status")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("nome", width=200, minwidth=150, anchor=tk.W)
        self.tree.column("login", width=120, minwidth=100, anchor=tk.W)
        self.tree.column("email", width=180, minwidth=150, anchor=tk.W)
        self.tree.column("perfil", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column("status", width=80, minwidth=60, anchor=tk.CENTER)
        
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
        self.entry_nome.focus()

    def salvar(self):
        nome = self.entry_nome.get().strip()
        login = self.entry_login.get().strip()
        email = self.entry_email.get().strip()
        perfil = self.combo_perfil.get()
        status = self.combo_status.get()

        if not nome:
            messagebox.showwarning("Campos obrigatórios", "Nome do usuário é obrigatório.")
            return

        if not login:
            messagebox.showwarning("Campos obrigatórios", "Login é obrigatório.")
            return

        # Validação básica de email
        if email and "@" not in email:
            messagebox.showwarning("Email inválido", "Digite um email válido.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        
        try:
            # Verificar se o login já existe
            cursor.execute("SELECT COUNT(*) FROM usuario WHERE nm_login = ? AND nm_nome != ?", (login, nome))
            if cursor.fetchone()[0] > 0:
                messagebox.showwarning("Login duplicado", "Este login já está sendo usado por outro usuário.")
                return

            # Verificar se é atualização ou inserção
            cursor.execute("SELECT id_usuario FROM usuario WHERE nm_nome = ?", (nome,))
            usuario_existente = cursor.fetchone()

            if usuario_existente:
                # Atualizar usuário existente
                cursor.execute("""
                    UPDATE usuario SET 
                        nm_login = ?, nm_email = ?, nm_perfil = ?, fl_status = ?
                    WHERE id_usuario = ?
                """, (login, email, perfil, status, usuario_existente[0]))
                messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
            else:
                # Inserir novo usuário
                cursor.execute("""
                    INSERT INTO usuario (nm_nome, nm_login, nm_email, nm_perfil, fl_status) 
                    VALUES (?, ?, ?, ?, ?)
                """, (nome, login, email, perfil, status))
                messagebox.showinfo("Sucesso", "Usuário salvo com sucesso!")

            conn.commit()
            self.limpar()
            self.carregar()
            
        except Exception as e:
            messagebox.showerror("Erro ao salvar", f"Erro: {str(e)}")
        finally:
            conn.close()

    def remover(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um usuário para remover.")
            return
            
        values = self.tree.item(item)["values"]
        id_usuario = values[0]
        nome_usuario = values[1]
        
        resposta = messagebox.askyesno("Confirmar", f"Deseja realmente remover o usuário '{nome_usuario}'?")
        if not resposta:
            return

        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário removido com sucesso!")
            self.carregar()
            self.limpar()
        except Exception as e:
            messagebox.showerror("Erro ao remover", f"Erro: {str(e)}")
        finally:
            conn.close()

    def carregar(self):
        # Limpar treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        conn = self.conectar()
        cursor = conn.cursor()
        
        try:
            # Verificar se as colunas existem, se não, criá-las
            cursor.execute("PRAGMA table_info(usuario)")
            colunas = [col[1] for col in cursor.fetchall()]
            
            if 'nm_login' not in colunas:
                cursor.execute("ALTER TABLE usuario ADD COLUMN nm_login TEXT")
            if 'nm_email' not in colunas:
                cursor.execute("ALTER TABLE usuario ADD COLUMN nm_email TEXT")
            if 'nm_perfil' not in colunas:
                cursor.execute("ALTER TABLE usuario ADD COLUMN nm_perfil TEXT DEFAULT 'Usuário'")
            if 'fl_status' not in colunas:
                cursor.execute("ALTER TABLE usuario ADD COLUMN fl_status TEXT DEFAULT 'Ativo'")
            
            conn.commit()
            
            # Carregar dados
            cursor.execute("""
                SELECT id_usuario, nm_nome, 
                       COALESCE(nm_login, '') as nm_login,
                       COALESCE(nm_email, '') as nm_email,
                       COALESCE(nm_perfil, 'Usuário') as nm_perfil,
                       COALESCE(fl_status, 'Ativo') as fl_status
                FROM usuario 
                ORDER BY nm_nome
            """)
            
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
                
        except Exception as e:
            messagebox.showerror("Erro ao carregar", f"Erro: {str(e)}")
        finally:
            conn.close()

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
            
        values = item["values"]
        if len(values) >= 6:
            id_usuario, nome, login, email, perfil, status = values
            
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, nome or "")
            
            self.entry_login.delete(0, tk.END)
            self.entry_login.insert(0, login or "")
            
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, email or "")
            
            self.combo_perfil.set(perfil or "Usuário")
            self.combo_status.set(status or "Ativo")

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.entry_nome.delete(0, tk.END)
        self.entry_login.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.combo_perfil.set("")
        self.combo_status.set("Ativo")
        
