from flask import Flask, render_template, request, jsonify, make_response, send_from_directory, redirect, url_for
import json
from flask_pymongo import PyMongo
import logging
import warnings
import base64

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://rs3:27043/test")



@app.route('/login', methods=['GET','POST'])
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username=request.values['username']
        password=request.values['password']
        if (username=="")or(password==""):
           return "<h1>input error!</h1>"
        else:
           users = mongo.db.col.find_one({'username':username})
           if users:
               name = users['username']
               pas  = users['password'] 
               epassword = base64.b64encode(password.encode('utf-8')).decode()
           
               if (name==username)and(pas==epassword):
                   return render_template('app.html')
               else:
                   return "<h1>login error check the name or password!</h1>"    
           else:
               return "<h1>login error check the name or password!</h1>"
    else:
        return render_template('login.html')
  

if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5002,debug=True)
