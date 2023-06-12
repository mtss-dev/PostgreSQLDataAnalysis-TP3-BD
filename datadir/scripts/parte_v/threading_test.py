import threading
import time
import random

value = 5

quant_agente_reservas = 1

#set disp to false for every tuple
def cleanTable():
    pass

done = False
def escolheAssento(text):
    a = random.randint(1, 200)
    print(f"Thread: {a}")

def geradorAssentos(text):
    while not done:
        time.sleep(1)
        escolheAssento(text)


#disp = false to close this element
def agente(text):
    counter = 0
    while done:
        time.sleep(1)
        counter+=1
        value+=1
        print(f"{text}: {counter};")

for i in range (0, 2):
    name = f"Thread_{i}"
    threading.Thread(target=geradorAssentos, args = (name, )).start()

##finish all threads
input("press enter")
done = True