from django.apps import AppConfig
from .consumers import RabbitMQManager
import logging

logger = logging.getLogger('django')

class ApiConfig(AppConfig):
    name = "turbidity"
    

    def ready(self):

        # Instancia o RabbitMQManager e inicia o consumidor
        rabbit_manager = RabbitMQManager()
        rabbit_manager.run()
        logger.info("RabbitMQ consumer thread started via run method.")
