import conecta
import time

# Estabelecer conexão
conn = conecta.establish_connection()

def recriar_tabela():
    # Criar cursor
    cursor = conn.cursor()

    # Remover a tabela 't' se existir
    cursor.execute("DROP TABLE IF EXISTS t")

    # Criar novamente a tabela 't' com 1.000.000 de tuplas
    cursor.execute("CREATE TABLE t (k serial PRIMARY KEY, v integer)")

    # Inserir 1.000.000 de tuplas na tabela
    cursor.execute("INSERT INTO t(v) SELECT trunc(random() * 10) FROM generate_series(1, 1000000)")

    # Confirmar as alterações
    conn.commit()

    # Fechar cursor
    cursor.close()
    print("\nTabela recriada com sucesso!")


def consultar_tabela():
    # Valor específico a ser consultado
    specific_value = 5

    # Criar cursor
    cursor = conn.cursor()

    # Medir o tempo de execução da consulta
    start_time = time.time()

    # Executar a consulta
    cursor.execute("SELECT * FROM t WHERE v = %s", (specific_value,))

    # Obter o resultado da consulta
    result = cursor.fetchall()

    # Calcular o tempo de execução
    execution_time = time.time() - start_time

    # Imprimir o resultado e o tempo de execução
    print("Tempo de execução: {:.4f} segundos.".format(execution_time))

    # Fechar cursor
    cursor.close()


def recria_indice():
    # Criar cursor
    cursor = conn.cursor()

    # Medir o tempo de execução da criação do índice
    start_time = time.time()

    # Recriar o índice para o atributo 'v'
    cursor.execute("DROP INDEX IF EXISTS idx_v")
    cursor.execute("CREATE INDEX idx_v ON t(v)")

    # Calcular o tempo de execução
    execution_time = time.time() - start_time

    # Imprimir o tempo de execução
    print("Tempo de execução para recriar o índice: {:.4f} segundos.".format(execution_time))

    # Fechar cursor
    cursor.close()
    conn.close()


recriar_tabela()
consultar_tabela()
recria_indice()