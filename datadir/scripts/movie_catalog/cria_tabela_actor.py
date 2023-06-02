from conecta import *
from cont_tuplas import *
import sqlparse

conn = establish_connection()

# Abrir um cursor para executar comandos SQL
cur = conn.cursor()

# Ler o arquivo .sql
with open("../sqls/actor.sql", "r") as file:
    # Ler os comandos SQL do arquivo
    sql_commands = file.read()

    # Dividir os comandos SQL corretamente usando sqlparse
    statements = sqlparse.split(sql_commands)

    # Executar cada comando SQL na lista
    for statement in statements:
        try:
            # Remover espaços em branco adicionais
            statement = statement.strip()

            # Se o comando não estiver vazio
            if statement:
                # Executar o comando SQL
                cur.execute(statement)

                # Confirmar as alterações
                conn.commit()

        except Exception as e:
            # Se ocorrer algum erro, imprimir a mensagem de erro
            print("Ocorreu um erro ao executar o comando SQL:")
            print(statement)
            print(e)

# Imprimir a quantidade de tuplas na tabela
execute_query(conn, "SELECT COUNT(*) FROM actor", "actor")

# Fechar o cursor e a conexão
cur.close()
conn.close()