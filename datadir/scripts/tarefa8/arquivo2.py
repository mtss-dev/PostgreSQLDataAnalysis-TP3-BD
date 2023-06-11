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

    # Inserir os dados diretamente no banco de dados
    with open(file_path, 'rb') as file:
        block_size = 64 * 1024  # Tamanho do bloco de leitura de 64 KB
        while True:
            data = file.read(block_size)
            if not data:
                break
            cursor.execute("INSERT INTO tabela_arquivo2 (content) VALUES (%s)", (data,))

    conn.commit()
    cursor.close()
    conn.close()
    print("Arquivo 2 inserido com sucesso no banco de dados!\n")

    end_time = time.time()
    insertion_time = end_time - start_time

    # Obter o espaço ocupado no disco pelo arquivo
    file_size = os.path.getsize(file_path)

    # Excluir o arquivo
    os.remove(file_path)
    print("Arquivo 2 excluído com sucesso! (Para liberar espaço no disco)\n")

    return insertion_time, file_size

# Função para excluir a tabela no banco de dados
def delete_table():
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS tabela_arquivo2")

    conn.commit()
    cursor.close()
    conn.close()
    print("Tabela excluída com sucesso! (Para liberar espaço no banco de dados)")


# Gera um arquivo com registros curtos (3 KB) e muitos registros (1 milhão)
def generate_short_records_file(file_path, num_records):
    start_time = time.time()

    with open(file_path, 'wb') as file:
        for i in range(num_records):
            record_id = i + 1
            record_content = generate_short_content()
            file.write(record_content)
    print("Arquivo 2 gerado com sucesso!\n")

    end_time = time.time()
    creation_time = end_time - start_time

    return creation_time


# Gera um conteúdo curto (3 KB) para cada registro
def generate_short_content():
    content_size = 3 * 1024  # Tamanho fixo de 3 KB
    content = os.urandom(content_size)
    return content


# Exemplo de uso
file_path = "arquivo2.bin"
num_records = 1000000

creation_time = generate_short_records_file(file_path, num_records)

insertion_time, disk_space = measure_insertion_time_and_disk_space(file_path)

total_execution_time = creation_time + insertion_time

print(f"Tempo para criação do arquivo: {round(creation_time, 2)} segundos")
print(f"Tempo de inserção no banco de dados: {round(insertion_time, 2)} segundos")
print(f"Tempo de execução total: {round(total_execution_time, 2)} segundos")
print(f"Espaço ocupado no disco pelo arquivo: {disk_space} bytes\n")

# Excluir a tabela no banco de dados
delete_table()