from introductions import app, db
from flask import request, Response, jsonify
from models import Conveyancer, Token
from services.search_api import get_property_by_title_number

import json
import string
import random
import datetime
import uuid


@app.route('/')
def index():
    return "OK"


@app.route('/relationship', methods=['POST'])
def add_relationship():
    if request.method == 'POST':

        title_number = request.json.get("title_number")
        conveyancer_lrid = uuid.UUID(request.json.get("conveyancer_lrid"))
        clients = request.json.get("clients")
        task = request.json.get("task")
        conveyancer_name = request.json.get("conveyancer_name")
        conveyancer_address = request.json.get("conveyancer_address")

        if title_number and conveyancer_lrid:

            code = code_generator()

            app.logger.info("code: %s" % (json.dumps(code)))
            query = db.session.query(Conveyancer).filter(Conveyancer.lrid == conveyancer_lrid).first()

            if query is None:
                conveyancer = Conveyancer()
                conveyancer.lrid = conveyancer_lrid
                conveyancer.name = conveyancer_name
                conveyancer.address = conveyancer_address
                db.session.add(conveyancer)
                db.session.commit()

            token = Token()
            token.code = code
            token.conveyancer_lrid = conveyancer_lrid
            token.task = task
            token.title_number = title_number
            token.client_details = json.dumps(clients)
            db.session.add(token)

            db.session.commit()

            data = {"code": code}

            app.logger.info("response: %s" % (json.dumps(data)))

            response = Response(response=json.dumps(data),
                                status=200,
                                mimetype="application/json")

            return response
        else:
            return Response("title_number or conveyancer_lrid field not found", status=400)


@app.route('/confirm', methods=['POST'])
def confirm_relationship():
    app.logger.info("confirm request:: %s" % request.get_json())
    code = request.json["code"]

    if code:
        token = Token.query.filter_by(code=code).first()

        if token:
            token.confirmed = datetime.datetime.now()

            db.session.add(token)
            db.session.commit()
            conveyancer = Conveyancer.query.filter_by(lrid=token.conveyancer_lrid).first()
            return jsonify({'conveyancer_name':conveyancer.name})
        else:
            return Response("No client found for lrid and code combination", status=400)
    else:
        return Response("Field code found", status=400)


@app.route('/details/<token>')
def get_relationship(token):
    client_array = []
    response_json = None
    conveyancer_json = None
    title_details = None
    task = None

    if token:
        # get relationship details
        token_details = db.session.query(Token).filter(Token.code == token).first()

        if token_details:
            task = token_details.task
            title_number = token_details.title_number

            client_details_json = json.loads(token_details.client_details)

            for client in client_details_json:
                # client_json['clients'].append(client_details_json)
                client_json = {"lrid": client['lrid'],
                               "name": client['name'],
                               "address": client['address'],
                               "tel_no": client['tel_no'],
                               "email": client['email'],
                               "DOB": client['DOB']}
                if 'completed' in client:
                    client_json['completed'] = client['completed']

                client_array.append(client_json)

            conveyancer_details = db.session.query(Conveyancer).filter(
                Conveyancer.lrid == token_details.conveyancer_lrid).first()

            if conveyancer_details:
                lrid_str = str(conveyancer_details.lrid)

                conveyancer_json = {"lrid": lrid_str,
                                    "name": conveyancer_details.name,
                                    "address": conveyancer_details.address}

                title_details = get_property_by_title_number(token_details.title_number)

        response_json = {"conveyancer_lrid": conveyancer_json['lrid'],
                         "conveyancer_name": conveyancer_json['name'],
                         "conveyancer_address": conveyancer_json['address'],
                         "task": task,
                         "title_number": title_number,
                         "clients": [],
                         "property_no": title_details['property']['address']['address_line_1'],
                         "property_road": title_details['property']['address']['address_line_2'],
                         "property_town": title_details['property']['address']['city'],
                         "property_postcode": title_details['property']['address']['postcode'],
                         "geometry": title_details['extent']
        }

    return json.dumps(__add_client(response_json, client_array))


def __add_client(response_json, client_array):
    """
    :rtype : JSON
    """
    for client in client_array:
        response_json['clients'].append(client)

    return response_json


def code_generator(size=4, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))
