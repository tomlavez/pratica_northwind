import psycopg2
from app.dao.base_dao import get_db_connection # Para pegar a conexão
from app.model.driver_model import Orders, OrderDetails, Customers, Employees, Products # Importe os modelos adaptados que serão usados
from datetime import date # Se for lidar com datas

def _find_next_order_id() -> int | None:
    """
    Busca o próximo ID para o pedido, visto que o ID não é auto incrementado no Banco de Dados
    """
    session = None
    next_order_id = None
    
    try:
        session = get_db_connection()
        if session:
            with session.cursor() as cursor:
                cursor.execute("SELECT MAX(orderid) FROM northwind.orders")
                max_id_result = cursor.fetchone()
                if max_id_result and max_id_result[0] is not None:
                    next_order_id = max_id_result[0] + 1
                else:
                    # ID inicial se tabela vazia
                    next_order_id = 1
        else:
            return None

    except psycopg2.Error as e:
        print(f"Error ao buscar próximo ID para o pedido: {e}")
    finally:
        if session:
            session.close()
    return next_order_id

def find_customer_id_by_name(company_name: str) -> str | None:
    """
    Busca o ID de um cliente pelo nome da empresa

    Args:
        company_name (str): Nome da empresa do cliente

    Returns:
        str | None: ID do cliente ou None se não encontrado
    """
    session = None
    customer_id = None
    
    try:
        session = get_db_connection()
        if session:
            with session.cursor() as cursor:
                sql = f"SELECT customerid FROM northwind.customers WHERE companyname = '{company_name}'"
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    customer_id = result[0]
    
    except psycopg2.Error as e:
        print(f"Error ao buscar customer_id de '{company_name}': {e}")
    finally:
        if session:
            session.close()
    return customer_id

def find_employee_id_by_name(first_name: str, last_name: str) -> int | None:
    """
    Busca o ID de um funcionário pelo primeiro e último nome

    Args:
        first_name (str): Primeiro nome do funcionário
        last_name (str): Sobrenome do funcionário

    Returns:
        int | None: ID do funcionário ou None se não encontrado
    """
    session = None
    employee_id = None
    
    try:
        session = get_db_connection()
        if session:
            with session.cursor() as cursor:
                sql = f"SELECT employeeid FROM northwind.employees WHERE firstname = '{first_name}' AND lastname = '{last_name}'"
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    employee_id = result[0]
    
    except psycopg2.Error as e:
        print(f"Error ao buscar employee_id de '{first_name} {last_name}': {e}")
    finally:
        if session:
            session.close()
    return employee_id

def find_product_id_and_price_by_name(name: str) -> tuple[int, float] | None:
    """
    Busca o ID e preço unitário de um produto pelo nome

    Args:
        name (str): Nome do produto

    Returns:
        tuple[int, float] | None: Tupla contendo (productid, unitprice) ou None se não encontrado
    """
    session = None
    result_data = None
    
    try:
        session = get_db_connection()
        if session:
            with session.cursor() as cursor:
                sql = f"SELECT productid, unitprice FROM northwind.products WHERE productname = '{name}'"
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    product_id = result[0]
                    unit_price = float(result[1]) if result[1] is not None else 0.0
                    result_data = (product_id, unit_price)
    
    except psycopg2.Error as e:
        print(f"Error ao buscar produto com nome '{name}': {e}")
    finally:
        if session:
            session.close()
    return result_data

def insert_order(order: Orders) -> int | None:
    """
    Insere um novo pedido no banco

    Args:
        order (Orders): Objeto Orders contendo os dados do pedido

    Returns:
        int | None: ID do pedido ou None se falhar
    """
    session = None
    
    # Busca o próximo ID para o pedido, visto que o ID não é auto incrementado no Banco de Dados
    next_order_id = _find_next_order_id()
    if next_order_id is None:
        print("Erro ao buscar próximo ID para o pedido")
        return None

    try:
        session = get_db_connection()
        if session:
            with session.cursor() as cursor:
                sql = f"""
                INSERT INTO northwind.orders
                (orderid, customerid, employeeid, orderdate, requireddate, shippeddate, shipperid, freight, 
                shipname, shipaddress, shipcity, shipregion, shippostalcode, shipcountry)
                VALUES (
                    {next_order_id}, 
                    '{order.customerid}', 
                    {order.employeeid}, 
                    '{order.orderdate}', 
                    {f"'{order.requireddate}'" if order.requireddate else 'NULL'}, 
                    {f"'{order.shippeddate}'" if order.shippeddate else 'NULL'}, 
                    {order.shipperid if order.shipperid else 'NULL'}, 
                    {order.freight if order.freight else 0}, 
                    {f"'{order.shipname}'" if order.shipname else 'NULL'}, 
                    {f"'{order.shipaddress}'" if order.shipaddress else 'NULL'}, 
                    {f"'{order.shipcity}'" if order.shipcity else 'NULL'}, 
                    {f"'{order.shipregion}'" if order.shipregion else 'NULL'}, 
                    {f"'{order.shippostalcode}'" if order.shippostalcode else 'NULL'}, 
                    {f"'{order.shipcountry}'" if order.shipcountry else 'NULL'}
                );
                """
                cursor.execute(sql)
            session.commit()
            # Atualiza o objeto order com o ID gerado
            order.orderid = next_order_id
    
    except psycopg2.Error as e:
        print(f"Error ao inserir pedido: {e}")
        if session:
            session.rollback()
            return None

    finally:
        if session:
            session.close()
    return next_order_id

def insert_order_detail(detail: OrderDetails):
    """
    Insere um item de pedido no banco

    Args:
        detail (OrderDetails): Objeto OrderDetails contendo os dados do item
    """
    session = None
    
    try:
        session = get_db_connection()
        if session:
            with session.cursor() as cursor:
                # VULNERÁVEL: Usando f-string em vez de parâmetros
                sql = f"""
                INSERT INTO northwind.order_details
                (orderid, productid, unitprice, quantity, discount)
                VALUES (
                    {detail.orderid}, 
                    {detail.productid}, 
                    {detail.unitprice}, 
                    {detail.quantity}, 
                    {detail.discount}
                );
                """
                cursor.execute(sql)
            session.commit()
    
    except psycopg2.Error as e:
        print(f"Error ao inserir detalhe do pedido: {e}")
        if session:
            session.rollback()

    finally:
        if session:
            session.close()
