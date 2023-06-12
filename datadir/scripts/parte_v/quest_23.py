from conecta import *
from cont_tuplas import *
import random
import time
import threading

versao = input("versao a ou b?")
num_agentes = int(input("numero de agentes [1,2,4,6,8,10]"))
tempo_inicio = time.time()
global done
done = False

#deixa a tabela pronta para uma nova carga teste
def cleanTable():
    conn = establish_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Assentos SET disp = True")
    conn.commit()
    conn.close()
    cur.close()

#chamar aqui para limpar a tabela antes de comecar a rodar as threads
cleanTable()

#verifica se todos os assentos ja foram ocupados, se sim, done = True
#atualiza escolheAssento() para nao incluir os ja ocupados
def controllerAssentos():
    global done #precisa p variavel done existir dentro do escopo dessa funcao
    while not done:
        conn = establish_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Assentos WHERE disp = True")     
        resultado = cur.fetchone()    
        if resultado[0] > 0:
            done = False
        # print("Há assentos disponíveis.")
        else: 
            done =  True
            tempo_final = time.time()
            tempo_total = tempo_final - tempo_inicio
            print(f"tempo final: {tempo_final}")
            print(f"tempo total: {tempo_total}")
            file = open("log.txt", "a")
            file.write(f"tempo total para {num_agentes} threads: {tempo_total}\n")
            print("Acabaram os assentos :(")

def retornaDisponiveis():   #passo 1
    conn = establish_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM Assentos WHERE disp = true')
    disponiveis = cur.fetchall()
    cur.close()
    conn.close()
    return disponiveis

def escolheAssento(assentos_disponiveis): #passo 2
    time.sleep(1)
    a = random.choice(assentos_disponiveis)[0]
    return a

def worker(thread_name, versao, nivel_isolamento = "READ COMMITED"):
    global done
    conn = establish_connection()
    cur = conn.cursor()

    #set da versao de isolamento
    if nivel_isolamento == "READ COMMITED":
        versao_isolamento = "BEGIN;" #read commited eh padrao, se tenta setar da erro
    else:
        versao_isolamento = "BEGIN; SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;"

    #o FOR UPDATE garante o isolamento a nivel de tupla


    if versao == 'a': #aqui eh a versao onde tudo vai numa unica transacao
        while not done:
            try: 
                cur.execute(versao_isolamento)
                cur.execute('SELECT * FROM Assentos WHERE disp = true FOR UPDATE') #parte 1
                disponiveis = cur.fetchall() #assentos disponiveis
                num_assento = random.choice(disponiveis)[0] #parte 2
                time.sleep(1)
                cur.execute("UPDATE Assentos SET disp = False WHERE num_voo = %s", (num_assento,)) #parte 3
                conn.commit()
                print(f"{thread_name}: {num_assento}")
            except (Exception, psycopg2.DatabaseError) as error:
                controllerAssentos()
                conn.rollback()
    elif versao == 'b': #versao onde 2 eh separada
        while not done:
            try:
                cur.execute(versao_isolamento)
                cur.execute('SELECT * FROM Assentos WHERE disp = true FOR UPDATE') #parte 1
                num_assento = escolheAssento(retornaDisponiveis())   #parte 2 que ocorre fora das transacoes
                cur.execute("UPDATE Assentos SET disp = False WHERE num_voo = %s", (num_assento,)) #parte 3
                conn.commit()
                print(f"{thread_name}: {num_assento}")
            except (Exception, psycopg2.DatabaseError) as error:
                controllerAssentos()
                conn.rollback()   
    else:
        print(f"erro em {thread_name}")
        done = True
    conn.close()
    cur.close()


#cria as threads do worker
vet_threads = []
for i in range(0, num_agentes):
    name = f"Thread_{i}"
    thread = threading.Thread(target=worker, args = (name, versao, "SERIALIZABLE"))
    vet_threads.append(thread)

#adiciona thread do controller
thread_controller = threading.Thread(target=controllerAssentos)
vet_threads.append(thread_controller)
print(vet_threads)

#inicia as threads
for i in vet_threads:
    i.start()

while not done:
    pass