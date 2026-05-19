import rabbitpy
import json
from const import RABBITMQ_ADDR, RABBITMQ_USER, RABBITMQ_PASS, RABBITMQ_VHOST

url = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_ADDR}:5672/{RABBITMQ_VHOST}'

with rabbitpy.Connection(url) as conn:
    with conn.channel() as channel:
        fila = rabbitpy.Queue(channel, 'alertas')
        fila.declare()

        print("[Alertas] Aguardando alertas criticos...")
        for msg in fila:
            alerta = json.loads(msg.body)
            print(f"[ALERTA] Sensor: {alerta['sensor_id']} | Temp: {alerta['temperatura']}C")
            print(f"  >> Simulando envio de notificacao para operador...")
            print(f"  >> {alerta['mensagem']}")
            msg.ack()