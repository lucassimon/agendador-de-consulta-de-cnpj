from os import getenv
from logging import Logger
import pika

from .utils import InterfaceRabbitMQ


class PublishCreateJobToRabbit(InterfaceRabbitMQ):
    """
    Classe que inicializa as configurações do rabbitmq e a fila
    """

    def __init__(self, connection, channel, logger: Logger | None = None):
        self.conn = connection
        self.channel = channel

        # colocar esses dados em uma tabela
        self.exchange = 'create-job-use-case'
        self.routing_key = 'job_created'
        self.queue = 'job_created'
        self.exchange_dlx = 'create-job-use-case-dlq'
        self.queue_dl = 'job_created_dlq'
        self.routing_key_dl = 'job_created_dlq'
        self.logger = logger

        self.connect()
        super().__init__()

    def connect(self):
        if self.logger:
            self.logger.info("utils.interface.rabbitmq", message="Trying to connect into rabbitmq")
        try:
            if self.exchange_dlx and self.queue_dl and self.routing_key_dl:
                arguments = {
                    "x-dead-letter-exchange": self.exchange_dlx,
                    "x-dead-letter-routing-key": self.routing_key_dl,
                    "x-max-priority": 5
                }
            else:
                arguments = {"x-max-priority": 5}

            self.channel.queue_declare(queue=self.queue, durable=True, arguments=arguments)
            self.channel.queue_bind(self.queue, self.exchange, routing_key=self.routing_key)
            # Turn on delivery confirmations
            self.channel.confirm_delivery()

        except Exception as err:
            raise err


    def publish(self, message: dict):
        """
        Publish a message
        """

        properties = pika.BasicProperties(
            app_id="agendador-de-consulta-cnpj",
            content_type="application/json",
            delivery_mode=pika.DeliveryMode.Persistent,
            priority=message['priority']
        )

        body = self.message_to_json(message)

        if self.logger:
            self.logger.info("utils.interface.rabbitmq", message="Message sent to rabbitmq")

        # Send a message
        try:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=body,
                properties=properties
            )

        except pika.exceptions.UnroutableError as err:
            raise err


class PublishErrorsInCreateJobUseCaseToRabbit(InterfaceRabbitMQ):
    """
    Classe que inicializa as configurações do rabbitmq e a fila
    """

    def __init__(self, connection, channel, queue, routing_key, logger: Logger | None = None):
        self.conn = connection
        self.channel = channel

        # colocar esses dados em uma tabela
        self.exchange = 'errors-when-create-job-use-case'
        self.routing_key = routing_key
        self.queue = queue
        self.exchange_dlx = None
        self.queue_dl = None
        self.routing_key_dl = None
        self.logger = logger

        self.connect()
        super().__init__()

    def publish(self, message: dict):
        """
        Publish a message
        """

        properties = pika.BasicProperties(
            app_id="agendador-de-consulta-cnpj",
            content_type="application/json",
            delivery_mode=pika.DeliveryMode.Persistent
        )

        body = self.message_to_json(message)

        if self.logger:
            self.logger.info("utils.interface.rabbitmq", message="Message sent to rabbitmq")

        # Send a message
        try:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=body,
                properties=properties,
            )

        except pika.exceptions.UnroutableError as err:
            raise err


class PublishCreateJobToSQS:
    pass
