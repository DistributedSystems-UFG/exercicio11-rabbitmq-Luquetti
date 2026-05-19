import rabbitpy
import json
import time
import threading
from const import RABBITMQ_ADDR, RABBITMQ_USER, RABBITMQ_PASS, RABBITMQ_VHOST

url = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_ADDR}:5672/{RABBITMQ_VHOST}'
historico = []

def consumir_fila(fila_nome, tipo):
    with rabbitpy.Connection(url) as conn:
        with conn.channel() as channel:
            fila = rabbitpy.Queue(channel, fila_nome)
            fila.declare()
            print(f"[Historico] Consumindo fila '{fila_nome}'...")
            for msg in fila:
                dado = json.loads(msg.body)
                dado['tipo'] = tipo
                historico.append(dado)
                total_alertas = sum(1 for h in historico if h['tipo'] == 'alerta')
                print(f"[Historico] Total registros: {len(historico)} | Alertas: {total_alertas}")
                msg.ack()

t1 = threading.Thread(target=consumir_fila, args=('leituras', 'leitura'), daemon=True)
t2 = threading.Thread(target=consumir_fila, args=('alertas', 'alerta'), daemon=True)
t1.start()
t2.start()
t1.join()
t2.join()