import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
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
from windows.ordem_compra import OrdemCompraWindow
from windows.item_ordem_compra import ItemOrdemCompraWindow
from windows.comissao import ComissaoWindow
from windows.system_config import SystemConfigWindow
from windows.itens_producao import ItensProducaoWindow
from windows.tipo import TipoWindow
from windows.textos import TextosWindow
from mdi import MDIContainer

class App(ttkb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        aplicar_estilo(self)
        self.title("Sistema Alba")
        self.geometry("1200x800")

        self.mdi = MDIContainer(self)
        self.mdi.pack(fill=tk.BOTH, expand=True)

        self.create_menus()

    def create_menus(self):
        menubar = tk.Menu(self)
        
        # Define menu structure as data
        menu_structure = {
            "Cadastros": [
                {"label": "Empresas", "command": self.abrir_empresas},
                {"label": "Contatos", "command": self.abrir_contatos},
                {"label": "Usuários", "command": self.abrir_usuarios},
                {"label": "CEP", "command": self.abrir_cep},
                {"label": "NCM", "command": self.abrir_ncm},
                {"label": "Atividades", "command": self.abrir_ativid},
                {"label": "CFOP", "command": self.abrir_cfop},
                {"label": "Tipos de Nota Fiscal", "command": self.abrir_tiponf},
                {"label": "Naturezas de Operação", "command": self.abrir_natop},
                {"label": "Endereços", "command": self.abrir_endereco},
                {"label": "Pessoas", "command": self.abrir_pessoas},
                {"label": "Produtos Fiscais", "command": self.abrir_produto_fiscal},
                {"label": "Comissões", "command": self.abrir_comissao},
                {"label": "Itens de Produção", "command": self.abrir_itens_producao},
                {"label": "Tipos de Clientes", "command": self.abrir_tipo},
                {"label": "Textos", "command": self.abrir_textos},
            ],
            "Movimentação": [
                {"label": "Ordens de Compra", "command": self.abrir_ordem_compra},
                {"label": "Itens de Ordens de Compra", "command": self.abrir_item_ordem_compra},
            ],
            "Administração": [
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

if __name__ == "__main__":
    app = App()
    app.mainloop()
