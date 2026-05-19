import rabbitpy
import json
import time
from const import RABBITMQ_ADDR, RABBITMQ_USER, RABBITMQ_PASS, RABBITMQ_VHOST

url = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_ADDR}:5672/{RABBITMQ_VHOST}'

janela = []
JANELA_SEGUNDOS = 7200

with rabbitpy.Connection(url) as conn:
    with conn.channel() as channel:
        fila = rabbitpy.Queue(channel, 'leituras')
        fila.declare()

        print("[Processador] Aguardando leituras...")
        for msg in fila:
            leitura = json.loads(msg.body)
            agora = time.time()

            janela.append(leitura)
            janela[:] = [l for l in janela if agora - l['timestamp'] <= JANELA_SEGUNDOS]

            media = round(sum(l['temperatura'] for l in janela) / len(janela), 2)
            print(f"[Processador] Media 2h: {media}C | Leituras na janela: {len(janela)}")
            msg.ack()