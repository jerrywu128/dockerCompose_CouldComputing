from flask import Flask, render_template, request, jsonify, make_response, json, send_from_directory, redirect, url_for
#import json
#from flask import request
#import publisher as pu
import pika
import logging
import warnings

from flasgger import Swagger
from flasgger import swag_from

app = Flask(__name__)

swagger = Swagger(app)

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
warnings.filterwarnings("ignore", category=DeprecationWarning) 

@app.route('/create_user', methods=['POST'])
@app.route('/')
@swag_from('apidocs/api_create_user.yml')
def create_user():

    # retrive post body
    jsonobj = request.get_json(silent=True)
    username = json.dumps(jsonobj['username']).replace("\"", "")
    password = json.dumps(jsonobj['password']).replace("\"", "")

    logging.info('username:', username)
    logging.info('password:', password)

    message = dict()
    message['username'] = username
    message['password'] = password

    # push username and password
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    #message = ' '.join(sys.argv[1:]) or "NPTU Cloud Computing"

    message = json.dumps(message)
    logging.info('message:', message)

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()

    # reture requests
    res = dict()
    res['success'] = True
    res['message'] = 'Create user successed, your username=' + username
    res = make_response(jsonify(res), 200)
    return res
'''
def get_hello_world():
    jsonobj = request.get_json(silent=True)
    token = json.dumps(jsonobj['token']).replace("\"", "")
    pu.pu(token)
    return token
'''
@app.route('/')
def index():
    return 'Hello, World Web App with Python Flask!'

if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5000)

