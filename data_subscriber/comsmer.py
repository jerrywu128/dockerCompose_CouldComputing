import pika
import time
import pymongo
import logging
import warnings

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
warnings.filterwarnings("ignore", category=DeprecationWarning)

client = pymongo.MongoClient("mongodb://rs1:27041/")
modb = client['test']
mocol = modb['col']

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

def callback(ch, method, properties, body):
    
    message = body.decode("utf-8")
    logging.info('receive messages:' + message  )
    time.sleep(body.count(b'.'))
 
    dimessage=eval(message)
    x = mocol.insert_one(dimessage)
    ch.basic_ack(delivery_tag=method.delivery_tag)
  
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue',on_message_callback=callback)
channel.start_consuming()

