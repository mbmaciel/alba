import ttkbootstrap as ttkb
from tkinter import messagebox
import sqlite3

DB_PATH = "alba_zip_extracted/alba.sqlite"

class BaseWindow(ttkb.Toplevel):
    """Janela base com utilidades comuns."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

    def conectar(self):
        """Retorna uma conexão com o banco de dados."""
        return sqlite3.connect(DB_PATH)

    def show_message(self, message, msg_type="info"):
        """Exibe mensagem utilizando message_label se disponível."""
        if hasattr(self, "message_label") and self.message_label is not None:
            colors = {
                "info": "blue",
                "success": "green",
                "warning": "orange",
                "error": "red",
            }
            self.message_label.config(text=message, foreground=colors.get(msg_type, "blue"))
            # Limpa a mensagem após alguns segundos
            self.after(5000, lambda: self.message_label.config(text="", foreground="blue"))
        else:
            if msg_type == "error":
                messagebox.showerror("Erro", message)
            elif msg_type == "warning":
                messagebox.showwarning("Aviso", message)
            else:
                messagebox.showinfo("Info", message)

    def ir_primeiro(self):
        items = self.tree.get_children()
        if items:
            item = items[0]
            self.tree.selection_set(item)
            self.tree.focus(item)
            self.tree.see(item)
            if hasattr(self, "on_select"):
                self.on_select(None)

    def ir_ultimo(self):
        items = self.tree.get_children()
        if items:
            item = items[-1]
            self.tree.selection_set(item)
            self.tree.focus(item)
            self.tree.see(item)
            if hasattr(self, "on_select"):
                self.on_select(None)

    def ir_anterior(self):
        selecionado = self.tree.selection()
        if not selecionado:
            self.ir_primeiro()
            return
        items = self.tree.get_children()
        idx = items.index(selecionado[0])
        if idx > 0:
            item = items[idx - 1]
            self.tree.selection_set(item)
            self.tree.focus(item)
            self.tree.see(item)
            if hasattr(self, "on_select"):
                self.on_select(None)

    def ir_proximo(self):
        selecionado = self.tree.selection()
        if not selecionado:
            self.ir_primeiro()
            return
        items = self.tree.get_children()
        idx = items.index(selecionado[0])
        if idx < len(items) - 1:
            item = items[idx + 1]
            self.tree.selection_set(item)
            self.tree.focus(item)
            self.tree.see(item)
            if hasattr(self, "on_select"):
                self.on_select(None)
