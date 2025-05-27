def aplicar_estilo(widget):
    # Fonte estilo Windows antigo
    fonte_padrao = ("MS Sans Serif", 11)

    fonte_menu = ("MS Sans Serif", 12)

    # Cores clássicas
    cor_fundo = "#d4d0c8"           # cinza claro
    cor_botao = "#e0e0e0"
    cor_texto = "#000000"
    cor_entrada = "#ffffff"
    cor_borda = "#a0a0a0"
    cor_selecao = "#0a246a"         # azul escuro para seleção
    cor_texto_selecao = "#ffffff"   # texto branco para itens selecionados

    # Aplicar estilo a todos os widgets
    widget.option_add("*Font", fonte_padrao)
    widget.option_add("*Background", cor_fundo)
    widget.option_add("*Foreground", cor_texto)
    
    # Labels
    widget.option_add("*Label.Background", cor_fundo)
    widget.option_add("*Label.Foreground", cor_texto)
    
    # Botões
    widget.option_add("*Button.Background", cor_botao)
    widget.option_add("*Button.Foreground", cor_texto)
    
    # Campos de entrada
    widget.option_add("*Entry.Background", cor_entrada)
    widget.option_add("*Entry.Foreground", cor_texto)
    widget.option_add("*TEntry.Background", cor_entrada)
    widget.option_add("*TEntry.Foreground", cor_texto)
    widget.option_add("*TCombobox.Background", cor_entrada)
    widget.option_add("*TCombobox.Foreground", cor_texto)
    
    # Menus
    widget.option_add("*Menu.Font", fonte_padrao)
    widget.option_add("*Menu.Background", cor_fundo)
    widget.option_add("*Menu.Foreground", cor_texto)
    widget.option_add("*Menu.activeBackground", cor_selecao)
    widget.option_add("*Menu.activeForeground", cor_texto_selecao)
    
    # Treeview (listas)
    widget.option_add("*Treeview.Font", fonte_padrao)
    widget.option_add("*Treeview.Background", cor_entrada)
    widget.option_add("*Treeview.Foreground", cor_texto)
    widget.option_add("*Treeview.rowheight", 25)  # Altura da linha para melhor legibilidade
    widget.option_add("*Treeview.Heading.Font", (fonte_padrao[0], fonte_padrao[1], "bold"))
    widget.option_add("*Treeview.Heading.Background", cor_botao)
    widget.option_add("*Treeview.Heading.Foreground", cor_texto)
    
    # Seleção no Treeview
    widget.option_add("*Treeview*selected*Background", cor_selecao)
    widget.option_add("*Treeview*selected*Foreground", cor_texto_selecao)
    
    # Frames
    widget.option_add("*Frame.Background", cor_fundo)
    
    # Scrollbars
    widget.option_add("*Scrollbar.Background", cor_fundo)
    widget.option_add("*Scrollbar.troughColor", cor_fundo)
    widget.option_add("*Scrollbar.activeBackground", cor_botao)
