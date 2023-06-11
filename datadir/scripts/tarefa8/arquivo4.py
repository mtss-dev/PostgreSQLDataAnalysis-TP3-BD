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

    # Abrir o arquivo e ler os dados
    with open(file_path, 'rb') as file:
        records = []
        while True:
            data = file.read(8192)  # Tamanho do bloco de leitura, ajuste conforme necessário
            if not data:
                break
            records.append((data,))

        # Utilizar o método executemany para inserir vários registros de uma vez
        cursor.executemany("INSERT INTO tabela_arquivo4 (content) VALUES (%s)", records)

    conn.commit()
    cursor.close()
    conn.close()
    print("Arquivo 4 inserido com sucesso no banco de dados!\n")

    end_time = time.time()
    insertion_time = end_time - start_time

    # Obter o espaço ocupado no disco pelo arquivo
    file_size = os.path.getsize(file_path)

    # Excluir o arquivo
    os.remove(file_path)
    print("Arquivo 4 excluído com sucesso! (Para liberar espaço no disco)\n")

    return insertion_time, file_size


# Função para excluir a tabela no banco de dados
def delete_table():
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS tabela_arquivo4")

    conn.commit()
    cursor.close()
    conn.close()
    print("Tabela excluída com sucesso! (Para liberar espaço no banco de dados)")


# Gera um arquivo com registros variáveis (ex. muitos NULLs) e muitos registros (30 mil)
def generate_variable_records_file(file_path, num_records):
    start_time = time.time()

    with open(file_path, 'wb') as file:
        block_size = 8192  # Tamanho do bloco de registros, ajuste conforme necessário
        records_per_block = 100  # Número de registros por bloco, ajuste conforme necessário

        for i in range(num_records // records_per_block):
            block_content = b""
            for j in range(records_per_block):
                record_content = generate_variable_content()
                block_content += record_content

            file.write(block_content)

        remaining_records = num_records % records_per_block
        for i in range(remaining_records):
            record_content = generate_variable_content()
            file.write(record_content)

    end_time = time.time()
    creation_time = end_time - start_time
    print("Arquivo 4 gerado com sucesso!\n")

    return creation_time


# Gera um conteúdo variável (ex. muitos NULLs) para cada registro
def generate_variable_content():
    # Gerar um conteúdo com uma mistura de dados e NULLs
    content_size = random.randint(10 * 1024, 20 * 1024)  # Tamanho entre 10 KB e 20 KB
    content = bytearray(content_size)

    # Definir uma taxa de NULLs (por exemplo, 10%)
    null_rate = 0.1

    for i in range(content_size):
        if random.random() < null_rate:
            content[i] = 0x00  # Representação de NULL em bytes
        else:
            content[i] = random.randint(1, 255)  # Dados aleatórios

    return bytes(content)


# Exemplo de uso
file_path = "arquivo4.bin"
num_records = 1000000

creation_time = generate_variable_records_file(file_path, num_records)

insertion_time, disk_space = measure_insertion_time_and_disk_space(file_path)

total_execution_time = creation_time + insertion_time

print(f"Tempo para criação do arquivo: {round(creation_time, 2)} segundos")
print(f"Tempo de inserção no banco de dados: {round(insertion_time, 2)} segundos")
print(f"Tempo de execução total: {round(total_execution_time, 2)} segundos")
print(f"Espaço ocupado no disco pelo arquivo: {disk_space} bytes\n")

# Excluir a tabela no banco de dados
delete_table()