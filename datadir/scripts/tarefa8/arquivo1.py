import os
import random
import time
import psycopg2
from conecta import *

# Função para medir o tempo de inserção dos dados no banco de dados e obter o espaço ocupado no disco
def measure_insertion_time_and_disk_space(file_path):
    conn = establish_connection()
    cursor = conn.cursor()

    start_time = time.time()

    # Inserir os dados diretamente no banco de dados utilizando o método executemany
    with open(file_path, 'rb') as file:
        data = file.read()  # Ler todo o conteúdo do arquivo de uma vez

        # Separar o conteúdo em blocos de inserção
        block_size = 64 * 1024  # Tamanho do bloco de inserção de 64 KB
        num_blocks = (len(data) + block_size - 1) // block_size  # Calcular o número de blocos necessários

        # Criar uma lista de blocos de dados
        blocks = [(data[i * block_size:(i + 1) * block_size],) for i in range(num_blocks)]

        # Utilizar o método executemany para inserir vários blocos de dados de uma vez
        cursor.executemany("INSERT INTO tabela_arquivo1 (content) VALUES (%s)", blocks)

    conn.commit()
    cursor.close()
    conn.close()
    print("Arquivo 1 inserido com sucesso no banco de dados!\n")

    end_time = time.time()
    insertion_time = end_time - start_time

    # Obter o espaço ocupado no disco pelo arquivo
    file_size = os.path.getsize(file_path)

    # Excluir o arquivo
    os.remove(file_path)
    print("Arquivo 1 excluído com sucesso! (Para liberar espaço no disco)\n")

    return insertion_time, file_size

# Função para excluir a tabela no banco de dados
def delete_table():
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS tabela_arquivo1")

    conn.commit()
    cursor.close()
    conn.close()
    print("Tabela excluída com sucesso! (Para liberar espaço no banco de dados)")


# Gera um arquivo com registros longos (>100 KB) e poucos registros (10000)
def generate_long_records_file(file_path, num_records):
    start_time = time.time()

    with open(file_path, 'wb') as file:
        for i in range(num_records):
            record_id = i + 1
            record_content = generate_long_content()
            file.write(record_content)
    print("Arquivo 1 gerado com sucesso!\n")

    end_time = time.time()
    creation_time = end_time - start_time

    return creation_time


# Gera um conteúdo longo (110 KB) para cada registro
def generate_long_content():
    content_size = 110 * 1024  # Tamanho fixo de 110 KB
    content = os.urandom(content_size)
    return content


# Exemplo de uso
file_path = "arquivo1.bin"
num_records = 10000

creation_time = generate_long_records_file(file_path, num_records)

insertion_time, disk_space = measure_insertion_time_and_disk_space(file_path)

total_execution_time = creation_time + insertion_time

print(f"Tempo para criação do arquivo: {round(creation_time, 2)} segundos")
print(f"Tempo de inserção no banco de dados: {round(insertion_time, 2)} segundos")
print(f"Tempo de execução total: {round(total_execution_time, 2)} segundos")
print(f"Espaço ocupado no disco pelo arquivo: {disk_space} bytes\n")

# Excluir a tabela no banco de dados
delete_table()