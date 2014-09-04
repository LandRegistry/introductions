from introductions import app
from introductions.models import Conveyancer, Client
from flask import request, Response
from flask_negotiate import consumes
import json

@app.route('/')
def index():
    return "OK"

@app.route('/relationship', methods=['POST'])
def add_relationship():
    #TODO add conveyancer and client relationship, generate and return code
    return "relationship added"

@app.route('/confirm', methods=['POST', 'GET'])
def confirm_relationship():
    #TODO add confirmation datetime
    return "client confirmed relationship"
