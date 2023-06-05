import click
from flask import current_app
from flask.cli import with_appcontext


@click.command(name='createqueue')
@with_appcontext
def createqueue():
    from apps.jobs.utils import RabbitMQ
    uri = current_app.config['RABBITMQ_CONNECTION']
    connect, channel = RabbitMQ.connect(uri=uri)

    # create exchanges
    channel.exchange_declare(exchange="create-job-use-case", exchange_type='direct', durable=True)
    channel.exchange_declare(exchange="create-job-use-case-dlq", exchange_type='direct', durable=True)
    channel.exchange_declare(exchange="errors-when-create-job-use-case", exchange_type='direct', durable=True)

    # create job_created_dlq
    channel.queue_declare(queue='job_created_dlq', durable=True)
    channel.queue_bind('job_created_dlq', 'create-job-use-case-dlq', routing_key='job_created_dlq')


    # create queue job_created
    arguments = {
        "x-dead-letter-exchange": "create-job-use-case-dlq",
        "x-dead-letter-routing-key": "job_created_dlq",
        "x-max-priority": 5
    }
    channel.queue_declare(queue='job_created', durable=True, arguments=arguments)
    channel.queue_bind('job_created', 'create-job-use-case', routing_key='job_created')

    # create payload error
    channel.queue_declare(queue='payload_error', durable=True)
    channel.queue_bind('payload_error', 'errors-when-create-job-use-case', routing_key='payload')

    # create database error
    channel.queue_declare(queue='database_error', durable=True)
    channel.queue_bind('database_error', 'errors-when-create-job-use-case', routing_key='database')

    # create queue error
    channel.queue_declare(queue='queue_error', durable=True)
    channel.queue_bind('queue_error', 'errors-when-create-job-use-case', routing_key='queue')

    channel.close()
    connect.close()
