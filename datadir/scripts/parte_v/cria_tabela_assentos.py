from conecta import *
from cont_tuplas import *
import psycopg2

conn = establish_connection()
cursor = conn.cursor()

# Crie a tabela Assentos
cursor.execute("CREATE TABLE Assentos (num_voo INTEGER, disp BOOLEAN)")

# Coloca todos os assentos disponiveis
for num_voo in range(1, 201):
    cursor.execute("INSERT INTO Assentos (num_voo, disp) VALUES (%s, %s)", (num_voo, True))

conn.commit()
cursor.close()
conn.close()

print("A tabela 'Assentos' foi criada e preenchida com sucesso!")
