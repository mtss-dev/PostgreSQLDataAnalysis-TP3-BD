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

print("\nConsulta 1: SELECT title FROM movie WHERE title LIKE 'I%';\n")
query1 = "SELECT title FROM movie WHERE title LIKE 'I%';"
execute_explain_query(query1)

print("-----------------------------------------------------------------------------------------")

print("\nConsulta 2: SELECT title FROM movie WHERE substr(title, 1, 1) = 'I';\n")
query2 = "SELECT title FROM movie WHERE substr(title, 1, 1) = 'I';"
execute_explain_query(query2)

print("-----------------------------------------------------------------------------------------")

print("\nConsulta 3: SELECT title FROM movie WHERE title LIKE '%A'; \n")
query3 = "SELECT title FROM movie WHERE title LIKE '%A'; "
execute_explain_query(query3)

# Fechar a conexão com o banco de dados
conn.close()