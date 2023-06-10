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
    cursor.close()

print("\nConsulta 1: SELECT title FROM movie WHERE votes > (SELECT votes FROM movie WHERE title = 'Star Wars');\n")
query1 = "SELECT title FROM movie WHERE votes > (SELECT votes FROM movie WHERE title = 'Star Wars');"
execute_explain_query(query1)

print("-----------------------------------------------------------------------------------------")

print("\nConsulta 2: SELECT m1.title FROM movie m1, movie m2 WHERE m1.votes > m2.votes AND m2.title = 'Star Wars';\n")
query2 = "SELECT m1.title FROM movie m1, movie m2 WHERE m1.votes > m2.votes AND m2.title = 'Star Wars';"
execute_explain_query(query2)

# Fechar a conexão com o banco de dados
conn.close()