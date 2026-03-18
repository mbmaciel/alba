import sys
import tkinter as tk


def aplicar_estilo(widget):
    fonte_padrao = ("MS Sans Serif", 11)
    fonte_menu = ("MS Sans Serif", 12)

    cor_fundo = "#d4d0c8"
    cor_botao = "#e0e0e0"
    cor_texto = "#000000"
    cor_entrada = "#ffffff"
    cor_borda = "#a0a0a0"
    cor_selecao = "#0a246a"
    cor_texto_selecao = "#ffffff"
    cor_texto_desabilitado = "#666666"

    # On macOS, tk_setPalette and option_add(*Background) conflict with the
    # native aqua rendering used by ttkbootstrap, making window contents
    # invisible.  Skip the classic-Tk palette overrides on that platform and
    # let ttkbootstrap handle the theme entirely.
    if isinstance(widget, (tk.Tk, tk.Toplevel)) and sys.platform != "darwin":
        try:
            widget.tk_setPalette(
                background=cor_fundo,
                foreground=cor_texto,
                activeBackground=cor_botao,
                activeForeground=cor_texto,
                highlightColor=cor_selecao,
                selectBackground=cor_selecao,
                selectForeground=cor_texto_selecao,
            )
        except Exception:
            pass

        try:
            widget.configure(background=cor_fundo)
        except Exception:
            pass

        widget.option_add("*Font", fonte_padrao)
        widget.option_add("*Background", cor_fundo)
        widget.option_add("*Foreground", cor_texto)
        widget.option_add("*insertBackground", cor_texto)

        widget.option_add("*Label.Background", cor_fundo)
        widget.option_add("*Label.Foreground", cor_texto)

        widget.option_add("*Button.Background", cor_botao)
        widget.option_add("*Button.Foreground", cor_texto)
        widget.option_add("*Button.activeBackground", cor_botao)
        widget.option_add("*Button.activeForeground", cor_texto)

        widget.option_add("*Entry.Background", cor_entrada)
        widget.option_add("*Entry.Foreground", cor_texto)
        widget.option_add("*Entry.insertBackground", cor_texto)

        widget.option_add("*Text.Background", cor_entrada)
        widget.option_add("*Text.Foreground", cor_texto)
        widget.option_add("*Text.insertBackground", cor_texto)

        widget.option_add("*Listbox.Background", cor_entrada)
        widget.option_add("*Listbox.Foreground", cor_texto)
        widget.option_add("*Listbox.selectBackground", cor_selecao)
        widget.option_add("*Listbox.selectForeground", cor_texto_selecao)

        widget.option_add("*Menu.Font", fonte_menu)
        widget.option_add("*Menu.Background", cor_fundo)
        widget.option_add("*Menu.Foreground", cor_texto)
        widget.option_add("*Menu.activeBackground", cor_selecao)
        widget.option_add("*Menu.activeForeground", cor_texto_selecao)

        widget.option_add("*Treeview.Font", fonte_padrao)
        widget.option_add("*Treeview.Background", cor_entrada)
        widget.option_add("*Treeview.Foreground", cor_texto)
        widget.option_add("*Treeview.rowheight", 25)
        widget.option_add("*Treeview.Heading.Font", (fonte_padrao[0], fonte_padrao[1], "bold"))
        widget.option_add("*Treeview.Heading.Background", cor_botao)
        widget.option_add("*Treeview.Heading.Foreground", cor_texto)

        widget.option_add("*Frame.Background", cor_fundo)
        widget.option_add("*Scrollbar.Background", cor_fundo)
        widget.option_add("*Scrollbar.troughColor", cor_fundo)
        widget.option_add("*Scrollbar.activeBackground", cor_botao)

    style = getattr(widget, "style", None)
    if style is None:
        return

    style.configure(".", font=fonte_padrao)

    style.configure(
        "TFrame",
        background=cor_fundo,
    )
    style.configure(
        "TLabel",
        background=cor_fundo,
        foreground=cor_texto,
        font=fonte_padrao,
    )
    style.configure(
        "TLabelframe",
        background=cor_fundo,
        bordercolor=cor_borda,
    )
    style.configure(
        "TLabelframe.Label",
        background=cor_fundo,
        foreground=cor_texto,
        font=fonte_padrao,
    )
    style.configure(
        "TButton",
        background=cor_botao,
        foreground=cor_texto,
        bordercolor=cor_borda,
        darkcolor=cor_botao,
        lightcolor=cor_botao,
        focusthickness=1,
        focuscolor=cor_selecao,
        font=fonte_padrao,
    )
    style.map(
        "TButton",
        background=[("pressed", cor_selecao), ("active", cor_botao)],
        foreground=[("pressed", cor_texto_selecao), ("disabled", cor_texto_desabilitado)],
    )
    style.configure(
        "TEntry",
        fieldbackground=cor_entrada,
        foreground=cor_texto,
        insertcolor=cor_texto,
        bordercolor=cor_borda,
    )
    style.map(
        "TEntry",
        fieldbackground=[("readonly", cor_entrada)],
        foreground=[("disabled", cor_texto_desabilitado)],
    )
    style.configure(
        "TCombobox",
        fieldbackground=cor_entrada,
        foreground=cor_texto,
        insertcolor=cor_texto,
        arrowcolor=cor_texto,
        bordercolor=cor_borda,
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", cor_entrada)],
        foreground=[("disabled", cor_texto_desabilitado)],
        selectbackground=[("readonly", cor_selecao)],
        selectforeground=[("readonly", cor_texto_selecao)],
    )
    style.configure(
        "Treeview",
        background=cor_entrada,
        fieldbackground=cor_entrada,
        foreground=cor_texto,
        bordercolor=cor_borda,
        rowheight=25,
        font=fonte_padrao,
    )
    style.map(
        "Treeview",
        background=[("selected", cor_selecao)],
        foreground=[("selected", cor_texto_selecao)],
    )
    style.configure(
        "Treeview.Heading",
        background=cor_botao,
        foreground=cor_texto,
        bordercolor=cor_borda,
        font=(fonte_padrao[0], fonte_padrao[1], "bold"),
    )
    style.map(
        "Treeview.Heading",
        background=[("active", cor_botao)],
        foreground=[("active", cor_texto)],
    )
    style.configure(
        "TNotebook",
        background=cor_fundo,
        bordercolor=cor_borda,
    )
    style.configure(
        "TNotebook.Tab",
        background=cor_botao,
        foreground=cor_texto,
        font=fonte_padrao,
        padding=(10, 4),
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", cor_fundo), ("active", cor_botao)],
        foreground=[("selected", cor_texto)],
    )
    style.configure(
        "TCheckbutton",
        background=cor_fundo,
        foreground=cor_texto,
        font=fonte_padrao,
        indicatorcolor=cor_entrada,
        indicatormargin=2,
    )
    style.map(
        "TCheckbutton",
        background=[("active", cor_fundo)],
        foreground=[("disabled", cor_texto_desabilitado)],
    )
    style.configure(
        "TRadiobutton",
        background=cor_fundo,
        foreground=cor_texto,
        font=fonte_padrao,
        indicatorcolor=cor_entrada,
    )
    style.map(
        "TRadiobutton",
        background=[("active", cor_fundo)],
        foreground=[("disabled", cor_texto_desabilitado)],
    )
    style.configure(
        "TScrollbar",
        background=cor_botao,
        troughcolor=cor_fundo,
        bordercolor=cor_borda,
        arrowcolor=cor_texto,
    )
