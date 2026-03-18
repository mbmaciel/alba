import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class GrupoProdutosWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_id = None
        self.current_recnum = None
        aplicar_estilo(self)
        self.set_title("Cadastro de Grupos de Produtos (alba0004)")
        self.config(width=800, height=600)

        # Frame principal
        main_frame = ttkb.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Barra de ferramentas no topo
        toolbar_frame = ttkb.Frame(main_frame, relief="raised", borderwidth=2, padding=5)
        toolbar_frame.pack(fill=tk.X, pady=(0, 15))

        # Create standard message panel
        self.ensure_message_panel(main_frame)

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

        # Botões de busca
        search_container = ttkb.Frame(toolbar_frame)
        search_container.pack(side=tk.LEFT, padx=(10, 0))

        btn_buscar = ttkb.Button(search_container, text="🔍", command=self.buscar_grupo_por_nome, width=3)
        btn_buscar.pack(side=tk.LEFT)
        self.create_tooltip(btn_buscar, "Buscar Grupo")
        
        btn_atualizar = ttkb.Button(search_container, text="🔄", command=self.carregar_dados, width=3)
        btn_atualizar.pack(side=tk.LEFT)
        self.create_tooltip(btn_atualizar, "Atualizar Lista")

        # Frame para campos de entrada
        input_frame = ttkb.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        # Primeira linha - ID do Grupo
        ttkb.Label(input_frame, text="COD").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_id_grupo = ttkb.Entry(input_frame, width=15, state="readonly")
        self.entry_id_grupo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Segunda linha - Nome do Grupo com busca
        ttkb.Label(input_frame, text="Nome do Grupo").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        search_frame = ttkb.Frame(input_frame)
        search_frame.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        self.entry_nm_grupo = ttkb.Entry(search_frame, width=50)
        self.entry_nm_grupo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        search_button = ttkb.Button(search_frame, text="🔍", bootstyle=INFO, command=self.buscar_grupo_por_nome, width=3)
        search_button.pack(side=tk.RIGHT, padx=(5, 0))
        self.create_tooltip(search_button, "Buscar por Nome")

        # Configurar expansão das colunas
        input_frame.grid_columnconfigure(1, weight=1)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview para exibir grupos de produtos
        self.tree = ttkb.Treeview(tree_frame, columns=("id_grupo", "nm_grupo"), show="headings", height=15)
        
        # Configuração das colunas com ordenação pelo COD
        self.sort_id = True  # True=crescente, False=decrescente
        self.tree.heading("id_grupo", text="COD ↕", command=lambda: self.ordenar_id())
        self.tree.heading("nm_grupo", text="Nome do Grupo")
        
        self.tree.column("id_grupo", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("nm_grupo", width=400, minwidth=300, anchor=tk.W)
        
        # Scrollbar para o Treeview
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack do Treeview e Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.carregar_dados()

    def ordenar_id(self):
        """Ordena a lista pelo COD (id_grupo) alternando crescente/decrescente"""
        try:
            ordem = "ASC" if self.sort_id else "DESC"
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute(f"SELECT id_grupo, nm_grupo FROM alba0004 ORDER BY CAST(id_grupo AS INTEGER) {ordem}")
            rows = cursor.fetchall()
            conn.close()

            # Atualiza ícone no cabeçalho
            icon = "↑" if self.sort_id else "↓"
            self.tree.heading("id_grupo", text=f"COD {icon}", command=lambda: self.ordenar_id())

            # Recarrega a tree
            for item in self.tree.get_children():
                self.tree.delete(item)
            for row in rows:
                self.tree.insert("", "end", values=row)

            # Alterna ordem para próxima chamada
            self.sort_id = not self.sort_id
        except Exception as e:
            self.show_message(f"ERRO ao ordenar por COD: {str(e)}", "error")

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
        self.limpar_campos()
        self.entry_nm_grupo.focus()
        self.show_message("Campos limpos. Preencha os dados do novo grupo de produtos.", "info")

    def buscar_grupo_por_nome(self):
        """Busca grupos por nome"""
        nome_busca = self.entry_nm_grupo.get().strip()
        if not nome_busca:
            self.carregar_dados()
            self.show_message("Busca limpa. Mostrando todos os grupos.", "info")
            return
        
        try:
            # Limpar treeview
            for row in self.tree.get_children():
                self.tree.delete(row)
                
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_grupo, nm_grupo FROM alba0004 
                WHERE nm_grupo LIKE ?
                ORDER BY nm_grupo
            """, (f'%{nome_busca}%',))
            
            resultados = cursor.fetchall()
            for row in resultados:
                self.tree.insert("", "end", values=row)
            conn.close()
            
            if resultados:
                self.show_message(f"Encontrados {len(resultados)} grupos para '{nome_busca}'.", "success")
            else:
                self.show_message(f"Nenhum grupo encontrado para '{nome_busca}'.", "warning")
                
        except Exception as e:
            self.show_message(f"ERRO ao buscar grupos: {str(e)}", "error")

    def _execute_save(self):
        """Salva ou atualiza um grupo de produtos"""
        nm_grupo = self.entry_nm_grupo.get().strip()
        try:
            conn = self.conectar()
            cursor = conn.cursor()

            is_update = self.current_id is not None

            if is_update:
                # Atualizar registro existente
                cursor.execute("""
                    UPDATE alba0004 SET nm_grupo = ?
                    WHERE id_grupo = ?
                """, (nm_grupo, self.current_id))

                self.show_message(f"Grupo '{nm_grupo}' atualizado com sucesso!", "success")

            else:
                # Inserir novo registro
                next_recnum = self.get_next_recnum("alba0004")
                if next_recnum is None:
                    self.show_message("ERRO: Não foi possível obter próximo recnum", "error")
                    return

                # Obter próximo ID
                cursor.execute("SELECT COALESCE(MAX(id_grupo), 0) + 1 FROM alba0004")
                next_id_grupo = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO alba0004 (recnum, id_grupo, nm_grupo)
                    VALUES (?, ?, ?)
                """, (next_recnum, next_id_grupo, nm_grupo))

                self.current_id = next_id_grupo
                self.current_recnum = next_recnum

                # Atualizar campo ID na tela
                self.entry_id_grupo.config(state="normal")
                self.entry_id_grupo.delete(0, tk.END)
                self.entry_id_grupo.insert(0, str(next_id_grupo))
                self.entry_id_grupo.config(state="readonly")

                self.show_message(f"Grupo '{nm_grupo}' salvo com sucesso!", "success")

            conn.commit()
            self.carregar_dados()

            if is_update:
                self.selecionar_item_por_id(self.current_id)

        except sqlite3.IntegrityError as e:
            conn.rollback()
            if "nm_grupo" in str(e):
                self.show_message("ERRO: Já existe um grupo com este nome.", "error")
            else:
                self.show_message(f"ERRO ao salvar: {str(e)}", "error")
        except Exception as e:
            conn.rollback()
            self.show_message(f"ERRO inesperado: {str(e)}", "error")
        finally:
            conn.close()

    def salvar(self):
        """Salva ou atualiza um grupo de produtos"""
        nm_grupo = self.entry_nm_grupo.get().strip()
        if not nm_grupo:
            self.show_message("ATENÇÃO: Preencha o nome do grupo.", "warning")
            return

        confirmation_message = f"Confirma a gravação do grupo '{nm_grupo}'?"
        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('save')

        if not self.request_confirmation('save', confirmation_message, self._execute_save):
            return

    def _execute_removal(self, id_grupo, nome_grupo):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alba0004 WHERE id_grupo = ?", (id_grupo,))
            conn.commit()
            conn.close()
            self.carregar_dados()
            self.limpar_campos()
            self.show_message(f"Grupo '{nome_grupo}' removido com sucesso!", "success")
        except Exception as e:
            self.show_message(f"ERRO ao remover grupo: {str(e)}", "error")

    def remover(self):
        """Remove um grupo de produtos"""
        item = self.tree.focus()
        if not item:
            self.show_message("ATENÇÃO: Selecione um grupo para remover.", "warning")
            return

        id_grupo = self.tree.item(item)["values"][0]
        nome_grupo = self.tree.item(item)["values"][1]

        confirmation_message = f"Pressione 'Remover' novamente para excluir o grupo '{nome_grupo}'."

        if not hasattr(self, '_confirmations'):
            self.setup_confirmation_pattern('remove')

        if not self.request_confirmation('remove', confirmation_message, self._execute_removal, id_grupo, nome_grupo):
            return

    def carregar_dados(self):
        """Carrega todos os grupos de produtos"""
        try:
            # Limpar treeview
            for row in self.tree.get_children():
                self.tree.delete(row)
                
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_grupo, nm_grupo FROM alba0004 ORDER BY nm_grupo")
            resultados = cursor.fetchall()
            
            for row in resultados:
                self.tree.insert("", "end", values=row)
            conn.close()
            
            self.show_message(f"Carregados {len(resultados)} grupos de produtos", "success")
            
        except Exception as e:
            self.show_message(f"ERRO ao carregar grupos: {str(e)}", "error")

    def on_select(self, event):
        """Evento de seleção no treeview"""
        item = self.tree.item(self.tree.focus())
        if not item:
            return
            
        try:
            id_grupo = item["values"][0]
            self.current_id = id_grupo
            
            # Buscar dados completos do grupo
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_grupo, nm_grupo, recnum FROM alba0004 WHERE id_grupo = ?", (id_grupo,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                id_grupo, nm_grupo, recnum = result
                self.current_recnum = recnum
                
                # Preencher campos
                self.entry_id_grupo.config(state="normal")
                self.entry_id_grupo.delete(0, tk.END)
                self.entry_id_grupo.insert(0, str(id_grupo))
                self.entry_id_grupo.config(state="readonly")
                
                self.entry_nm_grupo.delete(0, tk.END)
                self.entry_nm_grupo.insert(0, nm_grupo or "")
                
                self.show_message(f"Grupo selecionado: {nm_grupo}", "info")
                
        except Exception as e:
            self.show_message(f"ERRO ao carregar dados do grupo: {str(e)}", "error")

    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.current_id = None
        self.current_recnum = None
        
        self.entry_id_grupo.config(state="normal")
        self.entry_id_grupo.delete(0, tk.END)
        self.entry_id_grupo.config(state="readonly")
        
        self.entry_nm_grupo.delete(0, tk.END)

    def selecionar_item_por_id(self, id_grupo):
        """Seleciona um item na lista pelo ID do grupo"""
        for item in self.tree.get_children():
            valores = self.tree.item(item)["values"]
            if valores and str(valores[0]) == str(id_grupo):
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)
                break

    def ir_primeiro(self):
        """Navega para o primeiro registro"""
        children = self.tree.get_children()
        if children:
            first_item = children[0]
            self.tree.selection_set(first_item)
            self.tree.focus(first_item)
            self.tree.see(first_item)
            self.on_select(None)

    def ir_ultimo(self):
        """Navega para o último registro"""
        children = self.tree.get_children()
        if children:
            last_item = children[-1]
            self.tree.selection_set(last_item)
            self.tree.focus(last_item)
            self.tree.see(last_item)
            self.on_select(None)

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
        else:
            self.ir_primeiro()
