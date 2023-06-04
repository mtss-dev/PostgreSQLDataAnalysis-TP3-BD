from conecta import *

# Estabelecer conexão com o banco de dados
conn = establish_connection()

# Função para executar uma consulta e exibir o resultado do comando EXPLAIN
def execute_explain_query(query):
    cursor = conn.cursor()
    cursor.execute("EXPLAIN " + query)
    result = cursor.fetchall()
    for row in result:
        print(row[0])
    print()

print("\nConsulta 1: SELECT title FROM movie WHERE votes >= (SELECT MAX(votes) FROM movie);\n")
query1 = "SELECT title FROM movie WHERE votes >= (SELECT MAX(votes) FROM movie);"
execute_explain_query(query1)

print("-----------------------------------------------------------------------------------------")

print("\nConsulta 2: SELECT title FROM movie WHERE votes >= ALL (SELECT votes FROM movie);\n")
query2 = "SELECT title FROM movie WHERE votes >= ALL (SELECT votes FROM movie);"
execute_explain_query(query2)

# Fechar a conexão com o banco de dados
conn.close()