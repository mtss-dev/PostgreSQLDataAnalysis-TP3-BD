import conecta
import time


# Estabelecer conexão com o PostgreSQL
conn = conecta.establish_connection()

def checa_bloco():
    # Criar cursor
    cursor = conn.cursor()

    # Executar a consulta para obter o número de blocos usados
    cursor.execute("SELECT pg_sleep(1)")
    cursor.execute("SELECT * FROM pg_stats WHERE tablename='t'")
    cursor.execute("SELECT pg_stat_reset()")
    cursor.execute("EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM t ORDER BY k LIMIT 10")

    # Obter o resultado da consulta
    result = cursor.fetchall()

    # Percorrer as linhas do resultado
    for row in result:
        # Verificar se a linha contém a informação dos blocos
        if "Buffers:" in row[0]:
            # Extrair o número de blocos usados
            blocks_used = int(row[0].split("=")[1].split()[0])
            # Imprimir o número de blocos usados
            print("Número de blocos usados:", blocks_used)
            break

    # Fechar o cursor
    cursor.close()

def fill_factor():
    # Criar a tabela "t" e popula com os dados necessários
    create_table_query = """
    DROP TABLE IF EXISTS t;
    CREATE TABLE t (k serial PRIMARY KEY, v integer);
    INSERT INTO t (v)
    SELECT trunc(random() * 10) FROM generate_series(1, 100000);
    """
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
    conn.commit()
    print("Tabela 't' criada e populada com sucesso!\n")

    # Criar índices na tabela "t" com diferentes valores de fillfactor
    fillfactors = [60, 80, 90, 100]
    for fillfactor in fillfactors:
        index_name = f"t_fillfactor_{fillfactor}"
        create_index_query = f"""
        CREATE INDEX {index_name} ON t (v DESC) WITH (fillfactor={fillfactor});
        """
        with conn.cursor() as cursor:
            cursor.execute(create_index_query)
        conn.commit()

    # Executar as consultas e analisar o desempenho
    select_query = """
    SELECT * FROM t WHERE v = 5;
    """
    for fillfactor in fillfactors:
        index_name = f"t_fillfactor_{fillfactor}"
        explain_query = f"EXPLAIN (ANALYZE, BUFFERS) {select_query}"
        with conn.cursor() as cursor:
            cursor.execute(explain_query)
            result = cursor.fetchone()
            print(f"Índice: {index_name}")
            execution_time = result[0].split("actual time=")[1].split(" ")[0]
            print(f"  Tempo de execução: {execution_time} segundos")
            print(f"  Quantidade de linhas retornadas: {result[0].split('rows=')[1].split(' ')[0]}")
            print()

    # Fechar o cursor
    cursor.close()

def tempo():
    # Criar cursor
    cursor = conn.cursor()

    # Criar índice para o atributo 'v'
    cursor.execute("CREATE INDEX idx_v ON t (v)")

    # Realizar consulta para um valor específico
    start_time = time.time()

    valor_consulta = 5
    cursor.execute("SELECT * FROM t WHERE v = %s", (valor_consulta,))
    result = cursor.fetchall()

    end_time = time.time()
    consulta_time = end_time - start_time

    # Medir o tempo gasto para recriar o índice
    start_time = time.time()

    cursor.execute("DROP INDEX idx_v")
    cursor.execute("CREATE INDEX idx_v ON t (v)")

    end_time = time.time()
    recriar_indice_time = end_time - start_time

    # Imprimir resultados
    print("Tempo gasto para realizar a consulta: {:.4f} segundos".format(consulta_time))
    print("Tempo gasto para recriar o índice: {:.4f} segundos".format(recriar_indice_time))

    # Fechar cursor e conexão
    cursor.close()
    conn.close()

