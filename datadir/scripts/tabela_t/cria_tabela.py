import conecta

conn = conecta.establish_connection()

# Popular a tabela "t"
create_table_query = """
DROP TABLE IF EXISTS t;
CREATE TABLE t (k serial PRIMARY KEY, v integer);

INSERT INTO t(v) 
SELECT trunc(random() * 10) FROM generate_series(1, 100000);
"""

with conn.cursor() as cursor:
    cursor.execute(create_table_query)
conn.commit()

print("Tabela populada com sucesso!")

# Executar a consulta SQL para obter os valores das 10 primeiras tuplas ordenadas por "k"
select_query = """
SELECT * FROM t ORDER BY k LIMIT 10;
"""
with conn.cursor() as cursor:
    cursor.execute(select_query)
    rows = cursor.fetchall()
    for row in rows:
        print(f"k = {row[0]} v = {row[1]}")

# Fechar cursor e conexão
cursor.close()
conn.close()