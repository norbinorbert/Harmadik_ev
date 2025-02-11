import time
import pika

def callback(ch, method, properties, body):
    time.sleep(1)
    print(f" [Python consumer1] Consumer 1 received: {body.decode()}")
    
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='fanout_exchange', exchange_type='fanout')
queue = channel.queue_declare(queue='', durable=True)
channel.queue_bind(exchange='fanout_exchange', queue=queue.method.queue)

channel.basic_consume(queue=queue.method.queue, on_message_callback=callback, auto_ack=True)
print(' [Python consumer1] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
