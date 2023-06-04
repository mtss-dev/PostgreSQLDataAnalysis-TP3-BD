from conecta import *
from cont_tuplas import *

conn = establish_connection()

# Abrir o arquivo movie.sql
with open('../sqls/casting.sql', 'r') as f:
    script = f.read()

# Criar cursor
cursor = conn.cursor()

# Executar o script SQL
cursor.execute(script)

# Confirmar as alterações
conn.commit()

print("\nTabela casting criada com sucesso!")

# Imprimir a quantidade de tuplas na tabela
execute_query(conn, "SELECT COUNT(*) FROM casting", "casting")

# Fechar cursor e conexão
cursor.close()
conn.close()