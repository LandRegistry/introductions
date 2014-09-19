from introductions import app, db
from flask import request, Response, jsonify
from models import Conveyancer, Relationship

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
    title_number = request.json.get("title_number")
    conveyancer_lrid = uuid.UUID(request.json.get("conveyancer_lrid"))
    clients = request.json.get("clients")
    task = request.json.get("task")
    conveyancer_name = request.json.get("conveyancer_name")
    conveyancer_address = request.json.get("conveyancer_address")

    app.logger.info("add relationship for title: %s with conveyancer: %s" %(conveyancer_lrid, title_number))

    if title_number and conveyancer_lrid:

        token = code_generator()

        # check to see if an instance of the conveyancer exists already
        query = db.session.query(Conveyancer).filter(Conveyancer.lrid == conveyancer_lrid).first()
        if query is None:
            conveyancer = Conveyancer()
            conveyancer.lrid = conveyancer_lrid
            conveyancer.name = conveyancer_name
            conveyancer.address = conveyancer_address
            db.session.add(conveyancer)
            db.session.commit()

        #get client details out (should only be 1 for now)
        for client in clients:
            client_lrid = uuid.UUID(client['lrid'])

        relationship = Relationship()
        relationship.token = token
        relationship.conveyancer_lrid = conveyancer_lrid
        relationship.client_lrid = client_lrid
        relationship.task = task
        relationship.title_number = title_number
        db.session.add(relationship)

        db.session.commit()

        data = {"token": token}

        response = Response(response=json.dumps(data),
                            status=200,
                            mimetype="application/json")

        return response
    else:
        return Response("title_number or conveyancer_lrid field not found", status=400)


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

def code_generator(size=4, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))
