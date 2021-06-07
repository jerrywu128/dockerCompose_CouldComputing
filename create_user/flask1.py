from flask import Flask, render_template, request, jsonify, make_response, json, send_from_directory, redirect, url_for
#import json
#from flask import request
#import publisher as pu
import pika
import logging
import warnings
import base64

from flasgger import Swagger
from flasgger import swag_from

app = Flask(__name__)

swagger = Swagger(app)

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
warnings.filterwarnings("ignore", category=DeprecationWarning) 

@app.route('/create_user', methods=['GET','POST'])
@app.route('/', methods=['GET','POST'])
@swag_from('apidocs/api_create_user.yml')
def create_user():
    if request.method == 'POST':
        username=request.values['username']
        password=request.values['password']
        if (username=="")or(password==""):
           return "<h1>input error!</h1>"
        else:   
            epassword = base64.b64encode(password.encode('utf-8')).decode()
    # retrive post body
        #jsonobj = request.get_json(silent=True)
        #username = json.dumps(jsonobj['username']).replace("\"", "")
        #password = json.dumps(jsonobj['password']).replace("\"", "")

            logging.info('username:', username)
            logging.info('password:', epassword)

            message = dict()
            message['username'] = username
            message['password'] = epassword

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
        #res = dict()
        #res['success'] = True
        #res['message'] = 'Create user successed, your username=' + username 
        #res = make_response(jsonify(res), 200) 
            return render_template('create.html',mes='Create user successed, your username='+username)
        #return res
    else:
        return render_template('create.html',mes="")

#    return 'test'

#@app.route('/')
#def index():
#    return '''<form method="post" action="/create_user">
#    <label for="username">username:</label>
#      <input type="text" id="username" name="username">
#    <label for="password">password:</label>
#      <input type="password" id="password" name="password">
#      <button type="submit">sign up</button>
#    </form>'''

if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)

