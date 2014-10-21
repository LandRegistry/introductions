from sqlalchemy.exc import IntegrityError
from introductions import app, db
from flask import request, Response, jsonify
from models import Conveyancer, Relationship
from introductions.service import save_relationship, get_converyancer, update_relationship, get_relationship_by_token

import json
import string
import random
import datetime
import uuid


@app.route('/')
def index():
    return "OK", 200


@app.route('/relationship', methods=['POST'])
def add_relationship():
    try:
        token = save_relationship(request.json)
        if token:
            return jsonify({'token': token})
        else:
            return Response("Conveyancer does not exist", 404)
    except KeyError as e:
        return Response("Key error missing data in request. %s" % e.message, status=400)
    except IntegrityError as e:
        return Response("Integrity error relationship already exists. %s" % e.message, status=400)



@app.route('/confirm', methods=['POST'])
def confirm_relationship():
    app.logger.info("confirm request:: %s" % request.get_json())
    try:
        token = request.json["token"]
        client_lrid = uuid.UUID(request.json["client_lrid"])
    except Exception as e:
        app.logger.error("Confirm relationship failed: %s" % e.message)
        return Response("Invalid input", status=400)

    if token and client_lrid:
        conveyancer_lrid = update_relationship(token, client_lrid)
        if conveyancer_lrid:
            conveyancer = get_converyancer(conveyancer_lrid)
            return jsonify({'conveyancer_name': conveyancer.name})
        else:
            return Response("Unable to confirm relationship, the token or client lr_id does not match in the relationship.", status=400)

    else:
        return Response("Token is missing from the request", status=400)


@app.route('/details/<token>')
def get_relationship(token):
    if token:
        # get relationship and conveyancer details
        relationship = get_relationship_by_token(token)
        if relationship:
            return json.dumps(relationship)

    return Response("Token is missing from the request", status=404)
