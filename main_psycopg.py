# main_psycopg.py
from app.controller.order_controller import OrderController
from app.view.cli_view import (
    run_order_creation,
    run_order_report,
    run_employee_ranking_report
)
from app.view.slq_injection import demonstrar_sql_injection

def exibir_menu_principal():
    """Exibe o menu principal e processa a escolha do usuário"""
    print("--- Sistema de Inserção de Pedidos (vPsycopg) ---")
    
    opcao_valida = False
    while not opcao_valida:
        escolha = input(
        """
Opções:
1. Inserir novo pedido
2. Demonstrar SQL Injection
3. Relatório de Pedido
4. Ranking de Vendas por Funcionário
5. Sair
Escolha: """
        )
        
        if escolha == "1":
            opcao_valida = True
            run_order_creation()
        elif escolha == "2":
            opcao_valida = True
            demonstrar_sql_injection()
        elif escolha == "3":
            opcao_valida = True
            run_order_report()
        elif escolha == "4":
            opcao_valida = True
            run_employee_ranking_report()
        elif escolha == "5":
            opcao_valida = True
            print("Encerrando o programa. Até logo!")
        else:
            print("Opção inválida. Por favor, escolha uma opção de 1 a 5.")

if __name__ == "__main__":
    exibir_menu_principal()