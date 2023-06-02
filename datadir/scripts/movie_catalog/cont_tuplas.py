from conecta import *

def execute_query(c,query,table):
    # Estabelecer conexão
    conn = c

    try:
        # Criar um cursor para executar comandos SQL
        cur = conn.cursor()

        # Executar a consulta
        cur.execute(query)

        # Obter o resultado da consulta
        result = cur.fetchone()

        # Imprimir o resultado
        print("Total de tuplas na tabela " + table +":")
        print(result[0])  # A coluna de contagem estará no índice 0

        # Fechar o cursor
        cur.close()

    except psycopg2.Error as e:
        print("Erro ao executar a consulta:", e)

    finally:
        # Fechar a conexão
        conn.close()