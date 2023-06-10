from conecta import *

# Estabelecer conexão com o banco de dados
conn = establish_connection()

cur = conn.cursor()
# Consulta SQL para recuperar os metadados dos índices
query = """
    SELECT
        i.relname AS "Nome do Índice",
        t.relname AS "Nome da Tabela",
        idx.indnatts AS "Altura",
        pg_relation_size(t.oid) AS "Tamanho do Índice",
        am.amname AS "Método de Acesso",
        idx.indkey AS "Colunas do Índice",
        idx.indisunique AS "Índice Único",
        idx.indisprimary AS "Índice Primário"
    FROM
        pg_index idx
        JOIN pg_class t ON t.oid = idx.indrelid
        JOIN pg_class i ON i.oid = idx.indexrelid
        JOIN pg_am am ON am.oid = t.relam
    WHERE
        t.relkind = 'r'
    ORDER BY
        t.relname,
        i.relname;
"""

# Executando a consulta SQL
cur.execute(query)

# Recuperando os resultados
rows = cur.fetchall()

# Imprimindo os metadados dos índices
for row in rows:
    print("\nNome do Índice:", row[0])
    print("Nome da Tabela:", row[1])
    print("Altura:", row[2])
    print("Tamanho do Índice:", row[3], "bytes")
    print("Método de Acesso:", row[4])
    print("Colunas do Índice:", row[5])
    print("Índice Único:", row[6])
    print("Índice Primário:", row[7])
    print()

# Fechar a conexão com o banco de dados
cur.close()
conn.close()