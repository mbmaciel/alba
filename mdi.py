import tkinter as tk
import ttkbootstrap as ttkb

# Use classic tk colors so they render reliably on macOS (where ttkb.Frame
# uses the native Aqua renderer and ignores background/relief settings,
# making MDI windows invisible).
_COR_FUNDO = "#d4d0c8"
_COR_BARRA_TITULO = "#0a246a"


class MDIContainer(tk.Frame):
    """Container for MDI child windows."""

    def __init__(self, master=None, **kwargs):
        kwargs.setdefault("bg", _COR_FUNDO)
        super().__init__(master, **kwargs)
        self._offset = 10  # initial placement offset

    def register_child(self, child):
        """Place a child window with an incremental offset."""
        x = self._offset
        y = self._offset
        child.place(x=x, y=y)
        child.lift()
        self._offset += 30

class MDIChild(tk.Frame):
    """A movable child window inside an MDIContainer."""

    def __init__(self, master=None, title="", width=400, height=300, **kwargs):
        kwargs.setdefault("bg", _COR_FUNDO)
        super().__init__(master, relief="raised", borderwidth=2, **kwargs)

        # Title bar with close button — use classic tk.Frame/Label/Button so
        # that explicit background colours work on every platform (ttkb widgets
        # use the native Aqua renderer on macOS and ignore bg overrides).
        self.title_bar = tk.Frame(self, bg=_COR_BARRA_TITULO)
        self.title_bar.pack(fill=tk.X)

        self.title_label = tk.Label(
            self.title_bar, text=title, anchor="w", padx=4,
            bg=_COR_BARRA_TITULO, fg="white"
        )
        self.title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.close_button = tk.Button(
            self.title_bar, text="✖", width=3, command=self.destroy,
            bg="#cc0000", fg="white", relief="flat",
            activebackground="#ff4444", activeforeground="white",
            bd=0
        )
        self.close_button.pack(side=tk.RIGHT)

        # Dragging support
        self._drag_start = (0, 0)
        self.title_bar.bind("<ButtonPress-1>", self._on_start)
        self.title_bar.bind("<B1-Motion>", self._on_drag)
        self.title_label.bind("<ButtonPress-1>", self._on_start)
        self.title_label.bind("<B1-Motion>", self._on_drag)

        # pack_propagate(False) is required so that the frame reports its
        # configured dimensions to the place geometry manager rather than the
        # minimum size needed for its children.
        self.config(width=width, height=height)
        self.pack_propagate(False)

        # Place inside container if possible
        if hasattr(master, "register_child"):
            master.register_child(self)

    def _on_start(self, event):
        self._drag_start = (event.x, event.y)

    def _on_drag(self, event):
        dx = event.x - self._drag_start[0]
        dy = event.y - self._drag_start[1]
        x = self.winfo_x() + dx
        y = self.winfo_y() + dy
        self.place_configure(x=x, y=y)

    def set_title(self, text: str):
        """Update the window title."""
        self.title_label.config(text=text)
