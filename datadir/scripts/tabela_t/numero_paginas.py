import conecta

# Estabelecer conexão
conn = conecta.establish_connection()

# Criar cursor
cursor = conn.cursor()

# Atualizar as estatísticas da tabela 't'
cursor.execute("ANALYZE t")

# Executar a consulta
cursor.execute("SELECT relname, relpages, reltuples FROM pg_class WHERE relname='t';")

# Obter o resultado da consulta
result = cursor.fetchone()

# Imprimir o resultado
print("Tabela: ", result[0])
print("Número de páginas: ", result[1])
print("Número de tuplas: ", result[2])

# Fechar cursor e conexão
cursor.close()
conn.close()