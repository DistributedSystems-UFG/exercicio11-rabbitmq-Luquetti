[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/BK9AX0KL)
# RabbitMQ-Example
Example based on Tanenbaum &amp; van Steen (2025)

# Steps to run:

## Ports to open on the firewall (security group on AWS):
```
5671-5672
```

## Install the RabbitMQ broker on a server machine:
You may use the provided script for installation (install_rabbitmq.sh)
```
sudo install_rabbitmq.sh
```
*Note:* Make sure the file is executable (chmod 770 install_rabbitmq.sh)

See installation and configuration details on: https://www.rabbitmq.com/docs/install-debian#apt-quick-start (although the defaults should work just fine for our purposes).

### Once installed, put the broker to run:
```
sudo systemctl start rabbitmq-server
```
### Then create a new RabbitMQ user and password:
```
sudo rabbitmqctl add_user myuser abc123
```
### Now create a vhost in the RabbitMQ server (a vhost is like a container for message queues)?
```
sudo rabbitmqctl add_vhost my_vhost
```
### And give the new user the required permisssions to access the vhost:
```
sudo rabbitmqctl set_permissions -p my_vhost myuser ".*" ".*" ".*"
```

## Finally, install the RabbitMQ python client on the machines where producers and consumers will run:
```
pip install rabbitpy
```

*Note:* Make sure the IP address of the RabbitMQ server is correctly set in const.py


# Exercício 11 — RabbitMQ

## Arquitetura
produtor_sensor.py   → fila: leituras → consumidor_processador.py
                                       → consumidor_historico.py
produtor_alertas.py  → fila: leituras → (mesmos consumidores)
                     → fila: alertas  → consumidor_alertas.py
                                      → consumidor_historico.py

## Instalação
pip install rabbitpy

## Configuração
Edite const.py com o IP do servidor RabbitMQ.

## Setup no servidor (uma vez só)
sudo rabbitmqctl add_user myuser abc123
sudo rabbitmqctl add_vhost my_vhost
sudo rabbitmqctl set_permissions -p my_vhost myuser ".*" ".*" ".*"

## Execução (terminais separados)
python3 consumidor_processador.py
python3 consumidor_alertas.py
python3 consumidor_historico.py
python3 produtor_sensor.py
python3 produtor_alertas.py