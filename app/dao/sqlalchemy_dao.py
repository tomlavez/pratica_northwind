from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from app.dao.base_dao import get_sql_alchemy_new_session
from app.model.orm_model import Customers, Employees, Products, Orders, OrderDetails
from typing import Optional, Tuple, List, Dict, Any
from datetime import date

def pattern(parameter) -> None:
    db: Session = get_sql_alchemy_new_session()
    try:
        db.commit()
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()
    return None

def find_customer_by_name(name: str) -> Optional[Customers]:
    """
    Busca um cliente pelo nome da empresa usando SQLAlchemy ORM.
    
    Args:
        name (str): Nome da empresa do cliente
        
    Returns:
        Optional[Customers]: Objeto Customers encontrado ou None se não encontrado
    """
    db: Session = get_sql_alchemy_new_session()
    customer = None
    try:
        # Buscar cliente pelo nome da empresa
        customer = db.query(Customers).filter(Customers.companyname == name).first()
        return customer
    except Exception as e:
        print(f"Error ao buscar cliente: {e}")
        return None
    finally:
        db.close()

def find_employee_by_name(first_name: str, last_name: str) -> Optional[Employees]:
    """
    Busca um funcionário pelo primeiro e último nome usando SQLAlchemy ORM.
    
    Args:
        first_name (str): Primeiro nome do funcionário
        last_name (str): Sobrenome do funcionário
        
    Returns:
        Optional[Employees]: Objeto Employees encontrado ou None se não encontrado
    """
    db: Session = get_sql_alchemy_new_session()
    employee = None
    try:
        # Buscar funcionário pelo primeiro e último nome
        employee = db.query(Employees).filter(
            Employees.firstname == first_name,
            Employees.lastname == last_name
        ).first()
        return employee
    except Exception as e:
        print(f"Error ao buscar funcionário: {e}")
        return None
    finally:
        db.close()

def find_product_by_name(name: str) -> Optional[Products]:
    """
    Busca um produto pelo nome usando SQLAlchemy ORM.
    
    Args:
        name (str): Nome do produto
        
    Returns:
        Optional[Products]: Objeto Products encontrado ou None se não encontrado
    """
    db: Session = get_sql_alchemy_new_session()
    product = None
    try:
        # Buscar produto pelo nome
        product = db.query(Products).filter(Products.productname == name).first()
        return product
    except Exception as e:
        print(f"Error ao buscar produto: {e}")
        return None
    finally:
        db.close()

