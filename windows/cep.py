import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class CepWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilo(self)
        self.set_title("Consulta de CEPs")
        self.config(width=800, height=500)

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

        # Botão de busca
        search_container = ttkb.Frame(toolbar_frame)
        search_container.pack(side=tk.LEFT, padx=(10, 0))

        btn_buscar = ttkb.Button(search_container, text="🔍", command=self.buscar_cep, width=3)
        btn_buscar.pack(side=tk.LEFT)
        self.create_tooltip(btn_buscar, "Buscar CEP")
        
        btn_recarregar = ttkb.Button(search_container, text="🔄", command=self.carregar, width=3)
        btn_recarregar.pack(side=tk.LEFT)
        self.create_tooltip(btn_recarregar, "Recarregar Lista")

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
        ttkb.Label(input_frame, text="CEP").grid(row=0, column=0, sticky=tk.W)
        vcmd = (self.register(self.validate_cep), '%P')
        self.entry_cep = ttkb.Entry(input_frame, width=12, validate='key', validatecommand=vcmd)
        self.entry_cep.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Cidade").grid(row=0, column=2, sticky=tk.W)
        self.entry_cidade = ttkb.Entry(input_frame, width=30)
        self.entry_cidade.grid(row=0, column=3, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="UF").grid(row=0, column=4, sticky=tk.W)
        self.entry_uf = ttkb.Entry(input_frame, width=5)
        self.entry_uf.grid(row=0, column=5, pady=5, padx=5)

        # Segunda linha
        ttkb.Label(input_frame, text="Bairro").grid(row=1, column=0, sticky=tk.W)
        self.entry_bairro = ttkb.Entry(input_frame, width=30)
        self.entry_bairro.grid(row=1, column=1, columnspan=2, pady=5, padx=(5, 20), sticky=tk.W)

        ttkb.Label(input_frame, text="Logradouro").grid(row=1, column=3, sticky=tk.W)
        self.entry_endereco = ttkb.Entry(input_frame, width=40)
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
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar()

    def validate_cep(self, value):
        """Valida se o CEP contém apenas números"""
        return value.isdigit() or value == ""

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            tooltip.configure(bg="lightyellow", relief="solid", borderwidth=1)
            
            label = tk.Label(tooltip, text=text, bg="lightyellow", 
                           font=("Arial", 8), padx=5, pady=2)
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

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

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        # Habilitar campos para edição
        self.entry_cep.config(state="normal")
        self.entry_cidade.config(state="normal")
        self.entry_uf.config(state="normal")
        self.entry_bairro.config(state="normal")
        self.entry_endereco.config(state="normal")
        
        # Limpar campos
        self.entry_cep.delete(0, tk.END)
        self.entry_cidade.delete(0, tk.END)
        self.entry_uf.delete(0, tk.END)
        self.entry_bairro.delete(0, tk.END)
        self.entry_endereco.delete(0, tk.END)
        
        self.entry_cep.focus()
        self.show_message("Novo registro. Preencha os campos e clique em Salvar.", "info")

    def _execute_save(self):
        cep = self.entry_cep.get().strip()
        cidade = self.entry_cidade.get().strip()
        uf = self.entry_uf.get().strip()
        bairro = self.entry_bairro.get().strip()
        endereco = self.entry_endereco.get().strip()

        try:
            conn = self.conectar()
            cursor = conn.cursor()
            
            # Verificar se o registro já existe
            cursor.execute("SELECT cd_cep FROM cep WHERE cd_cep = ?", (cep,))
            registro_existente = cursor.fetchone()

            is_update = registro_existente is not None

            if is_update:
                # Atualizar registro existente
                cursor.execute("""UPDATE cep 
                                SET nm_cidade = ?, cd_uf = ?, nm_bairro = ?, nm_lograd = ? 
                                WHERE cd_cep = ?""",
                               (cidade, uf, bairro, endereco, cep))
                self.show_message("CEP atualizado com sucesso!", "success")
            else:
                # Obter o próximo recnum
                cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM cep")
                proximo_recnum = cursor.fetchone()[0]

                # Inserir novo registro
                cursor.execute("""INSERT INTO cep (recnum, cd_cep, nm_cidade, cd_uf, nm_bairro, nm_lograd) 
                                VALUES (?, ?, ?, ?, ?, ?)""",
                               (proximo_recnum, cep, cidade, uf, bairro, endereco))
                self.show_message("CEP salvo com sucesso!", "success")

            conn.commit()
            conn.close()

            # Recarregar a lista
            self.carregar()

            # Se foi uma inserção, limpar os campos
            if not is_update:
                self.limpar()
            else:
                # Reselecionar o item atualizado na lista
                self.selecionar_item_por_cep(cep)

        except Exception as e:
            self.show_message(f"Erro ao salvar: {str(e)}", "error")

    def salvar(self):
        cep = self.entry_cep.get().strip()
        cidade = self.entry_cidade.get().strip()
        uf = self.entry_uf.get().strip()

        if not cep or not cidade or not uf:
            self.show_message("CEP, cidade e UF são obrigatórios.", "warning")
            return

        confirmation_message = f"Confirma a gravação do CEP '{cep}'?"
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('save')

        if not self.request_confirmation('save', confirmation_message, self._execute_save):
            return

    def selecionar_item_por_cep(self, cep):
        """Seleciona um item na lista pelo CEP"""
        for item in self.tree.get_children():
            valores = self.tree.item(item)["values"]
            if valores and str(valores[0]) == str(cep):
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)
                break

    def _execute_removal(self, cep):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cep WHERE cd_cep = ?", (cep,))
            conn.commit()
            conn.close()
            self.show_message("CEP removido com sucesso!", "success")

            self.carregar()
            self.limpar()

        except Exception as e:
            self.show_message(f"Erro ao remover: {str(e)}", "error")

    def remover(self):
        item = self.tree.focus()
        if not item:
            self.show_message("Selecione um CEP para remover.", "warning")
            return
            
        cep = self.tree.item(item)["values"][0]
        confirmation_message = f"Pressione 'Remover' novamente para excluir o CEP '{cep}'."
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('remove')

        if not self.request_confirmation('remove', confirmation_message, self._execute_removal, cep):
            return
