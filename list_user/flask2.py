from flask import Flask, render_template, request, jsonify, make_response, send_from_directory, redirect, url_for
import json
from flask_pymongo import PyMongo
import logging
import warnings

from flasgger import Swagger
from flasgger import swag_from

app = Flask(__name__)

swagger = Swagger(app)

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
warnings.filterwarnings("ignore", category=DeprecationWarning) 

mongo = PyMongo(app, uri="mongodb://rs2:27042/test")



@app.route('/list_user', methods=['GET'])
@app.route('/', methods=['GET'])
@swag_from('apidocs/api_list_user.yml')
def list_user():
    users = mongo.db.col.find({})
    
    return render_template('list.html',users=users)
  

if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5001)
