# Sistemas-Embarcados
## Mini sistema para receber dados via MQTT de dispositivo IoT que captura dados de um sensor de turbidez de água

![Feito com Excalidraw](/image.png "Design do Sistema")

Você vai precisar do docker e docker compose para rodar o projeto, além da porta 15672, 5672 e 3000 disponíveis no seu computador.

Segue documentação de instalação do [Docker](https://docs.docker.com/get-started/get-docker/).

Rode o programa setando as varíaveis no arquivo *.env.development*

## Variáveis Alertmanager e RabbitMQ

|  Variável         | Uso
| ----------------- |:-------------------------------------------------------------------------:|
| RABBITMQ_USER     | Usuário RabbitMQ padrão do servidor                                       |
| RABBITMQ_PASSWORD | Senha RabbitMQ padrão do servidor                                         |
| SOURCE_EMAIL      | Email google para enviar o alerta de turbidez de água                     |
| TARGET_EMAIL      | Email google para receber o alerta de turbidez de água                    |
| GOOGLE_PASSWORD   | Senha de App para o Alertmanager se autenticar no servidor SMTP do Google |

e as variáveis do Django no arquivo *.env.development* no diretório ./django

## Variáveis Django

|  Variável         | Uso
| ----------------- |:--------------------------------------------------:|
| RABBITMQ_HOST     | Host do RabbitMQ                                   |
| RABBITMQ_USER     | Usuário do RabbitMQ para a aplicação Django        |
| RABBITMQ_PASSWORD | Senha do RabbitMQ para a aplicação Django          |
| RABBITMQ_PORT     | Porta de conexão AMQP com o RabbitMQ para o Django |
| SECRET_KEY        | Secret key utilizada pelo Django                   |


daí execute o arquivo script.sh na raiz do projeto

```
chmod +x script.sh
./script.sh
```

Habilitar plugin MQTT 
```rabbitmq-plugins enable rabbitmq_mqtt```

Reinicie o container RabbitMQ
```docker compose restart rabbitmq```

## Autores

Criado por Paulo Vanzolini, [Lucas Agnez](https://github.com/LucasAgnez) e [Rafael Gomes](https://github.com/rafaelgdgs).

# Embedded Systems
## Mini System to Receive Data via MQTT from IoT Device Capturing Water Turbidity Sensor Data

![Made with Excalidraw](/image.png "System Design")

You will need Docker and Docker Compose to run the project, and ensure that ports 15672, 5672, and 3000 are available on your computer.

Refer to the [Docker Installation Documentation](https://docs.docker.com/get-started/get-docker/) for instructions.

Run the program by setting the variables in the `*.env.development*` file.

## Alertmanager and RabbitMQ Variables

|  Variable         | Usage
| ----------------- |:-------------------------------------------------------------------------:|
| RABBITMQ_USER     | Default RabbitMQ username for the server                                    |
| RABBITMQ_PASSWORD | Default RabbitMQ password for the server                                    |
| SOURCE_EMAIL      | Google email to send the water turbidity alert                               |
| TARGET_EMAIL      | Google email to receive the water turbidity alert                            |
| GOOGLE_PASSWORD   | App password for Alertmanager to authenticate with Google's SMTP server      |

And set the Django variables in the `*.env.development*` file located in the `./django` directory.

## Django Variables

|  Variable         | Usage
| ----------------- |:--------------------------------------------------:|
| RABBITMQ_HOST     | RabbitMQ host                                      |
| RABBITMQ_USER     | RabbitMQ user for the Django application           |
| RABBITMQ_PASSWORD | RabbitMQ password for the Django application       |
| RABBITMQ_PORT     | AMQP connection port with RabbitMQ for Django      |
| SECRET_KEY        | Secret key used by Django                          |

Then, simply run the `script.sh` file in the root of the project:

```
chmod +x script.sh
./script.sh
```

## Authors

Created by Paulo Vanzolini, [Lucas Agnez](https://github.com/LucasAgnez) e [Rafael Gomes](https://github.com/rafaelgdgs).
