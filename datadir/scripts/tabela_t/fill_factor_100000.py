import conecta

# Estabelecer conexão com o PostgreSQL
connection = conecta.establish_connection()

# Criar a tabela "t" e popula com os dados necessários
create_table_query = """
DROP TABLE IF EXISTS t;
CREATE TABLE t (k serial PRIMARY KEY, v integer);
INSERT INTO t (v)
SELECT trunc(random() * 10) FROM generate_series(1, 100000);
"""
with connection.cursor() as cursor:
    cursor.execute(create_table_query)
connection.commit()
print("\nTabela 't' criada e populada com sucesso!\n")

# Criar índices na tabela "t" com diferentes valores de fillfactor
fillfactors = [60, 80, 90, 100]
for fillfactor in fillfactors:
    index_name = f"t_fillfactor_{fillfactor}"
    create_index_query = f"""
    CREATE INDEX {index_name} ON t (v) WITH (fillfactor={fillfactor});
    """
    with connection.cursor() as cursor:
        cursor.execute(create_index_query)
    connection.commit()

# Executar as consultas e analisar o desempenho
select_query = """
SELECT * FROM t WHERE v = 5;
"""
for fillfactor in fillfactors:
    index_name = f"t_fillfactor_{fillfactor}"
    explain_query = f"EXPLAIN (ANALYZE, BUFFERS) {select_query}"
    with connection.cursor() as cursor:
        cursor.execute(explain_query)
        result = cursor.fetchone()
        print(f"Índice: {index_name}")
        execution_time = result[0].split("actual time=")[1].split(" ")[0]
        print(f"  Tempo de execução: {execution_time} segundos")
        print(f"  Quantidade de linhas retornadas: {result[0].split('rows=')[1].split(' ')[0]}")
        print()

# Fechar a conexão
cursor.close()
connection.close()
