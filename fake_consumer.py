import time
import pika

queue_name = 'job_created'

def get_channel():
    # connect and get channel
    parameters = pika.URLParameters('amqp://guest:guest@localhost:5672')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    # declare queue with max priority
    arguments = {
        "x-dead-letter-exchange": 'create-job-use-case-dlq',
        "x-dead-letter-routing-key": 'job_created_dlq',
        "x-max-priority": 5
    }
    channel.queue_declare(
        queue=queue_name, durable=True, arguments=arguments
    )
    return channel

if __name__ == '__main__':

    channel = get_channel()


    # get messages
    while True:
        method_frame, header_frame, body = channel.basic_get(queue_name)
        if method_frame:
            channel.basic_ack(method_frame.delivery_tag)
            print("Recevied:", body)
        time.sleep(0.1)
