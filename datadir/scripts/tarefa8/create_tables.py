import psycopg2
import os
from conecta import *

# Configurações do banco de dados
db_name = 'test_files'

# Criação das tabelas
def create_tables():
    conn = establish_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DROP TABLE IF EXISTS tabela_arquivo1;
        CREATE TABLE tabela_arquivo1 (
            id serial PRIMARY KEY,
            content bytea
        );
    """)
    cursor.execute("""
        DROP TABLE IF EXISTS tabela_arquivo2;
        CREATE TABLE tabela_arquivo2 (
            id serial PRIMARY KEY,
            content bytea
        );
    """)
    cursor.execute("""
        DROP TABLE IF EXISTS tabela_arquivo3;
        CREATE TABLE tabela_arquivo3 (
            id serial PRIMARY KEY,
            content bytea
        );
    """)
    cursor.execute("""
        DROP TABLE IF EXISTS tabela_arquivo4;
        CREATE TABLE tabela_arquivo4 (
            id serial PRIMARY KEY,
            content bytea
        );
    """)
    cursor.close()
    conn.commit()
    conn.close()
    print("Tabelas criadas com sucesso!")

# Execução das etapas
create_tables()