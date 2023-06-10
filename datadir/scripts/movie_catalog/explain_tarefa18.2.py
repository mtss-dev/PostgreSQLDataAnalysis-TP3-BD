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

# Consulta em SQL sobre o atributo VOTES da tabela MOVIE que recupera um número grande de tuplas (>80% das tuplas).
print("\nConsulta: SELECT * FROM movie WHERE votes > 1 LIMIT (1844 * 0.90)\n")
query = "SELECT * FROM movie WHERE votes > 1 LIMIT (1844 * 0.90)"
execute_explain_query(query)

# Fechar a conexão com o banco de dados
conn.close()