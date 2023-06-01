from logging import Logger
from flask import current_app

from marshmallow import ValidationError

from .repositories import JobsSQLAlchemyRepository
from .schemas import CreateJobOutput
from .utils import RabbitMQ
from .infra import PublishCreateJobToRabbit, PublishErrorsInCreateJobUseCaseToRabbit, PublishCreateJobToSQS

class CreateJobUseCase:
    """
    Classe para criar um job
    """

    def __init__(self, repo: JobsSQLAlchemyRepository, use_queue: str, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger
        self.rabbitmq_conn = None
        self.rabbitmq_channel = None
        self.create_queue_connection(use_queue=use_queue)

    def __validate(self, schema_input, input_params):
        try:
            data = schema_input.load(input_params)
            return data

        except ValidationError as err:
            raise err

    def __to_output(self, job):
        # Realizo um dump dos dados de acordo com o modelo salvo
        schema = CreateJobOutput()
        result = schema.dump(job)
        if self.logger:
            self.logger.info("create.job.usecase", message="Render job output")

        return result

    def create_queue_connection(self, use_queue:str):
        if use_queue == 'rabbitmq':
            try:
                uri = current_app.config['RABBITMQ_CONNECTION']
                import ipdb
                ipdb.set_trace()
                self.rabbitmq_conn, self.rabbitmq_channel = RabbitMQ.connect(uri=uri)

            except Exception as err:
                raise err

        elif use_queue == 'sqs':
            try:
                # implement boto3 here
                pass
            except Exception as err:
                raise err

    def validate(self, schema_input, input_params):
        # Desserialização os dados postados ou melhor meu payload
        try:
            data = self.__validate(schema_input=schema_input, input_params=input_params)

            # By according LGPD the cpf is a sensitive data too. So is necessary to be supressed
            if self.logger:
                self.logger.info("create.job.usecase", message="Validate initial Payload")

            return data

        except ValidationError as err:
            if self.logger:
                self.logger.info("create.job.usecase", message="Schema validation failed", errors=err.messages)

            prepare_to_send = PublishErrorsInCreateJobUseCaseToRabbit(
                connection=self.rabbitmq_conn,
                channel=self.rabbitmq_channel,
                routing_key='payload',
                queue='payload_error',
            )
            prepare_to_send.run(input_params)

            raise err

    def save(self, data):
        try:
            model = self.repo.insert(data)
            if self.logger:
                self.logger.info("create.job.usecase", message="Job saved")

            return model

        except Exception as err:
            if self.logger:
                self.logger.info("create.job.usecase", message="Job not saved. Strange error")

            prepare_to_send = PublishErrorsInCreateJobUseCaseToRabbit(
                connection=self.rabbitmq_conn,
                channel=self.rabbitmq_channel,
                routing_key='database',
                queue='database_error',
            )
            prepare_to_send.run(model.to_dict())

            raise err

    def send_user_to_queue(self, model, use_queue):
        if self.logger:
            self.logger.info("create.job.usecase", use_queue=use_queue, message="Job was sent to queue")

        if use_queue is None:
            return

        if use_queue == 'rabbitmq':
            self.send_to_rabbitmq(model=model)

        if use_queue == 'sqs':
            raise NotImplementedError('this queue is not implemented yet')

    def send_to_rabbitmq(self, model):
        try:
            if self.rabbitmq_conn is None or self.rabbitmq_channel is None:
                # trying to connect again
                self.create_queue_connection('rabbitmq')

            prepare_to_send = PublishCreateJobToRabbit(
                self.rabbitmq_conn,
                self.rabbitmq_channel
            )
            prepare_to_send.run(model)

        except Exception as exc:
            prepare_to_send = PublishErrorsInCreateJobUseCaseToRabbit(
                connection=self.rabbitmq_conn,
                channel=self.rabbitmq_channel,
                routing_key='queue',
                queue='queue_error',
            )
            import ipdb
            ipdb.set_trace()
            prepare_to_send.run(model)

            raise exc

    def check_user_id(self, user_id):
        if self.logger:
            self.logger.info("create.job.command", user_id=user_id, message="User")

        if user_id is None:
            raise Exception('invalid user id')

    def check_user_email(self, user_email):
        if self.logger:
            self.logger.info("create.job.command", user_email=user_email, message="User")

        if user_email is None:
            raise Exception('invalid user email')

    def update_payload_with_user_data(self, data, user_id, user_email):
        data.update({'creator_id': user_id, 'creator_email': user_email})

        return data

    def execute(self, schema_input, input_params, kwargs):
        import ipdb
        ipdb.set_trace()
        data = self.validate(schema_input=schema_input, input_params=input_params)
        ipdb.set_trace()
        data = self.update_payload_with_user_data(data=data, user_id=kwargs['user_id'], user_email=kwargs['user_email'])
        ipdb.set_trace()
        model = self.save(data=data)
        ipdb.set_trace()
        output = self.__to_output(job=model)
        self.send_user_to_queue(model=output, use_queue=kwargs['use_queue'])
        ipdb.set_trace()
        self.repo.close()
        return output
