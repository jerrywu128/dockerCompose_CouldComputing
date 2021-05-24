from flask import Flask, render_template, request, jsonify, make_response, send_from_directory, redirect, url_for
import json
#from flask import request
import database2 as db
import logging
import warnings

from flasgger import Swagger
from flasgger import swag_from

app = Flask(__name__)

swagger = Swagger(app)

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
warnings.filterwarnings("ignore", category=DeprecationWarning) 


@app.route('/post_helloworld', methods=['POST'])

def get_hello_world():
    jsonobj = request.get_json(silent=True)
    token = json.dumps(jsonobj['token']).replace("\"", "")
    db.insert(token)
    return token

@app.route('/list_user', methods=['GET'])
@swag_from('apidocs/api_list_user.yml')
def create_user():


    # reture requests
    res = dict()
    res['username_1'] = 'Alice'
    res['username_2'] = 'Bob'
    res['username_3'] = 'Cindy'
    res = make_response(jsonify(res), 200)
    return res

@app.route('/test2')
def index():
    return 'Hello, World Web App with Py Flask!'

if __name__ =='__main__':
    app.run()
