import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from estilo import aplicar_estilo
from windows.base_window import BaseWindow
import sqlite3

class TiponfWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_id = None
        aplicar_estilo(self)
        self.set_title("Cadastro de Tipos de Nota Fiscal")
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

        ttkb.Label(input_frame, text="Nome").grid(row=0, column=0, sticky=tk.W)
        self.entry_nome = ttkb.Entry(input_frame, width=40)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Tipo (fl_tiponf)").grid(row=1, column=0, sticky=tk.W)
        self.combo_tipo = ttkb.Combobox(input_frame, width=27, values=["M", "S"], state="readonly")
        self.combo_tipo.grid(row=1, column=1, pady=5, padx=(5, 20))

        ttkb.Label(input_frame, text="Mapa (fl_mapa)").grid(row=2, column=0, sticky=tk.W)
        self.var_mapa = tk.BooleanVar()
        self.check_mapa = ttkb.Checkbutton(input_frame, text="Ativo", variable=self.var_mapa)
        self.check_mapa.grid(row=2, column=1, pady=5, padx=(5, 20), sticky=tk.W)

        # Frame para o Treeview (área expandida)
        tree_frame = ttkb.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview com colunas redimensionadas
        self.tree = ttkb.Treeview(tree_frame, columns=("id", "nome", "tipo", "mapa"), show="headings", height=15)

        # Configuração das colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("mapa", text="Mapa")

        # Hide the id column
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("nome", width=300, minwidth=200, anchor=tk.W)
        self.tree.column("tipo", width=150, minwidth=100, anchor=tk.CENTER)
        self.tree.column("mapa", width=150, minwidth=100, anchor=tk.CENTER)

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
        self.current_id = None
        self.limpar()
        self.entry_nome.focus()

    def salvar(self):
        try:
            nome = self.entry_nome.get()
            tipo = self.combo_tipo.get()
            mapa = "1" if self.var_mapa.get() else "0"

            if not nome:
                messagebox.showwarning("Atenção", "Nome é obrigatório.")
                return

            conn = self.conectar()
            cursor = conn.cursor()

            try:
                if self.current_id is None:
                    # Novo registro
                    cursor.execute("SELECT COALESCE(MAX(recnum), 0) + 1 FROM tiponf")
                    next_recnum = cursor.fetchone()[0]

                    cursor.execute(
                        "INSERT INTO tiponf (recnum, nm_tiponf, fl_tiponf, fl_mapa) VALUES (?, ?, ?, ?)",
                        (next_recnum, nome, tipo, mapa)
                    )
                    messagebox.showinfo("Sucesso", "Registro incluído com sucesso!")
                else:
                    # Atualização
                    cursor.execute(
                        "UPDATE tiponf SET nm_tiponf=?, fl_tiponf=?, fl_mapa=? WHERE id_tiponf=?",
                        (nome, tipo, mapa, self.current_id)
                    )
                    messagebox.showinfo("Sucesso", "Registro atualizado com sucesso!")

                conn.commit()
                self.limpar()
                self.carregar()
                self.current_id = None

            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao salvar registro: {str(e)}")
                conn.rollback()
            finally:
                conn.close()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")

    def remover(self):
        try:
            item = self.tree.focus()
            if not item:
                messagebox.showwarning("Atenção", "Selecione um registro para remover.")
                return

            if not messagebox.askyesno("Confirmar", "Deseja realmente remover este registro?"):
                return

            id_tiponf = self.tree.item(item)["values"][0]
            conn = self.conectar()
            cursor = conn.cursor()

            try:
                cursor.execute("DELETE FROM tiponf WHERE id_tiponf = ?", (id_tiponf,))
                conn.commit()
                messagebox.showinfo("Sucesso", "Registro removido com sucesso!")
                self.limpar()
                self.carregar()
                self.current_id = None

            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao remover registro: {str(e)}")
                conn.rollback()
            finally:
                conn.close()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")

    def carregar(self):
        try:
            self.tree.delete(*self.tree.get_children())
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_tiponf, nm_tiponf, fl_tiponf, fl_mapa FROM tiponf ORDER BY nm_tiponf")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar registros: {str(e)}")

    def on_select(self, event):
        try:
            item = self.tree.focus()
            if not item:
                return
            values = self.tree.item(item)["values"]
            if not values:
                return

            self.current_id = values[0]
            nome = values[1]
            tipo = values[2]

            # Preencher os campos
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, nome)
            self.combo_tipo.set(tipo if tipo else "")

            # Buscar o valor real do mapa no banco de dados
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT fl_mapa FROM tiponf WHERE id_tiponf = ?", (self.current_id,))
            result = cursor.fetchone()
            if result:
                mapa_value = result[0]
                # Converter para boolean - aceita tanto string quanto número
                self.var_mapa.set(str(mapa_value) == "1" or mapa_value == 1)
            conn.close()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao selecionar registro: {str(e)}")

    def limpar(self):
        self.entry_nome.delete(0, tk.END)
        self.combo_tipo.set("")
        self.var_mapa.set(False)

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
            messagebox.showerror("Erro", f"Erro ao navegar: {str(e)}")

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
            messagebox.showerror("Erro", f"Erro ao navegar: {str(e)}")

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
            messagebox.showerror("Erro", f"Erro ao navegar: {str(e)}")

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
            messagebox.showerror("Erro", f"Erro ao navegar: {str(e)}")
        
