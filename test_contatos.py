#!/usr/bin/env python3
"""
Script de teste para verificar se o módulo contatos pode ser importado
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Tentar importar o módulo
    from windows.contatos import ContatoWindow
    print("✓ Módulo contatos importado com sucesso!")
    print("✓ Classe ContatoWindow encontrada")
    
    # Verificar se os métodos necessários existem
    methods_to_check = [
        'carregar_empresas_relacionadas',
        'on_select',
        'limpar_campos',
        'carregar_contatos'
    ]
    
    for method in methods_to_check:
        if hasattr(ContatoWindow, method):
            print(f"✓ Método {method} encontrado")
        else:
            print(f"✗ Método {method} NÃO encontrado")
    
    print("\n✓ Teste concluído com sucesso!")
    
except ImportError as e:
    print(f"✗ Erro ao importar: {e}")
except SyntaxError as e:
    print(f"✗ Erro de sintaxe: {e}")
except Exception as e:
    print(f"✗ Erro inesperado: {e}")