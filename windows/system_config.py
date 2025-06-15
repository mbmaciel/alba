import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class SystemConfigWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Configurações do Sistema")
        self.geometry("900x700")
        self.resizable(False, False)

        self.campos = {}
        
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

        # Create notebook with tabs for different categories
        notebook = ttkb.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Company Information Tab
        company_frame = ttkb.Frame(notebook, padding=10)
        notebook.add(company_frame, text="Informações da Empresa")
        
        # Contact Information Tab
        contact_frame = ttkb.Frame(notebook, padding=10)
        notebook.add(contact_frame, text="Contato")
        
        # System Paths Tab
        paths_frame = ttkb.Frame(notebook, padding=10)
        notebook.add(paths_frame, text="Caminhos do Sistema")
        
        # Other Settings Tab
        other_frame = ttkb.Frame(notebook, padding=10)
        notebook.add(other_frame, text="Outras Configurações")
        
        # Company Information Fields
        company_fields = [
            ("Razão Social", "nm_razao"),
            ("CNPJ", "nr_cnpj"),
            ("Inscrição Estadual", "nr_ie"),
            ("Inscrição Municipal", "nr_im")
        ]
        
        # Address Fields
        address_fields = [
            ("CEP", "cd_cep"),
            ("Número", "nr_numero"),
            ("Complemento", "nm_compl")
        ]
        
        # Contact Fields
        contact_fields = [
            ("DDD", "nr_ddd"),
            ("Telefone", "nr_fone")
        ]
        
        # System Paths Fields
        path_fields = [
            ("Caminho XML", "nm_path_xml"),
            ("Caminho Temp", "nm_path_temp"),
            ("Certificado", "nm_certificado")
        ]
        
        # Other Settings Fields
        other_fields = [
            ("Manutenção (S/N)", "fl_manutencao"),
            ("Buscar CEP", "cd_buscarcep"),
            ("Vendedor", "nm_vendedor")
        ]
        
        # Create Company Information section
        self._create_section(company_frame, "Dados da Empresa", company_fields, 0)
        self._create_section(company_frame, "Endereço", address_fields, len(company_fields) + 1)
        
        # Create Contact Information section
        self._create_section(contact_frame, "Informações de Contato", contact_fields, 0)
        
        # Create System Paths section
        self._create_section(paths_frame, "Caminhos do Sistema", path_fields, 0)
        
        # Create Other Settings section
        self._create_section(other_frame, "Outras Configurações", other_fields, 0)

        # Frame para o Treeview (área expandida) - Mostra histórico de configurações
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))

        # Label para o histórico
        ttkb.Label(tree_frame, text="Histórico de Configurações", font=("MS Sans Serif", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "razao", "cnpj", "telefone", "data_config"), show="headings", height=8)
        
        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("razao", text="Razão Social")
        self.tree.heading("cnpj", text="CNPJ")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("data_config", text="Data Configuração")
        
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("razao", width=250, minwidth=200, anchor=tk.W)
        self.tree.column("cnpj", width=150, minwidth=120, anchor=tk.CENTER)
        self.tree.column("telefone", width=120, minwidth=100, anchor=tk.CENTER)
        self.tree.column("data_config", width=150, minwidth=120, anchor=tk.CENTER)
        
        # Scrollbar para o Treeview
        scrollbar_tree = ttkb.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_tree.set)
        
        # Pack do Treeview e Scrollbar
        tree_container = ttkb.Frame(tree_frame)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, in_=tree_container)
        scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y, in_=tree_container)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def _create_section(self, parent, title, fields, start_row):
        """Helper method to create a section with a title and fields"""
        # Section title
        if title:
            section_label = ttkb.Label(parent, text=title, font=("MS Sans Serif", 12, "bold"))
            section_label.grid(row=start_row, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
            start_row += 1
        
        # Create fields
        for i, (label, campo) in enumerate(fields):
            row = start_row + i
            ttkb.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, padx=(5, 10), pady=3)
            entry = ttkb.Entry(parent, width=50)
            entry.grid(row=row, column=1, pady=3, padx=5, sticky=tk.W)
            self.campos[campo] = entry
        
        return start_row + len(fields)

    def novo(self):
        """Limpa os campos para nova configuração"""
        self.limpar()
        # Focar no primeiro campo da primeira aba
        if "nm_razao" in self.campos:
            self.campos["nm_razao"].focus()

    def carregar(self):
        # Carregar dados atuais
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM system LIMIT 1")
        row = cursor.fetchone()
        if row:
            colnames = [desc[0] for desc in cursor.description]
            for i, campo in enumerate(colnames):
                if campo in self.campos:
                    self.campos[campo].delete(0, tk.END)
                    self.campos[campo].insert(0, str(row[i]) if row[i] is not None else "")
        
        # Carregar histórico no treeview
        self.carregar_historico()
        conn.close()

    def carregar_historico(self):
        """Carrega o histórico de configurações no treeview"""
        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        cursor = conn.cursor()
        
        # Adicionar coluna de timestamp se não existir
        try:
            cursor.execute("ALTER TABLE system ADD COLUMN data_config DATETIME DEFAULT CURRENT_TIMESTAMP")
            conn.commit()
        except:
            pass  # Coluna já existe
        
        cursor.execute("""
            SELECT rowid, nm_razao, nr_cnpj, nr_fone, 
                   COALESCE(data_config, 'Não informado') as data_config 
            FROM system 
            ORDER BY rowid DESC
        """)
        
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def salvar(self):
        valores = {campo: self.campos[campo].get() for campo in self.campos}
        
        # Validação básica
        if not valores.get("nm_razao", "").strip():
            messagebox.showwarning("Atenção", "Razão Social é obrigatória.")
            return
        
        conn = self.conectar()
        cursor = conn.cursor()
        
        try:
            # Adicionar timestamp
            valores["data_config"] = "datetime('now', 'localtime')"
            
            cursor.execute("DELETE FROM system")
            
            # Construir query com timestamp
            campos = list(valores.keys())
            valores_query = []
            for campo in campos:
                if campo == "data_config":
                    valores_query.append("datetime('now', 'localtime')")
                else:
                    valores_query.append("?")
            
            query = f"INSERT INTO system ({', '.join(campos)}) VALUES ({', '.join(valores_query)})"
            valores_sem_timestamp = [v for k, v in valores.items() if k != "data_config"]
            
            cursor.execute(query, valores_sem_timestamp)
            conn.commit()
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            self.carregar_historico()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")
        finally:
            conn.close()

    def remover(self):
        """Remove a configuração atual"""
        resposta = messagebox.askyesno("Confirmar", "Deseja realmente limpar todas as configurações?")
        if not resposta:
            return
            
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM system")
            conn.commit()
            messagebox.showinfo("Sucesso", "Configurações removidas com sucesso!")
            self.limpar()
            self.carregar_historico()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover configurações: {str(e)}")
        finally:
            conn.close()

    def on_select(self, event):
        """Carrega configuração selecionada no histórico"""
        item = self.tree.item(self.tree.focus())
        if not item:
            return
        
        rowid = item["values"][0]
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM system WHERE rowid = ?", (rowid,))
        row = cursor.fetchone()
        
        if row:
            colnames = [desc[0] for desc in cursor.description]
            for i, campo in enumerate(colnames):
                if campo in self.campos:
                    self.campos[campo].delete(0, tk.END)
                    self.campos[campo].insert(0, str(row[i]) if row[i] is not None else "")
        conn.close()

    def limpar(self):
        """Limpa todos os campos"""
        for campo in self.campos:
            self.campos[campo].delete(0, tk.END)
        
