from app.dao.psycopg_dao import (
    find_customer_id_by_name,
    find_employee_id_by_name,
    find_product_id_and_price_by_name,
    insert_order,
    insert_order_detail,
    find_order_with_details,
    get_employee_sales_ranking
)
from app.model.psycopg_model import Orders as PsycopgOrders, OrderDetails as PsycopgOrderDetails

# Importações para SQLAlchemy
from app.dao.sqlalchemy_dao import (
    find_customer_id_by_name as sqlalchemy_find_customer_id_by_name,
    find_employee_id_by_name as sqlalchemy_find_employee_id_by_name,
    find_product_id_and_price_by_name as sqlalchemy_find_product_id_and_price_by_name,
    insert_order as sqlalchemy_insert_order,
    insert_order_detail as sqlalchemy_insert_order_detail,
    find_order_with_details as sqlalchemy_find_order_with_details,
    get_employee_sales_ranking as sqlalchemy_get_employee_sales_ranking
)
from app.model.orm_model import Orders as SqlalchemyOrders, OrderDetails as SqlalchemyOrderDetails

from datetime import date

class OrderController:
    @staticmethod
    def create_new_order_psycopg(
        customer_name: str,
        employee_first_name: str, 
        employee_last_name: str,
        items_data: list[dict],
        shipping_data: dict = None
    ) -> tuple[bool, str]:
        """
        Cria um novo pedido com seus detalhes usando psycopg.
        
        Args:
            customer_name: Nome da empresa cliente
            employee_first_name: Nome do funcionário 
            employee_last_name: Sobrenome do funcionário
            items_data: Lista de dicionários com detalhes dos produtos
                Cada dicionário contém: 'product_name', 'quantity', 'discount'
            shipping_data: Dicionário com informações de envio
                Pode conter: 'shipper_id', 'freight', 'ship_name', 'ship_address',
                'ship_city', 'ship_region', 'ship_postal_code', 'ship_country'
        
        Returns:
            tuple[bool, str]: Tupla contendo status de sucesso e mensagem
        """
        if shipping_data is None:
            shipping_data = {}
        
        customer_id = find_customer_id_by_name(customer_name)
        if customer_id is None:
            return (False, "Erro: Cliente não encontrado.")
        
        employee_id = find_employee_id_by_name(employee_first_name, employee_last_name)
        if employee_id is None:
            return (False, "Erro: Funcionário não encontrado.")
        
        order_date = date.today()
        
        new_order = PsycopgOrders(
            orderid=None,
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
        
        new_order_id = insert_order(new_order)
        if new_order_id is None:
            return (False, "Erro: Falha ao inserir o cabeçalho do pedido.")
        
        for item in items_data:
            product_name = item.get('product_name')
            quantity = item.get('quantity', 1)
            discount = item.get('discount', 0.0)
            
            product_info = find_product_id_and_price_by_name(product_name)
            if product_info is None:
                return (False, f"Erro: Produto '{product_name}' não encontrado.")
                
            product_id, unit_price = product_info
            
            order_detail = PsycopgOrderDetails(
                orderid=new_order_id,
                productid=product_id,
                unitprice=unit_price,
                quantity=quantity,
                discount=discount
            )
            
            insert_order_detail(order_detail)
        
        return (True, f"Pedido {new_order_id} inserido com sucesso!")
    
    @staticmethod
    def create_new_order_sqlalchemy(
        customer_name: str,
        employee_first_name: str, 
        employee_last_name: str,
        items_data: list[dict],
        shipping_data: dict = None
    ) -> tuple[bool, str]:
        """
        Cria um novo pedido com seus detalhes usando SQLAlchemy.
        
        Args:
            customer_name: Nome da empresa cliente
            employee_first_name: Nome do funcionário
            employee_last_name: Sobrenome do funcionário
            items_data: Lista de dicionários com detalhes dos produtos
                Cada dicionário contém: 'product_name', 'quantity', 'discount'
            shipping_data: Dicionário com informações de envio
                Pode conter: 'shipper_id', 'freight', 'ship_name', 'ship_address',
                'ship_city', 'ship_region', 'ship_postal_code', 'ship_country'
        
        Returns:
            tuple[bool, str]: Tupla contendo status de sucesso e mensagem
        """
        if shipping_data is None:
            shipping_data = {}
        
        customer_id = sqlalchemy_find_customer_id_by_name(customer_name)
        if customer_id is None:
            return (False, "Erro: Cliente não encontrado.")
        
        employee_id = sqlalchemy_find_employee_id_by_name(employee_first_name, employee_last_name)
        if employee_id is None:
            return (False, "Erro: Funcionário não encontrado.")
        
        order_date = date.today()
        
        new_order = SqlalchemyOrders(
            orderid=None,
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
        
        order_result = sqlalchemy_insert_order(new_order)
        if order_result is None:
            return (False, "Erro: Falha ao inserir o cabeçalho do pedido.")
        
        new_order_id = order_result.orderid
        
        for item in items_data:
            product_name = item.get('product_name')
            quantity = item.get('quantity', 1)
            discount = item.get('discount', 0.0)
            
            product_info = sqlalchemy_find_product_id_and_price_by_name(product_name)
            if product_info is None:
                return (False, f"Erro: Produto '{product_name}' não encontrado.")
                
            product_id, unit_price = product_info
            
            order_detail = SqlalchemyOrderDetails(
                orderid=new_order_id,
                productid=product_id,
                unitprice=unit_price,
                quantity=quantity,
                discount=discount
            )
            
            sqlalchemy_insert_order_detail(order_detail)
        
        return (True, f"Pedido {new_order_id} inserido com sucesso!")
    
    @staticmethod
    def get_order_report_psycopg(order_id: int) -> tuple[bool, dict | str]:
        """
        Obtém um relatório completo de um pedido específico usando psycopg.
        
        Args:
            order_id (int): ID do pedido a ser consultado
            
        Returns:
            tuple[bool, dict | str]: Tupla contendo:
                - status de sucesso (bool)
                - dados do pedido (dict) ou mensagem de erro (str)
        """
        if not isinstance(order_id, int) or order_id <= 0:
            return (False, "Erro: ID do pedido deve ser um número inteiro positivo.")
        
        order_data = find_order_with_details(order_id)
        
        if order_data is None:
            return (False, f"Erro: Pedido com ID {order_id} não encontrado.")
            
        return (True, order_data)
    
    @staticmethod
    def get_order_report_sqlalchemy(order_id: int) -> tuple[bool, dict | str]:
        """
        Obtém um relatório completo de um pedido específico usando SQLAlchemy.
        
        Args:
            order_id (int): ID do pedido a ser consultado
            
        Returns:
            tuple[bool, dict | str]: Tupla contendo:
                - status de sucesso (bool)
                - dados do pedido (dict) ou mensagem de erro (str)
        """
        if not isinstance(order_id, int) or order_id <= 0:
            return (False, "Erro: ID do pedido deve ser um número inteiro positivo.")
        
        order_data = sqlalchemy_find_order_with_details(order_id)
        
        if order_data is None:
            return (False, f"Erro: Pedido com ID {order_id} não encontrado.")
            
        return (True, order_data)
    
    @staticmethod
    def get_employee_ranking_report_psycopg(start_date: date, end_date: date) -> tuple[bool, list | str]:
        """
        Obtém um relatório de ranking de vendas dos funcionários em um período específico usando psycopg.
        
        Args:
            start_date (date): Data de início do período
            end_date (date): Data de fim do período
            
        Returns:
            tuple[bool, list | str]: Tupla contendo:
                - status de sucesso (bool)
                - lista de ranking (list) ou mensagem de erro (str)
        """
        if not isinstance(start_date, date):
            return (False, "Erro: A data inicial deve ser um objeto date.")
            
        if not isinstance(end_date, date):
            return (False, "Erro: A data final deve ser um objeto date.")
            
        if start_date > end_date:
            return (False, "Erro: A data inicial não pode ser posterior à data final.")
        
        ranking_data = get_employee_sales_ranking(start_date, end_date)
        
        if ranking_data is None:
            return (False, "Erro: Ocorreu um erro ao gerar o ranking de vendas.")
            
        if len(ranking_data) == 0:
            return (True, "Nenhum pedido encontrado no período especificado.")
            
        return (True, ranking_data)
    
    @staticmethod
    def get_employee_ranking_report_sqlalchemy(start_date: date, end_date: date) -> tuple[bool, list | str]:
        """
        Obtém um relatório de ranking de vendas dos funcionários em um período específico usando SQLAlchemy.
        
        Args:
            start_date (date): Data de início do período
            end_date (date): Data de fim do período
            
        Returns:
            tuple[bool, list | str]: Tupla contendo:
                - status de sucesso (bool)
                - lista de ranking (list) ou mensagem de erro (str)
        """
        if not isinstance(start_date, date):
            return (False, "Erro: A data inicial deve ser um objeto date.")
            
        if not isinstance(end_date, date):
            return (False, "Erro: A data final deve ser um objeto date.")
            
        if start_date > end_date:
            return (False, "Erro: A data inicial não pode ser posterior à data final.")
        
        ranking_data = sqlalchemy_get_employee_sales_ranking(start_date, end_date)
        
        if ranking_data is None:
            return (False, "Erro: Ocorreu um erro ao gerar o ranking de vendas.")
            
        if len(ranking_data) == 0:
            return (True, "Nenhum pedido encontrado no período especificado.")
            
        return (True, ranking_data)
    