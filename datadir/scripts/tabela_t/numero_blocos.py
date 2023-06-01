import conecta

# Estabelecer conexão com o PostgreSQL
conn = conecta.establish_connection()

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

# Fechar cursor e conexão
cursor.close()
conn.close()
