import psycopg2
from app.dao.base_dao import get_db_connection
from app.model.psycopg_model import Orders, OrderDetails
from datetime import date

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
    sql = """
        SELECT customerid
        FROM northwind.customers
        WHERE companyname = %s
        """
    
    try:
        session = get_db_connection()
        if session:
            with session.cursor() as cursor:
                cursor.execute(sql, (company_name,))
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
    sql = """
        SELECT employeeid
        FROM northwind.employees
        WHERE firstname = %s AND lastname = %s
        """
    
    try:
        session = get_db_connection()
        if session:
            with session.cursor() as cursor:
                cursor.execute(sql, (first_name, last_name))
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
    sql = """
        SELECT productid, unitprice
        FROM northwind.products
        WHERE productname = %s
        """
    
    try:
        session = get_db_connection()
        if session:
            with session.cursor() as cursor:
                cursor.execute(sql, (name,))
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

    sql = """
        INSERT INTO northwind.orders
        (orderid, customerid, employeeid, orderdate, requireddate, shippeddate, shipperid, freight, shipname, shipaddress, shipcity, shipregion, shippostalcode, shipcountry)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
    
    params = (
        next_order_id,
        order.customerid,
        order.employeeid,
        order.orderdate,
        order.requireddate,
        order.shippeddate,
        order.shipperid,
        order.freight,
        order.shipname,
        order.shipaddress,
        order.shipcity,
        order.shipregion,
        order.shippostalcode,
        order.shipcountry
    )

    try:
        session = get_db_connection()
        if session:
            with session.cursor() as cursor:
                cursor.execute(sql, params)
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
    sql = """
        INSERT INTO northwind.order_details
        (orderid, productid, unitprice, quantity, discount)
        VALUES (%s, %s, %s, %s, %s);
        """
    
    params = (
        detail.orderid,
        detail.productid,
        detail.unitprice,
        detail.quantity,
        detail.discount
    )

    try:
        session = get_db_connection()
        if session:
            with session.cursor() as cursor:
                cursor.execute(sql, params)
            session.commit()
    
    except psycopg2.Error as e:
        print(f"Error ao inserir detalhe do pedido: {e}")
        if session:
            session.rollback()

    finally:
        if session:
            session.close()

def find_order_with_details(order_id: int) -> dict | None:
    """
    Busca todos os detalhes do pedido, incluindo informações do cliente, funcionário e itens
    
    Args:
        order_id (int): ID do pedido a ser pesquisado
        
    Returns:
        dict | None: Dicionário com todas as informações do pedido ou None se não encontrado
    """
    session = None
    result = None
    
    try:
        session = get_db_connection()
        if not session:
            return None
            
        with session.cursor() as cursor:
            sql = """
            SELECT 
                o.orderid,
                o.orderdate,
                c.companyname AS customer_name,
                e.firstname || ' ' || e.lastname AS employee_name
            FROM northwind.orders o
            INNER JOIN northwind.customers c ON o.customerid = c.customerid
            INNER JOIN northwind.employees e ON o.employeeid = e.employeeid
            WHERE o.orderid = %s
            """
            
            cursor.execute(sql, (order_id,))
            header_row = cursor.fetchone()
            
            if not header_row:
                return None
            
            result = {
                'order_id': header_row[0],
                'order_date': header_row[1],
                'customer_name': header_row[2],
                'employee_name': header_row[3],
                'items': []
            }

            sql = """
            SELECT 
                p.productname AS product_name,
                od.quantity,
                od.unitprice,
                od.discount
            FROM northwind.order_details od
            INNER JOIN northwind.products p ON od.productid = p.productid
            WHERE od.orderid = %s
            """
            
            cursor.execute(sql, (order_id,))
            items_rows = cursor.fetchall()
            
            for item in items_rows:
                result['items'].append({
                    'product_name': item[0],
                    'quantity': item[1],
                    'total_price': float(item[1] * item[2] * (1 - item[3])),
                })
                
            # Calcular o total do pedido
            total_order = sum(item['total_price'] for item in result['items'])
            result['total_order'] = total_order
            
    except psycopg2.Error as e:
        print(f"Erro ao buscar detalhes do pedido {order_id}: {e}")
        return None
        
    finally:
        if session:
            session.close()
            
    return result

def get_employee_sales_ranking(start_date, end_date) -> list | None:
    """
    Calcula o ranking de vendas dos funcionários em um período específico.
    
    Args:
        start_date: Data de início do período (inclusive)
        end_date: Data de fim do período (inclusive)
        
    Returns:
        list | None: Lista de dicionários com ranking de vendas ou None em caso de erro
    """
    session = None
    result = None
    
    try:
        session = get_db_connection()
        if not session:
            return None
            
        with session.cursor() as cursor:
            sql = """
            SELECT 
                e.firstname || ' ' || e.lastname AS employee_name,
                COUNT(DISTINCT o.orderid) AS total_orders,
                ROUND(SUM(od.quantity * od.unitprice * (1 - od.discount))::numeric, 2) AS total_value
            FROM northwind.employees e
            INNER JOIN northwind.orders o ON e.employeeid = o.employeeid
            INNER JOIN northwind.order_details od ON o.orderid = od.orderid
            WHERE o.orderdate BETWEEN %s AND %s
            GROUP BY e.employeeid, e.firstname, e.lastname
            ORDER BY total_value DESC
            """
            
            cursor.execute(sql, (start_date, end_date))
            rows = cursor.fetchall()
            
            if not rows:
                # Retorna lista vazia se não encontrar registros no período
                return []
                
            result = []
            for row in rows:
                result.append({
                    'employee_name': row[0],
                    'total_orders': row[1],
                    'total_value': float(row[2]) if row[2] is not None else 0.0
                })
                
    except psycopg2.Error as e:
        print(f"Erro ao calcular ranking de vendas: {e}")
        return None
        
    finally:
        if session:
            session.close()
            
    return result
    