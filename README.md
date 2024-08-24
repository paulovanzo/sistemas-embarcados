# Sistemas-Smbarcados
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


daí é só executar o arquivo script.sh na raiz do projeto

```
chmod +x script.sh
./script.sh
```
