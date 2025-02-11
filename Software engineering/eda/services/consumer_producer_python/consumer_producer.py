import time
import pika

def callback(ch, method, properties, body):
    time.sleep(1)
    print(f" [Python consumer_producer] Received: {body.decode()}")
    ch.basic_publish(exchange='choreography_exchange', routing_key='', body='Landmark Details Updated')
    print(" [Python consumer_producer] Sent 'Landmark Details Updated'")
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='fanout_exchange', exchange_type='fanout')
queue = channel.queue_declare(queue='', durable=True)
channel.queue_bind(exchange='fanout_exchange', queue=queue.method.queue)

channel.exchange_declare(exchange='choreography_exchange', exchange_type='fanout')

channel.basic_consume(queue=queue.method.queue, on_message_callback=callback, auto_ack=False)
print(' [Python consumer_producer] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
