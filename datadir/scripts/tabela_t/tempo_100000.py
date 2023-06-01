import conecta
import time

# Estabelecer conexão
conn = conecta.establish_connection()

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