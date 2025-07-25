import psycopg2
from psycopg2 import sql

# Database configuration
DB_CONFIG = {
    'host': 'database',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'port':  '5432'
}

# Database table columns
COLUMNS = [
    'nome', 'nome_social', 'email', 'idade', 'cep', 
    'numero', 'rua', 'bairro', 'cidade', 'estado', 
    'pais', 'profissao'
]

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn


def create_table():
    conn = get_db_connection()
    cur = conn.cursor()

    create_table_query = sql.SQL("""
    CREATE TABLE IF NOT EXISTS pessoas (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        nome_social VARCHAR(255),
        email VARCHAR(255),
        idade INTEGER,
        cep VARCHAR(20),
        numero VARCHAR(20),
        rua VARCHAR(255),
        bairro VARCHAR(255),
        cidade VARCHAR(255),
        estado VARCHAR(255),
        pais VARCHAR(255),
        profissao VARCHAR(255)
    )
    """)

    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()