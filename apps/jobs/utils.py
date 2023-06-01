from abc import ABC, abstractmethod
from json import dumps
from typing import Dict

# Third

from pika import URLParameters, BlockingConnection

# Apps

# Local

class Cpf:
    def __init__(self, cpf):
        # forçando inteiros para serem transformados para string
        self.cpf = str(cpf)
        self.normalize_cpf_cnpj()

    def normalize_cpf_cnpj(self):
        # normalizo a string retirando caracteres especiais
        self.cpf = self.cpf.strip().replace(".", "").replace("-", "").replace("/", "")

    def validate(self):
        if self.check_len():
            return False

        first_digit = self.calculate_first_digit()
        if self.cpf[9] != str(first_digit):
            return False

        second_digit = self.calculate_second_digit()
        if self.cpf[10] != str(second_digit):
            return False

        return True

    def check_len(self):
        return len(self.cpf) != 11

    def calculate_first_digit(self):
        first_digit = 0
        for i in range(10, 1, -1):
            first_digit += int(self.cpf[10 - i]) * i

        rest = first_digit % 11

        return self.cpf_rule(rest)

    def calculate_second_digit(self):
        second_digit = 0
        for i in range(11, 1, -1):
            second_digit += int(self.cpf[11 - i]) * i

        rest = second_digit % 11

        return self.cpf_rule(rest)

    def cpf_rule(self, rest):
        if rest < 2:
            return 0
        else:
            return 11 - rest



class RabbitMQ:
    """
    A class to do a connection
    """

    @staticmethod
    def connect(uri: str):
        """
        Connect sync to RabbitMQ and returns the connection and channel
        """
        params = URLParameters(uri)
        # number of socket connection attempts
        params.connection_attempts = 7
        # interval between socket connection attempts; see also connection_attempts.
        params.retry_delay = 300
        # AMQP connection heartbeat timeout value for negotiation during connection
        # tuning or callable which is invoked during connection tuning
        params.heartbeat = 600
        # None or float blocked connection timeout
        params.blocked_connection_timeout = 300
        try:
            connect = BlockingConnection(params)
            channel = connect.channel()

            return connect, channel

        except Exception as exc:
            raise exc


class InterfacePublishToQueue(ABC):
    """
    Interface to publish messages
    """

    conn = None
    channel = None
    exchange = None
    exchange_dlx = None
    queue_dl = None
    routing_key_dl = None
    queue = None
    routing_key = None

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def connect(self):
        """
        Abstract method to connect
        """
        pass

    @abstractmethod
    def publish(self, message: dict):
        """
        Abstract method to publish
        """
        pass

    def close_channel(self):
        """
        Close a channel
        """
        self.channel.close()

    def close_connection(self):
        """
        Close connection
        """
        self.conn.close()

    def teardown(self):
        """
        Closes a channel and connection
        """
        self.close_channel()
        self.close_connection()

    def run(self, message):
        """
        Connect and publish a message
        """
        self.connect()
        self.publish(message)

    def message_to_json(self, message: Dict):
        """ "
        Transforms a message dict to a json
        """
        try:
            body = dumps(message)
            return body
        except Exception as exc:
            raise exc


class InterfaceRabbitMQ(InterfacePublishToQueue):
    """
    Interface with connect and publish methods
    """

    def connect(self):
        if self.logger:
            self.logger.info("utils.interface.rabbitmq", message="Trying to connect into rabbitmq")
        try:
            if self.exchange_dlx and self.queue_dl and self.routing_key_dl:
                arguments = {
                    "x-dead-letter-exchange": self.exchange_dlx,
                    "x-dead-letter-routing-key": self.routing_key_dl,
                }
            else:
                arguments = {}

            self.channel.queue_declare(queue=self.queue, durable=True, arguments=arguments)
            self.channel.queue_bind(self.queue, self.exchange, routing_key=self.routing_key)
            # Turn on delivery confirmations
            self.channel.confirm_delivery()

        except Exception as err:
            raise err


