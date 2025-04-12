from app.view.cli_view import (
    run_order_creation,
    run_order_report,
    run_employee_ranking_report
)
from app.view.slq_injection import demonstrar_sql_injection

def exibir_menu_principal():
    """Exibe o menu principal e processa a escolha do usuário"""
    print("--- Sistema de Inserção de Pedidos (vPsycopg) ---")
    
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
    
    if escolha == "2":
        demonstrar_sql_injection()
        return
    
    if escolha == "5":
        print("Encerrando o programa. Até logo!")
        return
        
    if escolha in ["1", "3", "4"]:
        modo = ""
        while modo not in ["1", "2"]:
            modo = input(
            """
Selecione o modo de execução:
1. psycopg
2. sqlalchemy
Escolha: """
            )
            if modo not in ["1", "2"]:
                print("Opção inválida. Por favor, escolha 1 ou 2.")
        
        modo = "psycopg" if modo == "1" else "sqlalchemy"
        
        if escolha == "1":
            run_order_creation(modo)
        elif escolha == "3":
            run_order_report(modo)
        elif escolha == "4":
            run_employee_ranking_report(modo)
    else:
        print("Opção inválida. Por favor, escolha uma opção de 1 a 5.")
        exibir_menu_principal()

if __name__ == "__main__":
    continuar = True
    while continuar:
        exibir_menu_principal()
        continuar_resp = input("\nDeseja realizar outra operação? (S/N): ").upper()
        if continuar_resp == "N":
            continuar = False
        elif continuar_resp == "S":
            continuar = True
        else:
            print("Opção inválida. Por favor, escolha S ou N.")
    
    print("Programa encerrado. Até logo!")