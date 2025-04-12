from app.dao.psycopg import (
    find_customer_id_by_name,
    find_employee_id_by_name,
    find_product_id_and_price_by_name,
    insert_order,
    insert_order_detail,
    find_order_with_details,
    get_employee_sales_ranking
)
from app.model.driver_model import Orders, OrderDetails
from datetime import date

class OrderController:
    @staticmethod
    def create_new_order(
        customer_name: str,
        employee_first_name: str, 
        employee_last_name: str,
        items_data: list[dict],
        shipping_data: dict = None
    ) -> tuple[bool, str]:
        """
        Orchestrates the creation of a new order with its details.
        
        Args:
            customer_name: Name of the customer company
            employee_first_name: First name of the employee
            employee_last_name: Last name of the employee
            items_data: List of dictionaries with product details
                Each dict contains: 'product_name', 'quantity', 'discount'
            shipping_data: Dictionary with shipping information
                May contain: 'shipper_id', 'freight', 'ship_name', 'ship_address',
                'ship_city', 'ship_region', 'ship_postal_code', 'ship_country'
        
        Returns:
            tuple[bool, str]: A tuple containing success status and message
        """
        # Initialize shipping_data if None
        if shipping_data is None:
            shipping_data = {}
        
        # Find customer ID
        customer_id = find_customer_id_by_name(customer_name)
        if customer_id is None:
            return (False, "Erro: Cliente não encontrado.")
        
        # Find employee ID
        employee_id = find_employee_id_by_name(employee_first_name, employee_last_name)
        if employee_id is None:
            return (False, "Erro: Funcionário não encontrado.")
        
        # Get current date for order_date
        order_date = date.today()
        
        # Create order object using the shipping_data dictionary
        new_order = Orders(
            orderid=None,  # Will be set by insert_order function
            customerid=customer_id,
            employeeid=employee_id,
            orderdate=order_date,
            requireddate=shipping_data.get('required_date'),
            shippeddate=shipping_data.get('shipped_date'),
            shipperid=shipping_data.get('shipper_id'),
            freight=shipping_data.get('freight', 0.0),
            shipname=shipping_data.get('ship_name'),
            shipaddress=shipping_data.get('ship_address'),
            shipcity=shipping_data.get('ship_city'),
            shipregion=shipping_data.get('ship_region'),
            shippostalcode=shipping_data.get('ship_postal_code'),
            shipcountry=shipping_data.get('ship_country')
        )
        
        # Insert order header
        new_order_id = insert_order(new_order)
        if new_order_id is None:
            return (False, "Erro: Falha ao inserir o cabeçalho do pedido.")
        
        # Process each order item
        for item in items_data:
            product_name = item.get('product_name')
            quantity = item.get('quantity', 1)
            discount = item.get('discount', 0.0)
            
            # Get product ID and price
            product_info = find_product_id_and_price_by_name(product_name)
            if product_info is None:
                return (False, f"Erro: Produto '{product_name}' não encontrado.")
                
            product_id, unit_price = product_info
            
            # Create and insert order detail
            order_detail = OrderDetails(
                orderid=new_order_id,
                productid=product_id,
                unitprice=unit_price,
                quantity=quantity,
                discount=discount
            )
            
            insert_order_detail(order_detail)
            # Note: The specifications don't require error handling for insert_order_detail
        
        # Return success result
        return (True, f"Pedido {new_order_id} inserido com sucesso!")
    
    @staticmethod
    def get_order_report(order_id: int) -> tuple[bool, dict | str]:
        """
        Obtém um relatório completo de um pedido específico.
        
        Args:
            order_id (int): ID do pedido a ser consultado
            
        Returns:
            tuple[bool, dict | str]: Tupla contendo:
                - status de sucesso (bool)
                - dados do pedido (dict) ou mensagem de erro (str)
        """
        # Validar entrada
        if not isinstance(order_id, int) or order_id <= 0:
            return (False, "Erro: ID do pedido deve ser um número inteiro positivo.")
        
        # Chamar a função do DAO
        order_data = find_order_with_details(order_id)
        
        # Verificar o resultado
        if order_data is None:
            return (False, f"Erro: Pedido com ID {order_id} não encontrado.")
            
        return (True, order_data)
    
    @staticmethod
    def get_employee_ranking_report(start_date: date, end_date: date) -> tuple[bool, list | str]:
        """
        Obtém um relatório de ranking de vendas dos funcionários em um período específico.
        
        Args:
            start_date (date): Data de início do período
            end_date (date): Data de fim do período
            
        Returns:
            tuple[bool, list | str]: Tupla contendo:
                - status de sucesso (bool)
                - lista de ranking (list) ou mensagem de erro (str)
        """
        # Validar entradas
        if not isinstance(start_date, date):
            return (False, "Erro: A data inicial deve ser um objeto date.")
            
        if not isinstance(end_date, date):
            return (False, "Erro: A data final deve ser um objeto date.")
            
        if start_date > end_date:
            return (False, "Erro: A data inicial não pode ser posterior à data final.")
        
        # Chamar a função do DAO
        ranking_data = get_employee_sales_ranking(start_date, end_date)
        
        # Verificar o resultado
        if ranking_data is None:
            return (False, "Erro: Ocorreu um erro ao gerar o ranking de vendas.")
            
        if len(ranking_data) == 0:
            return (True, "Nenhum pedido encontrado no período especificado.")
            
        return (True, ranking_data)
