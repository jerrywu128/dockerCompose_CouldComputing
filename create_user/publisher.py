import pika
import sys

def pu(re):
    connection = pika.BlockingConnection( pika.ConnectionParameters(host='172.21.0.1'))

    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

   # message = ' '.join(sys.argv[1:])or "Hello World!"
    message = re
    channel.basic_publish(
         exchange='',
         routing_key='hello',
         body=message

    )
    print(" [x] Sent %r" % message)
    connection.close()
#pu("hello")
