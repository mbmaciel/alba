import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class SystemConfigWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Configurações do Sistema")
        self.geometry("850x550")
        self.resizable(False, False)

        self.campos = {}
        
        # Main container
        main_frame = ttkb.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
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
        
        # Save Button at the bottom
        button_frame = ttkb.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttkb.Button(button_frame, text="Salvar", command=self.salvar, bootstyle=SUCCESS).pack(side=tk.RIGHT)

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

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def carregar(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM system LIMIT 1")
        row = cursor.fetchone()
        if row:
            colnames = [desc[0] for desc in cursor.description]
            for i, campo in enumerate(colnames):
                if campo in self.campos:
                    self.campos[campo].delete(0, tk.END)
                    self.campos[campo].insert(0, row[i])
        conn.close()

    def salvar(self):
        valores = {campo: self.campos[campo].get() for campo in self.campos}
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM system")
        cursor.execute(f"""
            INSERT INTO system ({', '.join(valores.keys())})
            VALUES ({', '.join(['?' for _ in valores])})
        """, tuple(valores.values()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Configurações salvas com sucesso.")
