import locale
import os
import sys
import tkinter as tk


def _configure_macos_locale():
    """Normalize locale settings before importing ttkbootstrap on macOS."""
    if sys.platform != "darwin":
        return

    current_lang = os.environ.get("LANG", "")
    current_lc_all = os.environ.get("LC_ALL", "")
    needs_fallback = not current_lang or current_lang == "C.UTF-8" or current_lc_all == "C.UTF-8"

    if needs_fallback:
        os.environ["LANG"] = "en_US.UTF-8"
        os.environ["LC_ALL"] = "en_US.UTF-8"

    try:
        locale.setlocale(locale.LC_ALL, "")
    except locale.Error:
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


_configure_macos_locale()

import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from estilo import aplicar_estilo
from windows.empresas import EmpresaWindow
from windows.contatos import ContatoWindow
from windows.usuarios import UsuarioWindow
from windows.cep import CepWindow
from windows.ncm import NcmWindow
from windows.ativid import AtividWindow
from windows.cfop import CfopWindow
from windows.tiponf import TiponfWindow
from windows.natop import NatopWindow
from windows.endereco import EnderecoWindow
from windows.pessoas import PessoaWindow
from windows.produto_fiscal import ProdutoFiscalWindow
from windows.grupo_produtos import GrupoProdutosWindow
from windows.ordem_compra import OrdemCompraWindow
from windows.item_ordem_compra import ItemOrdemCompraWindow
from windows.comissao import ComissaoWindow
from windows.system_config import SystemConfigWindow
from windows.itens_producao import ItensProducaoWindow
from windows.tipo import TipoWindow
from windows.textos import TextosWindow
from windows.orcamento import OrcamentoWindow
from windows.ordens_faturamento import OrdensFaturamentoWindow
from windows.nota_fiscal import NotaFiscalWindow
from windows.item_nota_fiscal import ItemNotaFiscalWindow
from mdi import MDIContainer

class App(ttkb.Window):
    def __init__(self):
        window_kwargs = {"themename": "flatly"}
        if sys.platform == "darwin":
            # ttkbootstrap's embedded default icon can fail with Apple's Tk builds.
            window_kwargs["iconphoto"] = None

        super().__init__(**window_kwargs)
        aplicar_estilo(self)
        self.title("Sistema Alba")
        self.geometry("1280x900")

        self.mdi = MDIContainer(self)
        self.mdi.pack(fill=tk.BOTH, expand=True)

        self.create_menus()

    def create_menus(self):
        menubar = tk.Menu(self)
        
        # Define menu structure as data
        menu_structure = {
            "Cadastros": [
                {"label": "CEP", "command": self.abrir_cep},
                {"label": "CFOP", "command": self.abrir_cfop},
                {"label": "Naturezas de Operação", "command": self.abrir_natop},
                {"label": "Tipos de Nota Fiscal", "command": self.abrir_tiponf},
                {"label": "NCM", "command": self.abrir_ncm},
                {"label": "Textos", "command": self.abrir_textos},
                {"label": "Comissões", "command": self.abrir_comissao},
                {"label": "Empresas", "command": self.abrir_empresas},
                {"label": "Atividades", "command": self.abrir_ativid},
                {"label": "Tipos de Clientes", "command": self.abrir_tipo},
                {"label": "Contatos", "command": self.abrir_contatos},
                {"label": "Clientes", "command": self.abrir_pessoas},
                {"label": "Grupos de Produtos", "command": self.abrir_grupo_produtos},
                {"label": "Produtos Fiscais", "command": self.abrir_produto_fiscal},
                {"label": "Endereços", "command": self.abrir_endereco},
                {"label": "Notas Fiscais", "command": self.abrir_notas},
                {"label": "Itens de Notas Fiscais", "command": self.abrir_item_nota_fiscal},
            ],
            "Movimentação": [
                {"label": "Orçamentos", "command": self.abrir_orcamento},
                {"label": "Ordens de Compra", "command": self.abrir_ordem_compra},
                {"label": "Itens de Ordens de Compra", "command": self.abrir_item_ordem_compra},
                {"label": "Ordens de Faturamento", "command": self.abrir_ordens_faturamento},
                {"label": "Itens de Produção", "command": self.abrir_itens_producao},
            ],
            "Administração": [
                {"label": "Usuários", "command": self.abrir_usuarios},
                {"label": "Configurações do Sistema", "command": self.abrir_system_config},
            ],
            # Other top-level menus can be added here
        }
        
        # Create menus from structure
        for menu_name, items in menu_structure.items():
            submenu = tk.Menu(menubar, tearoff=0)
            for item in items:
                submenu.add_command(**item)
            menubar.add_cascade(label=menu_name, menu=submenu)
        
        self.config(menu=menubar)

    def abrir_empresas(self):
        EmpresaWindow(self.mdi)

    def abrir_contatos(self):
        ContatoWindow(self.mdi)

    def abrir_usuarios(self):
        UsuarioWindow(self.mdi)

    def abrir_cep(self):
        CepWindow(self.mdi)

    def abrir_ncm(self):
        NcmWindow(self.mdi)

    def abrir_ativid(self):
        AtividWindow(self.mdi)

    def abrir_cfop(self):
        CfopWindow(self.mdi)

    def abrir_tiponf(self):
        TiponfWindow(self.mdi)

    def abrir_natop(self):
        NatopWindow(self.mdi)
    
    def abrir_endereco(self):
        EnderecoWindow(self.mdi)
    
    def abrir_pessoas(self):
        PessoaWindow(self.mdi)

    def abrir_produto_fiscal(self):
        ProdutoFiscalWindow(self.mdi)

    def abrir_ordem_compra(self):
        OrdemCompraWindow(self.mdi)

    def abrir_item_ordem_compra(self):
        ItemOrdemCompraWindow(self.mdi)

    def abrir_comissao(self):
        ComissaoWindow(self.mdi)

    def abrir_system_config(self):
        SystemConfigWindow(self.mdi)

    def abrir_itens_producao(self):
        ItensProducaoWindow(self.mdi)

    def abrir_tipo(self):
        TipoWindow(self.mdi)

    def abrir_textos(self):
        TextosWindow(self.mdi)

    def abrir_orcamento(self):
        OrcamentoWindow(self.mdi)

    def abrir_grupo_produtos(self):
        GrupoProdutosWindow(self.mdi)

    def abrir_ordens_faturamento(self):
        OrdensFaturamentoWindow(self.mdi)

    def abrir_notas(self):
        NotaFiscalWindow(self.mdi)

    def abrir_item_nota_fiscal(self):
        ItemNotaFiscalWindow(self.mdi)

if __name__ == "__main__":
    app = App()
    app.mainloop()
