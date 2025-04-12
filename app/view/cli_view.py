from app.controller.order_controller import OrderController
from typing import Dict, List, Tuple, Any
from datetime import datetime, date

def get_order_input() -> dict:
    """
    Coleta todos os dados necessários para criar um novo pedido através da linha de comando.
    
    Returns:
        dict: Dicionário contendo todos os dados do pedido organizados
    """
    order_data = {}
    
    print("\n===== DADOS DO CLIENTE =====")
    order_data['customer'] = input("Nome Cliente: ")
    
    print("\n===== DADOS DO FUNCIONÁRIO =====")
    first_name = input("Primeiro nome do funcionário: ")
    last_name = input("Sobrenome do funcionário: ")
    order_data['employee'] = (first_name, last_name)
    
    print("\n===== DADOS DE ENVIO =====")
    shipping_data = {}
    
    shipping_data['ship_name'] = input("Nome para envio: ")
    shipping_data['ship_address'] = input("Endereço de envio: ")
    shipping_data['ship_city'] = input("Cidade de envio: ")
    shipping_data['ship_region'] = input("Região/Estado de envio: ")
    shipping_data['ship_postal_code'] = input("Código postal de envio: ")
    shipping_data['ship_country'] = input("País de envio: ")
    
    try:
        freight_str = input("Frete (deixe em branco para 0): ")
        shipping_data['freight'] = float(freight_str) if freight_str.strip() else 0.0
        
        shipper_id_str = input("ID do transportador (deixe em branco se não souber): ")
        if shipper_id_str.strip():
            shipping_data['shipper_id'] = int(shipper_id_str)
    except ValueError:
        print("Valor inválido informado. Usando valores padrão.")
    
    order_data['shipping'] = shipping_data
    
    print("\n===== ITENS DO PEDIDO =====")
    items_data = []
    
    while True:
        print(f"\nItem #{len(items_data) + 1}")
        item = {}
        
        item['product_name'] = input("Nome do produto: ")
        
        try:
            item['quantity'] = int(input("Quantidade: "))
            
            discount_str = input("Desconto (0.1 para 10%, 0 para nenhum): ")
            item['discount'] = float(discount_str) if discount_str.strip() else 0.0
            
        except ValueError:
            print("Valor inválido. Usando valores padrão (quantidade=1, desconto=0).")
            item['quantity'] = 1
            item['discount'] = 0.0
        
        items_data.append(item)
        
        if input("\nDeseja adicionar mais itens? (S/N): ").upper() != 'S':
            break
    
    order_data['items'] = items_data
    
    return order_data

def display_result(success: bool, message: str) -> None:
    """
    Exibe o resultado da operação de criação de pedido.
    
    Args:
        success (bool): Indica se a operação foi bem-sucedida
        message (str): Mensagem a ser exibida
    """
    if success:
        print(f"\n[SUCESSO] {message}")
    else:
        print(f"\n[ERRO] {message}")

def get_order_id_input() -> int:
    """
    Coleta e valida o ID do pedido a ser consultado.
    
    Returns:
        int: ID do pedido validado
    """
    while True:
        try:
            order_id = input("Digite o ID do pedido que deseja consultar: ")
            order_id = int(order_id)
            
            if order_id <= 0:
                raise ValueError("ID deve ser um número positivo")
                
            return order_id
        except ValueError as e:
            print(f"Erro: {e}. Por favor, digite um número inteiro positivo.")

def get_date_range_input() -> tuple[date, date]:
    """
    Coleta e valida um intervalo de datas para consulta.
    
    Returns:
        tuple[date, date]: Tupla contendo data inicial e data final
    """
    while True:
        try:
            print("(Formato de data: AAAA-MM-DD)")
            
            start_date_str = input("Data inicial: ")
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            
            end_date_str = input("Data final: ")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            
            if start_date > end_date:
                raise ValueError("A data inicial não pode ser posterior à data final")
                
            return start_date, end_date
            
        except ValueError as e:
            if "does not match format" in str(e):
                print("Erro: Formato de data inválido. Use AAAA-MM-DD.")
            else:
                print(f"Erro: {e}")

