# Sistema de Pedidos Northwind

Sistema de gestão de pedidos baseado no banco de dados Northwind, implementando dois métodos diferentes de acesso ao banco de dados (psycopg e SQLAlchemy).

## Visão Geral

Este projeto implementa um sistema de linha de comando para gerenciar pedidos no banco de dados Northwind. O sistema permite:

- Criar novos pedidos
- Consultar relatórios de pedidos específicos
- Gerar ranking de vendas por funcionário em um período
- Demonstrar vulnerabilidades de SQL Injection

O projeto utiliza uma arquitetura MVC (Model-View-Controller) e oferece duas implementações diferentes para acesso ao banco de dados:
- **psycopg**: Usando queries SQL diretamente
- **SQLAlchemy**: Usando ORM (Object-Relational Mapping)

## Requisitos

- Python 3.10+
- PostgreSQL com banco de dados Northwind
- Pacotes Python listados em `requirements.txt`

## Instalação

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/pratica_northwind.git
cd pratica_northwind
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate.bat  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```
Edite o arquivo `.env` com as credenciais do seu banco de dados PostgreSQL.

## Estrutura do Projeto

```
pratica_northwind/
│
├── app/                  # Código da aplicação
│   ├── controller/       # Controladores
│   │   └── order_controller.py  # Controlador de pedidos
│   │
│   ├── dao/              # Data Access Objects
│   │   ├── base_dao.py          # Configuração de conexão
│   │   ├── psycopg_dao.py       # Implementação com psycopg
│   │   ├── sqlalchemy_dao.py    # Implementação com SQLAlchemy
│   │   └── vulnerable_psycopg.py # Versão vulnerável para demonstração
│   │
│   ├── model/            # Modelos de dados
│   │   ├── psycopg_model.py     # Classes de modelo para psycopg
│   │   └── orm_model.py         # Modelos ORM para SQLAlchemy
│   │
│   └── view/             # Interfaces de usuário
│       ├── cli_view.py          # Interface de linha de comando
│       └── slq_injection.py     # Demonstração de SQL Injection
│
├── main.py               # Ponto de entrada da aplicação
├── .env                  # Variáveis de ambiente (não versionado)
├── .env.example          # Exemplo de variáveis de ambiente
├── requirements.txt      # Dependências do projeto
└── README.md             # Este arquivo
```

## Arquitetura

O projeto segue o padrão MVC (Model-View-Controller):

- **Model**: Representa as entidades do banco de dados (Orders, OrderDetails, etc.)
  - `psycopg_model.py`: Classes de entidade para uso com psycopg
  - `orm_model.py`: Classes ORM para SQLAlchemy com mapeamento de tabelas

- **View**: Interface de linha de comando para interação com o usuário
  - `cli_view.py`: Funções para exibir menus, coletar inputs e mostrar resultados
  - `slq_injection.py`: Interface para demonstrar vulnerabilidades

- **Controller**: Lógica de negócios para processamento de operações
  - `order_controller.py`: Coordena operações entre DAO e View para pedidos

- **DAO**: Camada de acesso a dados com duas implementações
  - `psycopg_dao.py`: Implementação usando SQL direto via psycopg2
  - `sqlalchemy_dao.py`: Implementação usando ORM (SQLAlchemy)
  - `vulnerable_psycopg.py`: Implementação propositalmente vulnerável

## Funcionalidades

### 1. Criação de Pedidos

Cria um novo pedido com:
- Dados do cliente
- Dados do funcionário
- Informações de envio
- Itens do pedido (produto, quantidade, desconto)

### 2. Relatório de Pedido

Consulta os detalhes de um pedido específico através do ID:
- Informações básicas do pedido
- Cliente e funcionário responsável
- Lista de produtos, quantidades e valores

### 3. Ranking de Vendas por Funcionário

Gera um relatório de vendas por funcionário em um período específico:
- Nome do funcionário
- Quantidade de pedidos
- Valor total de vendas

### 4. Demonstração de SQL Injection

Mostra como consultas vulneráveis podem ser exploradas, demonstrando práticas que devem ser evitadas.

## Uso

Execute a aplicação:

```bash
python main.py
```

O sistema apresentará um menu com as seguintes opções:
1. Inserir novo pedido
2. Demonstrar SQL Injection
3. Relatório de Pedido
4. Ranking de Vendas por Funcionário
5. Sair

Para cada operação que acessa o banco de dados, você poderá escolher qual método utilizar:
1. psycopg (SQL direto)
2. sqlalchemy (ORM)

## Implementações de Acesso a Dados

### psycopg

Utiliza o driver psycopg2 para executar queries SQL diretamente no banco de dados PostgreSQL. Características:
- Execução direta de consultas SQL
- Parametrização para prevenir injeção SQL
- Mapeamento manual entre resultados SQL e objetos Python

### SQLAlchemy

Utiliza o ORM SQLAlchemy para mapear objetos Python para tabelas do banco de dados. Características:
- Mapeamento automático entre objetos e tabelas
- Consultas usando API de objetos em vez de SQL direto
- Abstração sobre detalhes de banco de dados

## Modelos de Dados

O sistema utiliza os seguintes modelos principais:

- **Orders**: Representa o cabeçalho de um pedido
  - Contém dados gerais como cliente, funcionário e informações de envio
  
- **OrderDetails**: Representa os itens de um pedido
  - Contém referências aos produtos, quantidades, preços e descontos

Ambos os modelos estão implementados em duas versões:
- Versão psycopg com classes simples (em `psycopg_model.py`)
- Versão ORM com mapeamento SQLAlchemy (em `orm_model.py`)

## Segurança

O projeto implementa:
- Uso de parâmetros em consultas SQL para prevenir injeções SQL (na versão segura)
- Demonstração de vulnerabilidades SQL (propositalmente, para fins educacionais)

A aplicação inclui dois tipos de implementação para comparação:
- **Implementação segura**: Usa parametrização SQL (psycopg) ou ORM (SQLAlchemy)
- **Implementação vulnerável**: Demonstra consultas SQL vulneráveis (para fins didáticos)
