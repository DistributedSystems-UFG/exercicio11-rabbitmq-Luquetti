import rabbitpy
import json
import time
import random
from const import RABBITMQ_ADDR, RABBITMQ_USER, RABBITMQ_PASS, RABBITMQ_VHOST

url = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_ADDR}:5672/{RABBITMQ_VHOST}'

with rabbitpy.Connection(url) as conn:
    with conn.channel() as channel:
        fila_leituras = rabbitpy.Queue(channel, 'leituras')
        fila_leituras.declare()
        fila_alertas = rabbitpy.Queue(channel, 'alertas')
        fila_alertas.declare()

        print("[Sensor-02] Iniciado. Publicando leituras e alertas...")
        while True:
            temperatura = round(random.uniform(15.0, 45.0), 2)
            leitura = {
                'sensor_id': 'sensor-02',
                'timestamp': time.time(),
                'temperatura': temperatura
            }
            msg = rabbitpy.Message(channel, json.dumps(leitura))
            msg.publish('', 'leituras')
            print(f"[Sensor-02] Leitura: {leitura}")

            if temperatura > 40.0:
                alerta = {
                    'sensor_id': 'sensor-02',
                    'timestamp': time.time(),
                    'temperatura': temperatura,
                    'mensagem': f'ALERTA: temperatura critica {temperatura}C'
                }
                msg_alerta = rabbitpy.Message(channel, json.dumps(alerta))
                msg_alerta.publish('', 'alertas')
                print(f"[Sensor-02] ALERTA publicado: {alerta}")

            time.sleep(4)