def display_order_report(report_data: dict) -> None:
    """
    Exibe um relatório formatado de um pedido.
    
    Args:
        report_data (dict): Dados do pedido a serem exibidos
    """
    
    print(f"Número do pedido: {report_data['order_id']}")
    print(f"Data do pedido: {report_data['order_date']}")
    print(f"Nome do Cliente: {report_data['customer_name']}")
    print(f"Nome do Vendedor: {report_data['employee_name']}")
    print(f"Itens do pedido: ")
    for item in report_data['items']:
        print(f"\tProduto: {item['product_name']:<30} Quantidade: {item['quantity']:<8} Valor total: {item['total_price']:>15.2f}")

def display_employee_ranking(ranking_data: list) -> None:
    """
    Exibe um relatório formatado do ranking de vendas dos funcionários.
    
    Args:
        ranking_data (list): Lista de dados do ranking a serem exibidos
    """
    if isinstance(ranking_data, str):
        print(f"\n{ranking_data}")
        return
    
    separator = "=" * 75
    
    print(separator)
    print("RANKING DE VENDAS POR FUNCIONÁRIO")
    print(separator)
    
    # Cabeçalho da tabela
    print(f"{'POS.':<5} {'FUNCIONÁRIO':<30} {'QTD PEDIDOS':<15} {'VALOR TOTAL':>15}")
    print("-" * 75)
    
    # Dados do ranking
    for i, employee in enumerate(ranking_data, 1):
        print(f"{i:<5} {employee['employee_name']:<30} {employee['total_orders']:<15} {employee['total_value']:>15.2f}")
    
    print(separator)

def run_order_creation(mode: str) -> None:
    """
    Função principal que orquestra o processo de criação de pedido,
    coletando dados e exibindo resultados.
    """
    print("\n=== CRIAÇÃO DE NOVO PEDIDO ===")
    
    order_data = get_order_input()
    
    if mode == "psycopg":
        success, message = OrderController.create_new_order_psycopg(
            customer_name=order_data['customer'],
            employee_first_name=order_data['employee'][0],
            employee_last_name=order_data['employee'][1],
            items_data=order_data['items'],
            shipping_data=order_data['shipping']
        )
    elif mode == "sqlalchemy":
        success, message = OrderController.create_new_order_sqlalchemy(
            customer_name=order_data['customer'],
            employee_first_name=order_data['employee'][0],
            employee_last_name=order_data['employee'][1],
            items_data=order_data['items'],
            shipping_data=order_data['shipping']
        )
    
    display_result(success, message)

def run_order_report(mode: str) -> None:
    """
    Função principal que orquestra o processo de geração de relatório de pedido,
    coletando o ID do pedido e exibindo os detalhes.
    """
    print("\n=== RELATÓRIO DE PEDIDO ===")
    
    order_id = get_order_id_input()
    
    if mode == "psycopg":
        success, data = OrderController.get_order_report_psycopg(order_id)
    elif mode == "sqlalchemy":
        success, data = OrderController.get_order_report_sqlalchemy(order_id)
    
    if success:
        display_order_report(data)
    else:
        print(f"\n[ERRO] {data}")

def run_employee_ranking_report(mode: str) -> None:
    """
    Função principal que orquestra o processo de geração de ranking de vendas,
    coletando o intervalo de datas e exibindo o ranking.
    """
    print("\n=== RANKING DE VENDAS POR FUNCIONÁRIO ===")
    
    start_date, end_date = get_date_range_input()
    
    print(f"\nGerando ranking para o período de {start_date} a {end_date}...")
    
    if mode == "psycopg":
        success, data = OrderController.get_employee_ranking_report_psycopg(start_date, end_date)
    elif mode == "sqlalchemy":
        success, data = OrderController.get_employee_ranking_report_sqlalchemy(start_date, end_date)
    
    if success:
        display_employee_ranking(data)
    else:
        print(f"\n[ERRO] {data}")

if __name__ == "__main__":
    run_order_creation()
