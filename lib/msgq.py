import json
import pika

# MsgQueue
#
class MsgQueue():

    # __init__
    #
    def __init__(s, address='162.213.33.247', port=5672, exchange='kernel'):
        s.exchange_name = exchange

        params = pika.ConnectionParameters(address, port, connection_attempts=3)
        connection = pika.BlockingConnection(params)
        s.channel = connection.channel()
        s.channel.exchange_declare(exchange=s.exchange_name, type='topic')

    def listen(s, queue_name, routing_key, handler_function):
        def wrapped_handler(channel, method, properties, body):
            payload = json.loads(body)
            handler_function(payload)

        s.channel.queue_declare(queue_name, durable=True)
        s.channel.queue_bind(exchange=s.exchange_name, queue=queue_name, routing_key=routing_key)
        s.channel.basic_consume(wrapped_handler, queue=queue_name, no_ack=True)
        s.channel.start_consuming()

    def publish(s, routing_key, payload):
        message_body = json.dumps(payload)
        properties = pika.BasicProperties(delivery_mode=2)
        s.channel.basic_publish(exchange=s.exchange_name, routing_key=routing_key, body=message_body, properties=properties)

# vi:set ts=4 sw=4 expandtab:
