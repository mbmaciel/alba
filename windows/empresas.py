import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class EmpresaWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_id = None  # Add this line at the beginning of __init__
        aplicar_estilo(self)
        self.set_title("Cadastro de Empresas")
        self.config(width=900, height=700)

        # Frame principal
        main_frame = ttkb.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para toolbar e mensagens
        top_frame = ttkb.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 15))

        # Barra de ferramentas no topo
        toolbar_frame = ttkb.Frame(top_frame, relief="raised", borderwidth=2, padding=5)
        toolbar_frame.pack(side=tk.LEFT, fill=tk.X)

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

        # Notebook para as abas
        self.notebook = ttkb.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Aba Dados Básicos
        self.frame_basico = ttkb.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_basico, text='Dados Básicos')

        ttkb.Label(self.frame_basico, text="Razão Social").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_razao = ttkb.Entry(self.frame_basico, width=60)
        self.entry_razao.grid(row=0, column=1, columnspan=3, pady=5, padx=(5, 0), sticky=tk.W+tk.E)

        ttkb.Label(self.frame_basico, text="Nome Fantasia").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_fantasia = ttkb.Entry(self.frame_basico, width=60)
        self.entry_fantasia.grid(row=1, column=1, columnspan=3, pady=5, padx=(5, 0), sticky=tk.W+tk.E)

        ttkb.Label(self.frame_basico, text="CNPJ").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_cnpj = ttkb.Entry(self.frame_basico, width=25)
        self.entry_cnpj.grid(row=2, column=1, pady=5, padx=(5, 20))

        ttkb.Label(self.frame_basico, text="Inscrição Estadual").grid(row=2, column=2, sticky=tk.W, pady=5)
        self.entry_ie = ttkb.Entry(self.frame_basico, width=25)
        self.entry_ie.grid(row=2, column=3, pady=5, padx=(5, 0))

        ttkb.Label(self.frame_basico, text="Inscrição Municipal").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_im = ttkb.Entry(self.frame_basico, width=25)
        self.entry_im.grid(row=3, column=1, pady=5, padx=(5, 0))

        # Configurar expansão das colunas
        self.frame_basico.grid_columnconfigure(1, weight=1)
        self.frame_basico.grid_columnconfigure(3, weight=1)

        # Aba Endereço
        self.frame_endereco = ttkb.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_endereco, text='Endereço')

        ttkb.Label(self.frame_endereco, text="CEP").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_cep = ttkb.Entry(self.frame_endereco, width=15)
        self.entry_cep.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(self.frame_endereco, text="Número").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.entry_numero = ttkb.Entry(self.frame_endereco, width=10)
        self.entry_numero.grid(row=0, column=3, pady=5, padx=(5, 0))

        ttkb.Label(self.frame_endereco, text="Complemento").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_complemento = ttkb.Entry(self.frame_endereco, width=50)
        self.entry_complemento.grid(row=1, column=1, columnspan=3, pady=5, padx=(5, 0), sticky=tk.W+tk.E)

        # Configurar expansão das colunas
        self.frame_endereco.grid_columnconfigure(1, weight=1)

        # Aba JUCESP
        self.frame_jucesp = ttkb.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_jucesp, text='JUCESP')

        ttkb.Label(self.frame_jucesp, text="Nº JUCESP Cadastro").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_jucesp_cad = ttkb.Entry(self.frame_jucesp, width=25)
        self.entry_jucesp_cad.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(self.frame_jucesp, text="Data Cadastro").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.entry_dt_cad = ttkb.Entry(self.frame_jucesp, width=20)
        self.entry_dt_cad.grid(row=0, column=3, pady=5, padx=(5, 0))

        ttkb.Label(self.frame_jucesp, text="Nº JUCESP Alteração").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_jucesp_alt = ttkb.Entry(self.frame_jucesp, width=25)
        self.entry_jucesp_alt.grid(row=1, column=1, pady=5, padx=(5, 20))

        ttkb.Label(self.frame_jucesp, text="Data Alteração").grid(row=1, column=2, sticky=tk.W, pady=5)
        self.entry_dt_alt = ttkb.Entry(self.frame_jucesp, width=20)
        self.entry_dt_alt.grid(row=1, column=3, pady=5, padx=(5, 0))

        # Aba Numeração
        self.frame_numeracao = ttkb.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_numeracao, text='Numeração')

        ttkb.Label(self.frame_numeracao, text="COD Última OC").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_ult_oc = ttkb.Entry(self.frame_numeracao, width=20)
        self.entry_ult_oc.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(self.frame_numeracao, text="COD Última OF").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.entry_ult_of = ttkb.Entry(self.frame_numeracao, width=20)
        self.entry_ult_of.grid(row=0, column=3, pady=5, padx=(5, 0))

        ttkb.Label(self.frame_numeracao, text="COD Última NFS").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_ult_nfsa = ttkb.Entry(self.frame_numeracao, width=20)
        self.entry_ult_nfsa.grid(row=1, column=1, pady=5, padx=(5, 20))

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "razao", "fantasia", "cnpj"), show="headings", height=12)
            
        # Configuração das colunas
        self.tree.heading("id", text="COD")
        self.tree.heading("razao", text="Razão Social")
        self.tree.heading("fantasia", text="Nome Fantasia")
        self.tree.heading("cnpj", text="CNPJ")
            
        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("razao", width=300, minwidth=200, anchor=tk.W)
        self.tree.column("fantasia", width=250, minwidth=150, anchor=tk.W)
        self.tree.column("cnpj", width=150, minwidth=120, anchor=tk.CENTER)
            
        # Scrollbar para o Treeview
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
            
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_empresas()

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

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.limpar_campos()
        self.entry_razao.focus()

    def _execute_save(self):
        try:
            dados = (
                self.entry_razao.get(),
                self.entry_fantasia.get(),
                self.entry_cnpj.get(),
                self.entry_ie.get(),
                self.entry_im.get(),
                self.entry_cep.get(),
                self.entry_numero.get(),
                self.entry_complemento.get(),
                self.entry_jucesp_cad.get(),
                self.entry_dt_cad.get(),
                self.entry_jucesp_alt.get(),
                self.entry_dt_alt.get()
            )

            conn = self.conectar()
            cursor = conn.cursor()

            try:
                if self.current_id is None:
                    # Novo registro - INSERT com campos de numeração se existirem
                    cols = [r[1] for r in cursor.execute("PRAGMA table_info(empresas)").fetchall()]
                    extra_cols = []
                    extra_vals = []
                    if 'nr_ult_oc' in cols:
                        extra_cols.append('nr_ult_oc')
                        extra_vals.append(self.entry_ult_oc.get() or None)
                    if 'nr_ult_of' in cols:
                        extra_cols.append('nr_ult_of')
                        extra_vals.append(self.entry_ult_of.get() or None)
                    if 'nr_ult_nf_sa' in cols:
                        extra_cols.append('nr_ult_nf_sa')
                        extra_vals.append(self.entry_ult_nfsa.get() or None)

                    base_cols = [
                        'nm_razao','nm_fantasia','nr_cnpj','nr_ie','nr_im','cd_cep',
                        'nr_numero','nm_complemento','nr_jucesp_cad','dt_jucesp_cad',
                        'nr_jucesp_alt','dt_jucesp_alt'
                    ]
                    all_cols = base_cols + extra_cols + ['recnum']
                    placeholders = ', '.join(['?']*len(base_cols + extra_cols)) + ", (SELECT COALESCE(MAX(recnum), 0) + 1 FROM empresas)"
                    sql = f"INSERT INTO empresas ({', '.join(all_cols)}) VALUES ({placeholders})"
                    cursor.execute(sql, dados + tuple(extra_vals))
                    self.show_message("Empresa incluída com sucesso!", "success")
                else:
                    # Atualização - UPDATE com campos de numeração se existirem
                    cols = [r[1] for r in cursor.execute("PRAGMA table_info(empresas)").fetchall()]
                    sets = [
                        'nm_razao=?','nm_fantasia=?','nr_cnpj=?','nr_ie=?','nr_im=?','cd_cep=?',
                        'nr_numero=?','nm_complemento=?','nr_jucesp_cad=?','dt_jucesp_cad=?',
                        'nr_jucesp_alt=?','dt_jucesp_alt=?'
                    ]
                    params = list(dados)
                    if 'nr_ult_oc' in cols:
                        sets.append('nr_ult_oc=?')
                        params.append(self.entry_ult_oc.get() or None)
                    if 'nr_ult_of' in cols:
                        sets.append('nr_ult_of=?')
                        params.append(self.entry_ult_of.get() or None)
                    if 'nr_ult_nf_sa' in cols:
                        sets.append('nr_ult_nf_sa=?')
                        params.append(self.entry_ult_nfsa.get() or None)
                    sql = f"UPDATE empresas SET {', '.join(sets)} WHERE id_empresa=?"
                    params.append(self.current_id)
                    cursor.execute(sql, tuple(params))
                    self.show_message("Empresa atualizada com sucesso!", "success")

                conn.commit()
                self.limpar_campos()
                self.carregar_empresas()
                self.current_id = None

            except sqlite3.Error as e:
                self.show_message(f"Erro ao salvar empresa: {str(e)}", "error")
                conn.rollback()
            finally:
                conn.close()

        except Exception as e:
            self.show_message(f"Erro inesperado: {str(e)}", "error")

    def salvar(self):
        razao = self.entry_razao.get()
        cnpj = self.entry_cnpj.get()

        if not razao or not cnpj:
            self.show_message("Preencha os campos obrigatórios: Razão Social e CNPJ.", "warning")
            return

        confirmation_message = f"Confirma a gravação da empresa '{razao}'?"
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('save')

        if not self.request_confirmation('save', confirmation_message, self._execute_save):
            return

    def _execute_removal(self, empresa_id, razao_social):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM empresas WHERE id_empresa = ?", (empresa_id,))
            conn.commit()
            conn.close()
            self.carregar_empresas()
            self.limpar_campos()
            self.show_message(f"Empresa '{razao_social}' removida com sucesso!", "success")
        except sqlite3.Error as e:
            self.show_message(f"Erro ao remover empresa: {str(e)}", "error")

    def remover(self):
        selecionado = self.tree.focus()
        if not selecionado:
            self.show_message("Selecione uma empresa para remover.", "warning")
            return

        item = self.tree.item(selecionado)
        empresa_id, razao_social = item["values"][:2]

        confirmation_message = f"Pressione 'Remover' novamente para excluir a empresa '{razao_social}'."

        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('remove')

        if not self.request_confirmation('remove', confirmation_message, self._execute_removal, empresa_id, razao_social):
            return

    def carregar_empresas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_empresa, nm_razao, nm_fantasia, nr_cnpj FROM empresas ORDER BY nm_razao")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, event):
        try:
            item = self.tree.item(self.tree.focus())
            if not item or not item.get("values"):
                return

            empresa_id = item["values"][0]
            self.current_id = empresa_id  # Store ID for editing
            
            conn = self.conectar()
            cursor = conn.cursor()
            cols = [r[1] for r in cursor.execute("PRAGMA table_info(empresas)").fetchall()]
            select_cols = [
                'nm_razao','nm_fantasia','nr_cnpj','nr_ie','nr_im','cd_cep','nr_numero',
                'nm_complemento','nr_jucesp_cad','dt_jucesp_cad','nr_jucesp_alt','dt_jucesp_alt'
            ]
            extra_present = []
            for c in ('nr_ult_oc','nr_ult_of','nr_ult_nf_sa'):
                if c in cols:
                    select_cols.append(c)
                    extra_present.append(c)
            sql = f"SELECT {', '.join(select_cols)} FROM empresas WHERE id_empresa = ?"
            cursor.execute(sql, (empresa_id,))
            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                base = resultado[:12]
                (razao, fantasia, cnpj, ie, im, cep, numero,
                complemento, jucesp_cad, dt_cad, jucesp_alt, dt_alt) = base
                extras = resultado[12:]
                    
                self.entry_razao.delete(0, tk.END)
                self.entry_razao.insert(0, razao or "")
                    
                self.entry_fantasia.delete(0, tk.END)
                self.entry_fantasia.insert(0, fantasia or "")
                    
                self.entry_cnpj.delete(0, tk.END)
                self.entry_cnpj.insert(0, cnpj or "")
                    
                self.entry_ie.delete(0, tk.END)
                self.entry_ie.insert(0, ie or "")
                    
                self.entry_im.delete(0, tk.END)
                self.entry_im.insert(0, im or "")
                    
                self.entry_cep.delete(0, tk.END)
                self.entry_cep.insert(0, cep or "")
                    
                self.entry_numero.delete(0, tk.END)
                self.entry_numero.insert(0, numero or "")
                    
                self.entry_complemento.delete(0, tk.END)
                self.entry_complemento.insert(0, complemento or "")
                    
                self.entry_jucesp_cad.delete(0, tk.END)
                self.entry_jucesp_cad.insert(0, jucesp_cad or "")
                    
                self.entry_dt_cad.delete(0, tk.END)
                self.entry_dt_cad.insert(0, dt_cad or "")
                    
                self.entry_jucesp_alt.delete(0, tk.END)
                self.entry_jucesp_alt.insert(0, jucesp_alt or "")
                    
                self.entry_dt_alt.delete(0, tk.END)
                self.entry_dt_alt.insert(0, dt_alt or "")
                if extras:
                    idx = 0
                    if 'nr_ult_oc' in extra_present:
                        self.entry_ult_oc.delete(0, tk.END)
                        self.entry_ult_oc.insert(0, str(extras[idx] or ""))
                        idx += 1
                    if 'nr_ult_of' in extra_present:
                        self.entry_ult_of.delete(0, tk.END)
                        self.entry_ult_of.insert(0, str(extras[idx] or ""))
                        idx += 1
                    if 'nr_ult_nf_sa' in extra_present:
                        self.entry_ult_nfsa.delete(0, tk.END)
                        self.entry_ult_nfsa.insert(0, str(extras[idx] or ""))
        except Exception as e:
            self.show_message(f"Erro ao selecionar empresa: {str(e)}", "error")
    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.entry_razao.delete(0, tk.END)
        self.entry_fantasia.delete(0, tk.END)
        self.entry_cnpj.delete(0, tk.END)
        self.entry_ie.delete(0, tk.END)
        self.entry_im.delete(0, tk.END)
        self.entry_cep.delete(0, tk.END)
        self.entry_numero.delete(0, tk.END)
        self.entry_complemento.delete(0, tk.END)
        self.entry_jucesp_cad.delete(0, tk.END)
        self.entry_dt_cad.delete(0, tk.END)
        self.entry_jucesp_alt.delete(0, tk.END)
        self.entry_dt_alt.delete(0, tk.END)

    # Métodos de navegação
    def ir_primeiro(self):
        try:
            items = self.tree.get_children()
            if items:
                first_item = items[0]
                self.tree.selection_set(first_item)
                self.tree.focus(first_item)
                self.tree.see(first_item)
                self.on_select(None)
        except Exception as e:
            self.show_message(f"Erro ao navegar: {str(e)}", "error")

    def ir_anterior(self):
        try:
            selection = self.tree.selection()
            if not selection:
                self.ir_primeiro()
                return

            current_index = self.tree.index(selection[0])
            if current_index > 0:
                prev_item = self.tree.get_children()[current_index - 1]
                self.tree.selection_set(prev_item)
                self.tree.focus(prev_item)
                self.tree.see(prev_item)
                self.on_select(None)
        except Exception as e:
            self.show_message(f"Erro ao navegar: {str(e)}", "error")

    def ir_proximo(self):
        try:
            selection = self.tree.selection()
            if not selection:
                self.ir_primeiro()
                return

            current_index = self.tree.index(selection[0])
            items = self.tree.get_children()
            if current_index < len(items) - 1:
                next_item = items[current_index + 1]
                self.tree.selection_set(next_item)
                self.tree.focus(next_item)
                self.tree.see(next_item)
                self.on_select(None)
        except Exception as e:
            self.show_message(f"Erro ao navegar: {str(e)}", "error")

    def ir_ultimo(self):
        try:
            items = self.tree.get_children()
            if items:
                last_item = items[-1]
                self.tree.selection_set(last_item)
                self.tree.focus(last_item)
                self.tree.see(last_item)
                self.on_select(None)
        except Exception as e:
            self.show_message(f"Erro inesperado: {str(e)}", "error")
