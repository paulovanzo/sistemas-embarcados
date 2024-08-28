from django.apps import AppConfig
from .consumers import MQTTManager
import logging

logger = logging.getLogger('django')

class ApiConfig(AppConfig):
    name = "turbidity"
    

    def ready(self):

        # Instancia o RabbitMQManager e inicia o consumidor
        rabbit_manager = MQTTManager()
        rabbit_manager.run()
        logger.info("RabbitMQ consumer thread started via run method.")
