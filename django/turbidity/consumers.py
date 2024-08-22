import pika
from django.conf import settings
import logging
import threading

import pika.exceptions
from prometheus_client import Gauge

turdity = Gauge('Turbidity', 'Valor de turbidez da água')

logger = logging.getLogger('django')

class RabbitMQManager:
    def __init__(self, port=settings.RABBITMQ_PORT, host=settings.RABBITMQ_HOST, username=settings.RABBITMQ_USER, password=settings.RABBITMQ_PASSWORD, exchange='topic_logs', exchange_type='topic', queue='sensor-1', routing_key='metrics.turbidity_metric'):
        self.host = host
        self.username=username
        self.password=password
        self.port=port
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.queue = queue
        self.routing_key = routing_key
        self.connection = None
        self.channel = None
        self.consumer_thread = None

    def connect(self):
        """Estabelece a conexão com RabbitMQ e configura a exchange e fila."""
        try:
            credentials = pika.PlainCredentials(username=self.username, password=self.password)
            connection_params = pika.ConnectionParameters(
                host=self.host,
                credentials=credentials,
                port=self.port
            )
            self.connection = pika.BlockingConnection(connection_params)
            
            self.channel = self.connection.channel()
            
            # Declarar a exchange
            self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type)
            
            # Declarar a fila
            result = self.channel.queue_declare(queue=self.queue, exclusive=True)
            self.queue_name = result.method.queue
            
            # Vincular a fila à exchange com a routing key especificada
            self.channel.queue_bind(exchange=self.exchange, queue=self.queue_name, routing_key=self.routing_key)
            
            logger.info(f"Connected to RabbitMQ on {self.host}, exchange '{self.exchange}', queue '{self.queue_name}'")
        except Exception as e:
            logger.critical(f"Failed to connect to RabbitMQ: {e}")
            raise pika.exceptions.ConnectionClosed

    def start_consuming(self, callback):
        """Inicia o consumo de mensagens da fila."""
        try:
            if not self.channel:
                self.connect()

            logger.info(f"Waiting for messages on queue '{self.queue_name}'.")
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
            self.channel.start_consuming()
        except Exception as e:
            logger.error(f"Failed to consume messages: {e}")
            raise pika.exceptions.ConsumerCancelled

    def stop(self):
        """Encerra a conexão com RabbitMQ."""
        if self.connection and self.connection.is_open:
            self.connection.close()
            logger.info("RabbitMQ connection closed.")
    
    
    def start_consumer():
        rabbit_manager = RabbitMQManager()
        rabbit_manager.connect()
        rabbit_manager.start_consuming(rabbit_manager.callback)


    def callback(self, ch, method, properties, body):
        try:
            # Converte a mensagem recebida (presumindo que seja um número)
            value = int.from_bytes(body, byteorder="big")
            # Atualiza a métrica Prometheus
            turdity.set(value)
            logger.info(f"Received {value} from RabbitMQ and updated Prometheus metric.")
        except Exception as e:
            logger.error(f"Failed to process message: {body}. Error: {e}")

    def run(self):
        """Inicia o consumidor em uma thread separada."""
        if not self.consumer_thread or not self.consumer_thread.is_alive():
            self.consumer_thread = threading.Thread(target=self._consume)
            self.consumer_thread.start()
            logger.info("RabbitMQ consumer thread started.")

    def _consume(self):
        """Método privado que conecta e começa a consumir mensagens."""
        self.connect()
        self.start_consuming(self.callback)
