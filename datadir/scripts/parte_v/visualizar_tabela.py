import psycopg2
from conecta import *
from cont_tuplas import *


conn = establish_connection()
cursor = conn.cursor()

# Nome da tabela que deseja visualizar
nome_tabela = "Assentos"

# Execute a consulta SQL para selecionar todas as linhas da tabela
cursor.execute(f"SELECT * FROM {nome_tabela}")

# Recupere os resultados da consulta
tuplas = cursor.fetchall()

# Exiba o conteúdo das tuplas
for tupla in tuplas:
    print(tupla)

# Encerre a conexão com o banco de dados
cursor.close()
conn.close()