def insert_order(order: Orders) -> Optional[Orders]:
    """
    Insere um novo pedido usando SQLAlchemy ORM.
    Como o banco não gera o ID automaticamente, é necessário calcular o próximo ID.
    
    Args:
        order (Orders): Objeto Orders com os dados do pedido
        
    Returns:
        Optional[Orders]: Objeto Orders com o ID gerado ou None se falhar
    """
    db: Session = get_sql_alchemy_new_session()
    try:
        # Calcular o próximo ID para o pedido
        max_id_result = db.query(func.max(Orders.orderid)).scalar()
        calculated_id = (max_id_result or 0) + 1  # Usar 11077 como base se não houver pedidos
        
        # Definir o ID no objeto antes de adicionar à sessão
        order.orderid = calculated_id
        
        # Adicionar o objeto à sessão e confirmar a inserção
        db.add(order)
        db.commit()
        
        # Atualizar o objeto com dados do banco (útil se houver defaults ou triggers)
        db.refresh(order)
        
        return order
    except Exception as e:
        print(f"Error ao inserir pedido: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def insert_order_detail(detail: OrderDetails) -> None:
    """
    Insere um detalhe de pedido usando SQLAlchemy ORM.
    
    Args:
        detail (OrderDetails): Objeto OrderDetails com os dados do item
    """
    db: Session = get_sql_alchemy_new_session()
    try:
        # Adicionar o objeto à sessão e confirmar a inserção
        db.add(detail)
        db.commit()
    except Exception as e:
        print(f"Error ao inserir detalhe do pedido: {e}")
        db.rollback()
    finally:
        db.close()

def find_order_with_details(order_id: int) -> Optional[Dict[str, Any]]:
    """
    Busca um pedido com todos os seus detalhes usando eager loading com joinedload.
    
    Args:
        order_id (int): ID do pedido a ser consultado
        
    Returns:
        Optional[Dict[str, Any]]: Dicionário com todas as informações do pedido ou None se não encontrado
    """
    db: Session = get_sql_alchemy_new_session()
    try:
        # Buscar o pedido com eager loading para todos os relacionamentos
        order = (
            db.query(Orders)
            .options(
                joinedload(Orders.customers),
                joinedload(Orders.employees),
                joinedload(Orders.order_details).joinedload(OrderDetails.products)
            )
            .filter(Orders.orderid == order_id)
            .first()
        )
        
        if not order:
            return None
            
        # Construir dicionário de retorno no mesmo formato que a versão do psycopg
        result = {
            'order_id': order.orderid,
            'order_date': order.orderdate,
            'customer_name': order.customers.companyname if order.customers else None,
            'employee_name': f"{order.employees.firstname} {order.employees.lastname}" if order.employees else None,
            'items': []
        }
        
        # Adicionar os itens do pedido
        total_order = 0.0
        for detail in order.order_details:
            product = detail.products
            unit_price = float(detail.unitprice) if detail.unitprice else 0.0
            quantity = detail.quantity or 0
            discount = float(detail.discount) if detail.discount else 0.0
            total_price = unit_price * quantity * (1 - discount)
            
            result['items'].append({
                'product_name': product.productname if product else 'Unknown',
                'quantity': quantity,
                'total_price': total_price
            })
            
            total_order += total_price
            
        result['total_order'] = total_order
        
        return result
        
    except Exception as e:
        print(f"Error ao buscar pedido com detalhes: {e}")
        return None
    finally:
        db.close()

def get_employee_sales_ranking(start_date: date, end_date: date) -> Optional[List[Dict[str, Any]]]:
    """
    Calcula o ranking de vendas dos funcionários em um período específico.
    
    Args:
        start_date (date): Data de início do período
        end_date (date): Data de fim do período
        
    Returns:
        Optional[List[Dict[str, Any]]]: Lista de dicionários com ranking de vendas ou None em caso de erro
    """
    db: Session = get_sql_alchemy_new_session()
    try:
        # Query para calcular o ranking de vendas
        # Convertendo date para datetime para comparação com os campos DateTime do modelo
        start_datetime = date(start_date.year, start_date.month, start_date.day)
        end_datetime = date(end_date.year, end_date.month, end_date.day)
        
        result_rows = (
            db.query(
                Employees.firstname,
                Employees.lastname,
                func.count(func.distinct(Orders.orderid)).label('total_orders'),
                func.sum(
                    OrderDetails.quantity * OrderDetails.unitprice * (1 - OrderDetails.discount)
                ).label('total_value')
            )
            .join(Orders, Orders.employeeid == Employees.employeeid)
            .join(OrderDetails, OrderDetails.orderid == Orders.orderid)
            .filter(Orders.orderdate >= start_datetime)
            .filter(Orders.orderdate <= end_datetime)
            .group_by(Employees.employeeid, Employees.firstname, Employees.lastname)
            .order_by(desc('total_value'))
            .all()
        )
        
        if not result_rows:
            return []
            
        # Converter os resultados para o formato esperado
        ranking = []
        for row in result_rows:
            employee_name = f"{row.firstname} {row.lastname}"
            total_orders = row.total_orders
            total_value = float(row.total_value) if row.total_value is not None else 0.0
            
            ranking.append({
                'employee_name': employee_name,
                'total_orders': total_orders,
                'total_value': total_value
            })
            
        return ranking
        
    except Exception as e:
        print(f"Error ao calcular ranking de vendas: {e}")
        return None
    finally:
        db.close()
        
# Funções auxiliares para compatibilidade com o código existente

def find_customer_id_by_name(company_name: str) -> Optional[str]:
    """
    Busca o ID de um cliente pelo nome da empresa (função de compatibilidade)
    
    Args:
        company_name (str): Nome da empresa do cliente
        
    Returns:
        Optional[str]: ID do cliente ou None se não encontrado
    """
    customer = find_customer_by_name(company_name)
    return customer.customerid if customer else None

def find_employee_id_by_name(first_name: str, last_name: str) -> Optional[int]:
    """
    Busca o ID de um funcionário pelo nome (função de compatibilidade)
    
    Args:
        first_name (str): Primeiro nome do funcionário
        last_name (str): Sobrenome do funcionário
        
    Returns:
        Optional[int]: ID do funcionário ou None se não encontrado
    """
    employee = find_employee_by_name(first_name, last_name)
    return employee.employeeid if employee else None

def find_product_id_and_price_by_name(name: str) -> Optional[Tuple[int, float]]:
    """
    Busca o ID e preço de um produto pelo nome (função de compatibilidade)
    
    Args:
        name (str): Nome do produto
        
    Returns:
        Optional[Tuple[int, float]]: Tupla com ID e preço do produto ou None se não encontrado
    """
    product = find_product_by_name(name)
    if product and product.unitprice is not None:
        return (product.productid, float(product.unitprice))
    return None