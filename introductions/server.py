from sqlalchemy.exc import IntegrityError
from introductions import app, db
from flask import request, Response, jsonify
from models import Conveyancer, Relationship
from introductions.service import save_relationship

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
        relationship = Relationship.query.filter_by(token=token, client_lrid=client_lrid).first()

        if relationship:
            relationship.confirmed = datetime.datetime.now()
            db.session.add(relationship)
            db.session.commit()

            conveyancer = Conveyancer.query.filter_by(lrid=relationship.conveyancer_lrid).first()

            return jsonify({'conveyancer_name': conveyancer.name})
        else:
            return Response("No client found for lrid and code combination", status=400)
    else:
        return Response("Field code found", status=400)


@app.route('/details/<token>')
def get_relationship(token):
    response_json = None
    conveyancer_json = None
    task = None

    if token:
        # get relationship details
        relationship = db.session.query(Relationship).filter(Relationship.token == token).first()

        if relationship:
            task = relationship.task
            title_number = relationship.title_number

            client_lrid = str(relationship.client_lrid)

            conveyancer_details = db.session.query(Conveyancer).filter(
                Conveyancer.lrid == relationship.conveyancer_lrid).first()

            if conveyancer_details:
                lrid_str = str(conveyancer_details.lrid)

                conveyancer_json = {"lrid": lrid_str,
                                    "name": conveyancer_details.name,
                                    "address": conveyancer_details.address}

            response_json = {"conveyancer_lrid": conveyancer_json['lrid'],
                         "conveyancer_name": conveyancer_json['name'],
                         "conveyancer_address": conveyancer_json['address'],
                         "client_lrid": client_lrid,
                         "task": task,
                         "title_number": title_number}

            return json.dumps(response_json)
        else:
            return Response("No details found for token", status=404)

def code_generator(size=4, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))
