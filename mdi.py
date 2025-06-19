import tkinter as tk
import ttkbootstrap as ttkb

class MDIContainer(ttkb.Frame):
    """Container for MDI child windows."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._offset = 10  # initial placement offset

    def register_child(self, child):
        """Place a child window with an incremental offset."""
        x = self._offset
        y = self._offset
        child.place(x=x, y=y)
        self._offset += 30

class MDIChild(ttkb.Frame):
    """A movable child window inside an MDIContainer."""

    def __init__(self, master=None, title="", width=400, height=300, **kwargs):
        super().__init__(master, relief="raised", borderwidth=2, **kwargs)

        # Title bar with close button
        self.title_bar = ttkb.Frame(self, style="primary.TFrame")
        self.title_bar.pack(fill=tk.X)

        self.title_label = ttkb.Label(
            self.title_bar, text=title, anchor="w", padding=2,
            style="primary.Inverse.TLabel", foreground="white"
        )
        self.title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.close_button = ttkb.Button(
            self.title_bar, text="✖", width=3, command=self.destroy,
            style="danger.TButton"
        )
        self.close_button.pack(side=tk.RIGHT)

        # Dragging support
        self._drag_start = (0, 0)
        self.title_bar.bind("<ButtonPress-1>", self._on_start)
        self.title_bar.bind("<B1-Motion>", self._on_drag)
        self.title_label.bind("<ButtonPress-1>", self._on_start)
        self.title_label.bind("<B1-Motion>", self._on_drag)

        # Default size
        self.config(width=width, height=height)

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
