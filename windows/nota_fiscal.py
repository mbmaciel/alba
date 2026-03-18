
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3
from datetime import datetime
import os

class NotaFiscalWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_id = None  # Para controlar inserção/atualização
        aplicar_estilo(self)
        self.set_title("Cadastro de Notas Fiscais")
        self.config(width=1200, height=700)

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
        ttkb.Label(input_frame, text="Empresa").grid(row=0, column=0, sticky=tk.W)
        self.combo_empresa = ttkb.Combobox(input_frame, width=30, state="readonly")
        self.combo_empresa.grid(row=0, column=1, padx=5, pady=5)

        ttkb.Label(input_frame, text="Número").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.entry_nr_nota = ttkb.Entry(input_frame, width=10)
        self.entry_nr_nota.grid(row=0, column=3, padx=5, pady=5)

        ttkb.Label(input_frame, text="Série").grid(row=0, column=4, sticky=tk.W, padx=(20, 0))
        self.entry_serie = ttkb.Entry(input_frame, width=10)
        self.entry_serie.grid(row=0, column=5, padx=5, pady=5)

        # Segunda linha
        ttkb.Label(input_frame, text="Cliente").grid(row=1, column=0, sticky=tk.W)
        self.combo_cliente = ttkb.Combobox(input_frame, width=30, state="readonly")
        self.combo_cliente.grid(row=1, column=1, padx=5, pady=5)

        ttkb.Label(input_frame, text="Tipo").grid(row=1, column=2, sticky=tk.W, padx=(20, 0))
        self.entry_tipo = ttkb.Entry(input_frame, width=10)
        self.entry_tipo.grid(row=1, column=3, padx=5, pady=5)

        ttkb.Label(input_frame, text="Data").grid(row=1, column=4, sticky=tk.W, padx=(20, 0))
        self.entry_data = ttkb.Entry(input_frame, width=12)
        self.entry_data.grid(row=1, column=5, padx=5, pady=5)

        # Terceira linha
        ttkb.Label(input_frame, text="Transportadora").grid(row=2, column=0, sticky=tk.W)
        self.combo_transp = ttkb.Combobox(input_frame, width=30, state="readonly")
        self.combo_transp.grid(row=2, column=1, padx=5, pady=5)

        ttkb.Label(input_frame, text="Total").grid(row=2, column=2, sticky=tk.W, padx=(20, 0))
        self.entry_total = ttkb.Entry(input_frame, width=12)
        self.entry_total.grid(row=2, column=3, padx=5, pady=5)

        ttkb.Label(input_frame, text="Situação").grid(row=2, column=4, sticky=tk.W, padx=(20, 0))
        self.entry_situacao = ttkb.Entry(input_frame, width=12)
        self.entry_situacao.grid(row=2, column=5, padx=5, pady=5)

        # Quarta linha
        ttkb.Label(input_frame, text="Texto padrão").grid(row=3, column=0, sticky=tk.W)
        self.combo_texto = ttkb.Combobox(input_frame, width=30, state="readonly")
        self.combo_texto.grid(row=3, column=1, padx=5, pady=5)

        ttkb.Label(input_frame, text="Tipo de Frete").grid(row=3, column=2, sticky=tk.W, padx=(20, 0))
        self.combo_frete = ttkb.Combobox(input_frame, width=15, state="readonly")
        self.combo_frete["values"] = ["0 - Sem frete", "1 - Emitente", "2 - Destinatário"]
        self.combo_frete.grid(row=3, column=3, padx=5, pady=5)

        ttkb.Label(input_frame, text="Placa").grid(row=3, column=4, sticky=tk.W, padx=(20, 0))
        self.entry_placa = ttkb.Entry(input_frame, width=12)
        self.entry_placa.grid(row=3, column=5, padx=5, pady=5)

        # Quinta linha - campos longos
        ttkb.Label(input_frame, text="Prazo").grid(row=4, column=0, sticky=tk.W)
        self.entry_prazo = ttkb.Entry(input_frame, width=80)
        self.entry_prazo.grid(row=4, column=1, columnspan=5, padx=5, pady=5, sticky=tk.W+tk.E)

        ttkb.Label(input_frame, text="Condições").grid(row=5, column=0, sticky=tk.W)
        self.entry_condicoes = ttkb.Entry(input_frame, width=80)
        self.entry_condicoes.grid(row=5, column=1, columnspan=5, padx=5, pady=5, sticky=tk.W+tk.E)

        ttkb.Label(input_frame, text="Observações").grid(row=6, column=0, sticky=tk.W)
        self.entry_obs = ttkb.Entry(input_frame, width=80)
        self.entry_obs.grid(row=6, column=1, columnspan=5, padx=5, pady=5, sticky=tk.W+tk.E)

        # Configurar expansão das colunas
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)
        input_frame.columnconfigure(5, weight=1)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id_nota", "empresa", "cliente", "numero", "total", "sit", "data"), show="headings", height=15)
        
        # Configuração das colunas
        self.tree.heading("id_nota", text="COD")
        self.tree.heading("empresa", text="Empresa")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("numero", text="Número")
        self.tree.heading("total", text="Total")
        self.tree.heading("sit", text="Situação")
        self.tree.heading("data", text="Data")
        
        # Hide the id column
        self.tree.column("id_nota", width=0, stretch=False)
        self.tree.column("empresa", width=200, minwidth=150, anchor=tk.W)
        self.tree.column("cliente", width=200, minwidth=150, anchor=tk.W)
        self.tree.column("numero", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("total", width=100, minwidth=80, anchor=tk.E)
        self.tree.column("sit", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("data", width=100, minwidth=80, anchor=tk.CENTER)
        
        # Scrollbar para o Treeview
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_empresas()
        self.carregar_clientes()
        self.carregar_transportadoras()
        self.carregar_textos()
        self.carregar()
        self.ir_primeiro()

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

    def novo(self):
        """Limpa os campos para inclusão de novo registro"""
        self.current_id = None
        self.limpar()
        self.combo_empresa.focus()
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, datetime.today().strftime("%Y-%m-%d"))
        self.show_message("Novo registro. Preencha os campos e salve.", "info")

    def carregar_empresas(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_empresa, nm_razao FROM empresas ORDER BY nm_razao")
            self.empresas = cursor.fetchall()
            conn.close()
            self.combo_empresa['values'] = [nome for _, nome in self.empresas]
        except Exception as e:
            self.show_message(f"Erro ao carregar empresas: {str(e)}", "error")
            self.empresas = []

    def carregar_clientes(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_pessoa, nm_razao FROM alba0001 ORDER BY nm_razao")
            self.clientes = cursor.fetchall()
            conn.close()
            self.combo_cliente['values'] = [nome for _, nome in self.clientes]
        except Exception as e:
            self.show_message(f"Erro ao carregar clientes: {str(e)}", "error")
            self.clientes = []

    def carregar_transportadoras(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_pessoa, nm_razao FROM alba0001 ORDER BY nm_razao")
            self.transp = cursor.fetchall()
            conn.close()
            self.combo_transp['values'] = [nome for _, nome in self.transp]
        except Exception as e:
            self.show_message(f"Erro ao carregar transportadoras: {str(e)}", "error")
            self.transp = []

    def carregar_textos(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_texto, nm_descricao FROM textos ORDER BY nm_descricao")
            self.textos = cursor.fetchall()
            conn.close()
            self.combo_texto['values'] = [desc for _, desc in self.textos]
            self.combo_texto.bind("<<ComboboxSelected>>", self.preencher_textos)
        except Exception as e:
            self.show_message(f"Erro ao carregar textos: {str(e)}", "error")
            self.textos = []

    def preencher_textos(self, event=None):
        try:
            descricao = self.combo_texto.get()
            id_texto = next((id for id, desc in self.textos if desc == descricao), None)
            if not id_texto:
                return

            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT tx_prazo, tx_condicoes, tx_obs FROM textos WHERE id_texto = ?", (id_texto,))
            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                self.entry_prazo.delete(0, tk.END)
                self.entry_condicoes.delete(0, tk.END)
                self.entry_obs.delete(0, tk.END)
                self.entry_prazo.insert(0, resultado[0] or "")
                self.entry_condicoes.insert(0, resultado[1] or "")
                self.entry_obs.insert(0, resultado[2] or "")
                self.show_message("Texto padrão aplicado com sucesso.", "success")
        except Exception as e:
            self.show_message(f"Erro ao preencher textos: {str(e)}", "error")

    def salvar(self):
        try:
            # Validações básicas
            if not self.combo_empresa.get():
                self.show_message("Selecione uma empresa.", "warning")
                return
            if not self.entry_nr_nota.get():
                self.show_message("Informe o número da nota fiscal.", "warning")
                return

            id_empresa = next((id for id, nome in self.empresas if nome == self.combo_empresa.get()), None)
            id_cliente = next((id for id, nome in self.clientes if nome == self.combo_cliente.get()), None)
            id_transp = next((id for id, nome in self.transp if nome == self.combo_transp.get()), None)
            id_texto = next((id for id, desc in self.textos if desc == self.combo_texto.get()), None)

            frete_valor = "0"
            if self.combo_frete.get():
                frete_valor = self.combo_frete.get().split(" - ")[0]

            conn = self.conectar()
            cursor = conn.cursor()

            if self.current_id is None:
                # Novo registro - INSERT
                data = (
                    self.entry_nr_nota.get(), self.entry_serie.get(), self.entry_tipo.get(), self.entry_data.get(),
                    self.entry_total.get(), self.entry_situacao.get(), self.entry_obs.get(),
                    id_empresa, id_cliente, id_transp, id_texto,
                    self.entry_prazo.get(), self.entry_condicoes.get(),
                    frete_valor, self.entry_placa.get()
                )
                cursor.execute("""
                    INSERT INTO alba0012 (
                        nr_nota, cd_serie, tp_nota, dt_emissao, vl_total_nf,
                        fl_situacao, tx_obs, id_empresa, id_cliente,
                        id_transp, id_texto, tx_prazo, tx_condicoes, fl_frete, cd_placa
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, data)
                self.show_message(f"Nota fiscal {self.entry_nr_nota.get()} incluída com sucesso!", "success")
            else:
                # Atualização - UPDATE
                data = (
                    self.entry_nr_nota.get(), self.entry_serie.get(), self.entry_tipo.get(), self.entry_data.get(),
                    self.entry_total.get(), self.entry_situacao.get(), self.entry_obs.get(),
                    id_empresa, id_cliente, id_transp, id_texto,
                    self.entry_prazo.get(), self.entry_condicoes.get(),
                    frete_valor, self.entry_placa.get(), self.current_id
                )
                cursor.execute("""
                    UPDATE alba0012 SET
                        nr_nota=?, cd_serie=?, tp_nota=?, dt_emissao=?, vl_total_nf=?,
                        fl_situacao=?, tx_obs=?, id_empresa=?, id_cliente=?,
                        id_transp=?, id_texto=?, tx_prazo=?, tx_condicoes=?, fl_frete=?, cd_placa=?
                    WHERE id_nota=?
                """, data)
                self.show_message(f"Nota fiscal {self.entry_nr_nota.get()} atualizada com sucesso!", "success")

            conn.commit()
            conn.close()
            self.limpar()
            self.carregar()
        except Exception as e:
            self.show_message(f"Erro ao salvar: {str(e)}", "error")

    def remover(self):
        try:
            item = self.tree.focus()
            if not item:
                self.show_message("Selecione uma nota fiscal para remover.", "warning")
                return
            
            item_values = self.tree.item(item)["values"]
            id_nota = item_values[0]
            numero = item_values[3]
            
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alba0012 WHERE id_nota = ?", (id_nota,))
            conn.commit()
            conn.close()
            
            self.show_message(f"Nota fiscal {numero} removida com sucesso!", "success")
            self.carregar()
            self.limpar()
        except Exception as e:
            self.show_message(f"Erro ao remover: {str(e)}", "error")

    def carregar(self):
        try:
            self.tree.delete(*self.tree.get_children())
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT n.id_nota, e.nm_razao AS empresa, c.nm_razao AS cliente,
                       n.nr_nota, n.vl_total_nf, n.fl_situacao, n.dt_emissao
                FROM alba0012 n
                LEFT JOIN empresas e ON n.id_empresa = e.id_empresa
                LEFT JOIN alba0001 c ON n.id_cliente = c.id_pessoa
                ORDER BY n.id_nota DESC
            """)
            resultados = cursor.fetchall()
            for row in resultados:
                self.tree.insert("", "end", values=row)
            conn.close()
            self.show_message(f"Carregadas {len(resultados)} notas fiscais", "success")
        except Exception as e:
            self.show_message(f"Erro ao carregar dados: {str(e)}", "error")

    def on_select(self, event):
        try:
            item = self.tree.item(self.tree.focus())
            if not item or not item.get("values"):
                return
            
            values = item["values"]
            if len(values) >= 7:
                id_nota = values[0]
                self.current_id = id_nota  # Armazenar ID para edição
                
                # Carregar dados completos da nota
                conn = self.conectar()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT n.id_nota, n.nr_nota, n.cd_serie, n.tp_nota, n.dt_emissao,
                           n.vl_total_nf, n.fl_situacao, n.tx_obs, n.tx_prazo, n.tx_condicoes,
                           n.fl_frete, n.cd_placa,
                           e.nm_razao AS empresa, c.nm_razao AS cliente,
                           t.nm_razao AS transp, tx.nm_descricao AS texto
                    FROM alba0012 n
                    LEFT JOIN empresas e ON n.id_empresa = e.id_empresa
                    LEFT JOIN alba0001 c ON n.id_cliente = c.id_pessoa
                    LEFT JOIN alba0001 t ON n.id_transp = t.id_pessoa
                    LEFT JOIN textos tx ON n.id_texto = tx.id_texto
                    WHERE n.id_nota = ?
                """, (id_nota,))
                nota = cursor.fetchone()
                columns = [desc[0] for desc in cursor.description]
                conn.close()
                
                if nota:
                    dados = dict(zip(columns, nota))
                    # Preencher campos
                    self.combo_empresa.set(dados.get("empresa") or "")
                    self.combo_cliente.set(dados.get("cliente") or "")
                    self.combo_transp.set(dados.get("transp") or "")
                    self.combo_texto.set(dados.get("texto") or "")
                    
                    self.entry_nr_nota.delete(0, tk.END)
                    self.entry_nr_nota.insert(0, str(dados.get("nr_nota") or ""))
                    
                    self.entry_serie.delete(0, tk.END)
                    self.entry_serie.insert(0, str(dados.get("cd_serie") or ""))
                    
                    self.entry_tipo.delete(0, tk.END)
                    self.entry_tipo.insert(0, str(dados.get("tp_nota") or ""))
                    
                    self.entry_data.delete(0, tk.END)
                    self.entry_data.insert(0, str(dados.get("dt_emissao") or ""))
                    
                    self.entry_total.delete(0, tk.END)
                    self.entry_total.insert(0, str(dados.get("vl_total_nf") or ""))
                    
                    self.entry_situacao.delete(0, tk.END)
                    self.entry_situacao.insert(0, str(dados.get("fl_situacao") or ""))
                    
                    self.entry_obs.delete(0, tk.END)
                    self.entry_obs.insert(0, str(dados.get("tx_obs") or ""))
                    
                    self.entry_prazo.delete(0, tk.END)
                    self.entry_prazo.insert(0, str(dados.get("tx_prazo") or ""))
                    
                    self.entry_condicoes.delete(0, tk.END)
                    self.entry_condicoes.insert(0, str(dados.get("tx_condicoes") or ""))
                    
                    self.entry_placa.delete(0, tk.END)
                    self.entry_placa.insert(0, str(dados.get("cd_placa") or ""))
                    
                    # Frete
                    frete_val = str(dados.get("fl_frete") or "0")
                    frete_options = ["0 - Sem frete", "1 - Emitente", "2 - Destinatário"]
                    frete_selected = next((opt for opt in frete_options if opt.startswith(frete_val)), "")
                    self.combo_frete.set(frete_selected)
                    
                    self.show_message(f"Nota fiscal {dados.get('nr_nota')} selecionada para edição", "info")
        except Exception as e:
            self.show_message(f"Erro ao selecionar: {str(e)}", "error")

    def limpar(self):
        """Limpa todos os campos do formulário"""
        self.current_id = None
        for widget in [
            self.combo_empresa, self.combo_cliente, self.combo_transp, self.combo_texto,
            self.entry_nr_nota, self.entry_serie, self.entry_tipo, self.entry_data,
            self.entry_total, self.entry_situacao, self.entry_obs,
            self.entry_prazo, self.entry_condicoes, self.combo_frete, self.entry_placa
        ]:
            if isinstance(widget, ttkb.Combobox):
                widget.set("")
            else:
                widget.delete(0, tk.END)

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
