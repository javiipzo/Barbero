import threading
import time
import random
import queue

Barberos=1
Clientess=80
Asiento=1
Espera=1

def Esperar():
    time.sleep(random.randrange(1,5))

class barbero(threading.Thread):
    condicion=threading.Condition()
    completado=threading.Event()

    def __init__(self,id):
        super().__init__()
        self.id=id

    def run(self):
        while True:
            try:
                cliente_actual=sala_espera.get(block=False)
            except queue.Empty:
                if self.completado.is_set():
                    return

                print(f"Barbero durmiendo...")
                with self.condicion:
                    self.condicion.wait()
            else:
                cliente_actual.cortar(self.id)

class Clientee(threading.Thread):
    Duracion_corte=random.randrange(5,15)
    def __init__(self,id):
        super().__init__()
        self.id=id

    def corte(self):
        time.sleep(random.randrange(5,15))
    def cortar(self,barbero):
        print(f"Cliente {self.id} se esta cortando el pelo por el barbero ")
        self.corte()
        print(f"Cliente {self.id} termino de cortarse el pelo")
        self.atendido.set()

    def run(self):
        self.atendido=threading.Event()

        try:
            sala_espera.put(self,block=False)
        except queue.Full:
            print(f"Cliente {self.id} se fue")
            return

        print(f"Cliente {self.id} esperando...")
        with barbero.condicion:
            barbero.condicion.notify(1)

        self.atendido.wait()

if __name__=="__main__":
    Clientes=[]
    sala_espera=queue.Queue(maxsize=Asiento)
    for i in range (Barberos):
        hilo_Barbero=barbero(i)
        hilo_Barbero.start()

    for i in range (Clientess):
        Esperar()
        cliente=Clientee(i)
        Clientes.append(cliente)
        cliente.start()
    for cliente in Clientes:
        cliente.join()
    time.sleep(0.1)
    barbero.completado.set()
    with barbero.condicion:
        barbero.condicion.notify(1)
    print("La barberia cerró")



