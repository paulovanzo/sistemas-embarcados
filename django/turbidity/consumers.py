import paho.mqtt.client as mqtt
from django.conf import settings
import logging
import threading
from prometheus_client import Gauge

# Configura a métrica Prometheus
turbidity = Gauge('Turbidity', 'Valor de turbidez da água')

# Configura o logger
logger = logging.getLogger('django')

class MQTTManager:
    def __init__(self, host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT, username=settings.RABBITMQ_USER, password=settings.RABBITMQ_PASSWORD, topic='metrics.turbidity'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.topic = topic
        self.client = mqtt.Client()
        self.client.username_pw_set(username=self.username, password=self.password)
        self.consumer_thread = None

    def connect(self):
        """Estabelece a conexão com o broker MQTT e configura a assinatura do tópico."""
        try:
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message

            self.client.connect(self.host, int(self.port), 60)
            self.client.loop_start()  # Inicia o loop de rede

            logger.info(f"Connected to MQTT broker on {self.host}, subscribing to topic '{self.topic}'")
        except Exception as e:
            logger.critical(f"Failed to connect to MQTT broker: {e}")
            raise

    def on_connect(self, client, userdata, flags, rc):
        """Callback quando a conexão é estabelecida."""
        if rc == 0:
            logger.info(f"Connected to MQTT broker with result code {rc}")
            self.client.subscribe(self.topic)
        else:
            logger.error(f"Failed to connect to MQTT broker, result code {rc}")

    def on_message(self, client, userdata, msg):
        """Callback quando uma mensagem é recebida."""
        try:
            # Converte a mensagem recebida (presumindo que seja um número em bytes)
            value = int.from_bytes(msg.payload, byteorder="big")
            # Atualiza a métrica Prometheus
            turbidity.set(value)
            logger.info(f"Received {value} from MQTT topic '{msg.topic}' and updated Prometheus metric.")
        except Exception as e:
            logger.error(f"Failed to process message from topic '{msg.topic}': {msg.payload}. Error: {e}")

    def run(self):
        """Inicia o consumidor em uma thread separada."""
        if not self.consumer_thread or not self.consumer_thread.is_alive():
            self.consumer_thread = threading.Thread(target=self._consume)
            self.consumer_thread.start()
            logger.info("MQTT consumer thread started.")

    def _consume(self):
        """Método privado que conecta e começa a consumir mensagens."""
        self.connect()

    def stop(self):
        """Encerra a conexão com o broker MQTT."""
        if self.client.is_connected():
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("MQTT connection closed.")
