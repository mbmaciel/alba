import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class CepWindow(ttkb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.title("Consulta de CEPs")
        self.geometry("800x500")
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

        # Botões de navegação
        nav_container = ttkb.Frame(button_container)
        nav_container.pack(side=tk.LEFT, padx=(10, 0))

        ttkb.Button(nav_container, text="⏮", command=self.ir_primeiro, width=3).pack(side=tk.LEFT)
        ttkb.Button(nav_container, text="◀", command=self.ir_anterior, width=3).pack(side=tk.LEFT)
        ttkb.Button(nav_container, text="▶", command=self.ir_proximo, width=3).pack(side=tk.LEFT)
        ttkb.Button(nav_container, text="⏭", command=self.ir_ultimo, width=3).pack(side=tk.LEFT)

        # Separador visual
        separator = ttkb.Separator(toolbar_frame, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

        # Botão de busca
        search_container = ttkb.Frame(toolbar_frame)
        search_container.pack(side=tk.LEFT, padx=(10, 0))

        ttkb.Button(search_container, text="🔍", command=self.buscar_cep, width=3).pack(side=tk.LEFT)
        ttkb.Button(search_container, text="🔄", command=self.carregar, width=3).pack(side=tk.LEFT)

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

        # Frame para campos de entrada (somente leitura)
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        # Primeira linha
        ttkb.Label(input_frame, text="CEP").grid(row=0, column=0, sticky=tk.W)
        self.entry_cep = ttkb.Entry(input_frame, width=12, state="readonly")
        self.entry_cep.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Cidade").grid(row=0, column=2, sticky=tk.W)
        self.entry_cidade = ttkb.Entry(input_frame, width=30, state="readonly")
        self.entry_cidade.grid(row=0, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="UF").grid(row=0, column=4, sticky=tk.W)
        self.entry_uf = ttkb.Entry(input_frame, width=5, state="readonly")
        self.entry_uf.grid(row=0, column=5, pady=5, padx=5)

        # Segunda linha
        ttkb.Label(input_frame, text="Bairro").grid(row=1, column=0, sticky=tk.W)
        self.entry_bairro = ttkb.Entry(input_frame, width=30, state="readonly")
        self.entry_bairro.grid(row=1, column=1, columnspan=2, pady=5, padx=(5, 20), sticky=tk.W)

        ttkb.Label(input_frame, text="Logradouro").grid(row=1, column=3, sticky=tk.W)
        self.entry_endereco = ttkb.Entry(input_frame, width=40, state="readonly")
        self.entry_endereco.grid(row=1, column=4, columnspan=2, pady=5, padx=(5, 0), sticky=tk.W+tk.E)

        # Frame para busca
        search_frame = ttkb.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 15))

        ttkb.Label(search_frame, text="Buscar por CEP, Cidade, Bairro ou Logradouro").grid(row=0, column=0, sticky=tk.W)
        self.entry_busca = ttkb.Entry(search_frame, width=30)
        self.entry_busca.grid(row=0, column=1, pady=5, padx=(5, 10))
        self.entry_busca.bind("<Return>", lambda e: self.buscar_cep())

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("cep", "cidade", "uf", "bairro", "endereco"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("cep", text="CEP")
        self.tree.heading("cidade", text="Cidade")
        self.tree.heading("uf", text="UF")
        self.tree.heading("bairro", text="Bairro")
        self.tree.heading("endereco", text="Logradouro")
        
        self.tree.column("cep", width=80, minwidth=70, anchor=tk.CENTER)
        self.tree.column("cidade", width=150, minwidth=120, anchor=tk.W)
        self.tree.column("uf", width=50, minwidth=40, anchor=tk.CENTER)
        self.tree.column("bairro", width=150, minwidth=120, anchor=tk.W)
        self.tree.column("endereco", width=300, minwidth=200, anchor=tk.W)
        
        # Scrollbar para o Treeview
        scrollbar = ttkb.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def show_message(self, message, msg_type="info"):
        """Exibe mensagem na área de mensagens"""
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
        
        # Auto-limpar mensagem após 5 segundos
        self.after(5000, lambda: self.message_label.config(text="Sistema pronto para uso", foreground="blue"))

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def buscar_cep(self):
        cep_valor = self.entry_busca.get()
        if not cep_valor:
            self.carregar()
            self.show_message("Busca limpa. Mostrando primeiros 100 registros.", "info")
            return
        
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cd_cep, nm_cidade, cd_uf, nm_bairro, nm_lograd 
                FROM cep 
                WHERE cd_cep LIKE ? OR nm_cidade LIKE ? OR nm_bairro LIKE ? OR nm_lograd LIKE ?
                ORDER BY cd_cep
                LIMIT 100
            """, (f"%{cep_valor}%", f"%{cep_valor}%", f"%{cep_valor}%", f"%{cep_valor}%"))
            resultados = cursor.fetchall()
            conn.close()

            self.tree.delete(*self.tree.get_children())
            for row in resultados:
                self.tree.insert("", "end", values=row)
            
            if len(resultados) == 100:
                self.show_message(f"Mostrando primeiros 100 resultados para '{cep_valor}'. Refine a busca.", "warning")
            elif resultados:
                self.show_message(f"Encontrados {len(resultados)} resultados para '{cep_valor}'.", "success")
            else:
                self.show_message(f"Nenhum resultado encontrado para '{cep_valor}'.", "warning")
                
        except sqlite3.Error as e:
            self.show_message(f"ERRO ao buscar CEPs: {str(e)}", "error")

    def carregar(self):
        try:
            self.tree.delete(*self.tree.get_children())
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT cd_cep, nm_cidade, cd_uf, nm_bairro, nm_lograd FROM cep ORDER BY cd_cep LIMIT 100")
            rows = cursor.fetchall()
            conn.close()
            
            for row in rows:
                self.tree.insert("", "end", values=row)
            
            self.show_message(f"Carregados {len(rows)} CEPs (primeiros 100 registros)", "success")
            
        except sqlite3.Error as e:
            self.show_message(f"ERRO ao carregar CEPs: {str(e)}", "error")

    def on_select(self, event):
        item = self.tree.item(self.tree.focus())
        if not item:
            return
            
        try:
            cep, cidade, uf, bairro, endereco = item["values"]
            
            # Habilitar temporariamente os campos para inserir dados
            self.entry_cep.config(state="normal")
            self.entry_cidade.config(state="normal")
            self.entry_uf.config(state="normal")
            self.entry_bairro.config(state="normal")
            self.entry_endereco.config(state="normal")
            
            self.entry_cep.delete(0, tk.END)
            self.entry_cep.insert(0, cep or "")
            
            self.entry_cidade.delete(0, tk.END)
            self.entry_cidade.insert(0, cidade or "")
            
            self.entry_uf.delete(0, tk.END)
            self.entry_uf.insert(0, uf or "")
            
            self.entry_bairro.delete(0, tk.END)
            self.entry_bairro.insert(0, bairro or "")
            
            self.entry_endereco.delete(0, tk.END)
            self.entry_endereco.insert(0, endereco or "")
            
            # Voltar para readonly
            self.entry_cep.config(state="readonly")
            self.entry_cidade.config(state="readonly")
            self.entry_uf.config(state="readonly")
            self.entry_bairro.config(state="readonly")
            self.entry_endereco.config(state="readonly")
            
            self.show_message(f"CEP selecionado: {cep} - {cidade}/{uf}", "info")
            
        except Exception as e:
            self.show_message(f"ERRO ao selecionar CEP: {str(e)}", "error")

    def limpar(self):
        # Habilitar temporariamente os campos para limpar
        self.entry_cep.config(state="normal")
        self.entry_cidade.config(state="normal")
        self.entry_uf.config(state="normal")
        self.entry_bairro.config(state="normal")
        self.entry_endereco.config(state="normal")
        
        self.entry_cep.delete(0, tk.END)
        self.entry_cidade.delete(0, tk.END)
        self.entry_uf.delete(0, tk.END)
        self.entry_bairro.delete(0, tk.END)
        self.entry_endereco.delete(0, tk.END)
        self.entry_busca.delete(0, tk.END)
        
        # Voltar para readonly
        self.entry_cep.config(state="readonly")
        self.entry_cidade.config(state="readonly")
        self.entry_uf.config(state="readonly")
        self.entry_bairro.config(state="readonly")
        self.entry_endereco.config(state="readonly")
        
    def ir_primeiro(self):
        """Navega para o primeiro registro na lista"""
        items = self.tree.get_children()
        if items:
            primeiro_item = items[0]
            self.tree.selection_set(primeiro_item)
            self.tree.focus(primeiro_item)
            self.tree.see(primeiro_item)
            self.on_select(None)
            self.show_message("Navegado para o primeiro CEP", "info")
        else:
            self.show_message("Nenhum CEP disponível", "warning")
        
    def ir_ultimo(self):
        """Navega para o último registro na lista"""
        items = self.tree.get_children()
        if items:
            ultimo_item = items[-1]
            self.tree.selection_set(ultimo_item)
            self.tree.focus(ultimo_item)
            self.tree.see(ultimo_item)
            self.on_select(None)
            self.show_message("Navegado para o último CEP", "info")
        else:
            self.show_message("Nenhum CEP disponível", "warning")
        
    def ir_anterior(self):
        """Navega para o registro anterior na lista"""
        selecionado = self.tree.selection()
        if not selecionado:
            self.ir_primeiro()
            return
        
        items = self.tree.get_children()
        idx = items.index(selecionado[0])
        
        if idx > 0:
            anterior = items[idx - 1]
            self.tree.selection_set(anterior)
            self.tree.focus(anterior)
            self.tree.see(anterior)
            self.on_select(None)
            self.show_message("Navegado para o CEP anterior", "info")
        else:
            self.show_message("Já está no primeiro CEP", "warning")
        
    def ir_proximo(self):
        """Navega para o próximo registro na lista"""
        selecionado = self.tree.selection()
        if not selecionado:
            self.ir_primeiro()
            return
        
        items = self.tree.get_children()
        idx = items.index(selecionado[0])
        
        if idx < len(items) - 1:
            proximo = items[idx + 1]
            self.tree.selection_set(proximo)
            self.tree.focus(proximo)
            self.tree.see(proximo)
            self.on_select(None)
            self.show_message("Navegado para o próximo CEP", "info")
        else:
            self.show_message("Já está no último CEP", "warning")