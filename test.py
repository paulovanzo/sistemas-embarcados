import pika

rabbitmq_host = '10.51.69.15'  # ou o endereço do seu servidor RabbitMQ
rabbitmq_user = 'user'    # Substitua pelo seu nome de usuário
rabbitmq_password = 'password'  # Substitua pela sua senha

# Configuração de autenticação
credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)
connection_params = pika.ConnectionParameters(
    host=rabbitmq_host,
    credentials=credentials,
    port=3001
)

connection = pika.BlockingConnection(connection_params)

channel = connection.channel()

# Declarando uma fila
queue_name = 'bomdia'
channel.queue_declare(queue=queue_name, durable=True)

# Publicando mensagens na fila
message = 'Bom dia chefe'
channel.basic_publish(
    exchange='',
    routing_key=queue_name,
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2  # Torna a mensagem persistente
    )
)

print(f"Mensagem enviada: {message}")

# Fechar conexão
connection.close()
