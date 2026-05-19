import rabbitpy
import json
import time
import random
from const import RABBITMQ_ADDR, RABBITMQ_USER, RABBITMQ_PASS, RABBITMQ_VHOST

url = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_ADDR}:5672/{RABBITMQ_VHOST}'

with rabbitpy.Connection(url) as conn:
    with conn.channel() as channel:
        fila = rabbitpy.Queue(channel, 'leituras')
        fila.declare()

        print("[Sensor-01] Iniciado. Publicando leituras de temperatura...")
        while True:
            mensagem = {
                'sensor_id': 'sensor-01',
                'timestamp': time.time(),
                'temperatura': round(random.uniform(15.0, 45.0), 2)
            }
            msg = rabbitpy.Message(channel, json.dumps(mensagem))
            msg.publish('', 'leituras')
            print(f"[Sensor-01] Publicado: {mensagem}")
            time.sleep(3)