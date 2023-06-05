from logging import Logger
from flask import current_app

from marshmallow import ValidationError

from .repositories import JobsSQLAlchemyRepository
from .schemas import CreateJobOutput, PaginationJobsOutput, JobSchema
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
        data = self.validate(schema_input=schema_input, input_params=input_params)
        data = self.update_payload_with_user_data(data=data, user_id=kwargs['user_id'], user_email=kwargs['user_email'])
        model = self.save(data=data)
        output = self.__to_output(job=model)
        self.send_user_to_queue(model=output, use_queue=kwargs['use_queue'])

        self.repo.close()
        return output


class GetJobsPaginatedUseCase:
    """
    Classe para buscar os jobs por usuário
    """

    def __init__(self, repo: JobsSQLAlchemyRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def __to_output(self, pagination):
        # Realizo um dump dos dados de acordo com o modelo salvo
        job_schema = JobSchema(many=True)
        jobs = job_schema.dump(pagination.items)

        result = {
            "items": jobs,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
            "next_num": pagination.next_num,
            "prev_num": pagination.prev_num,
        }

        if self.logger:
            self.logger.info("get_jobs_paginated.job.usecase", message="Render job output")

        return result

    def fetch(self, *_, **kwargs):
        try:
            creator = kwargs['creator_id']
            page = kwargs['page']
            per_page = kwargs['per_page']
            pagination = self.repo.get_jobs_paginated_by_user(
                creator_id=creator, page_id=page, page_size=per_page
            )

            if self.logger:
                self.logger.info("get_jobs_paginated.job.usecase", message="Jobs fetched")

            return pagination

        except Exception as err:
            if self.logger:
                self.logger.info("get_jobs_paginated.job.usecase", message="Jobs pagination not fetched. Strange error")

            raise err

    def execute(self, **kwargs):
        pagination = self.fetch(**kwargs)
        output = self.__to_output(pagination=pagination)
        self.repo.close()
        return output



class GetJobUseCase:
    """
    Classe para buscar um job por usuário
    """

    def __init__(self, repo: JobsSQLAlchemyRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def __to_output(self, model):
        # Realizo um dump dos dados de acordo com o modelo salvo
        job_schema = JobSchema()
        result = job_schema.dump(model)

        if self.logger:
            self.logger.info("get_job.job.usecase", message="Render job output")

        return result

    def get(self, *_, **kwargs):
        try:
            creator = kwargs['creator_id']
            job = kwargs['job_id']

            model = self.repo.get_job_by_id(creator_id=creator, job_id=job)

            if self.logger:
                self.logger.info("get_job.job.usecase", message="Jobs fetched")

            return model

        except Exception as err:
            if self.logger:
                self.logger.info("get_job.job.usecase", message="Get Job. Strange error")

            raise err

    def execute(self, **kwargs):
        model = self.get(**kwargs)
        output = self.__to_output(model=model)
        self.repo.close()
        return output
