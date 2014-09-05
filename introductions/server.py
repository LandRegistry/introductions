from introductions import app, db
from introductions.models import Conveyancer, Client
from flask import request, Response
from flask_negotiate import consumes
import json
import string
import random
import datetime

@app.route('/')
def index():
    return "OK"

@app.route('/relationship', methods=['POST'])
def add_relationship():
    if request.method == 'POST':

        title_number = request.json.get("title_number")
        conveyancer_lrid = request.json.get("conveyancer_lrid")
        clients = request.json.get("clients")

        if title_number and conveyancer_lrid:

            code = code_generator()

            app.logger.info("code: %s" % (json.dumps(code)))

            conveyancer = Conveyancer()
            conveyancer.code = code
            conveyancer.lrid = conveyancer_lrid
            conveyancer.title_number = title_number
            db.session.add(conveyancer)
            db.session.commit()

            for client_lrid in clients:
                client = Client()
                client.lrid = client_lrid
                client.code = code
                db.session.add(client)

            db.session.commit()

            data = {"code" : code}

            app.logger.info("response: %s" % (json.dumps(data)))

            response = Response(response=json.dumps(data),
                    status=200,
                    mimetype="application/json")

            return response
        else:
            return Response("title_number or conveyancer_lrid field not found", status=400)


@app.route('/confirm', methods=['POST'])
def confirm_relationship():

    code = request.json.get("code")

    if code:
      client_lrid = request.json.get("client_lrid")

      client = Client.query.filter_by(lrid=client_lrid, code=code).first()

      if client:
        client.confirmed = datetime.datetime.now()
        db.session.add(client)
        db.session.commit()
        return Response("Client confirmed", status=200)
      else:
        return Response("No client found for lrid and code combination", status=400)
    else:
      return Response("Field code found", status=400)

def code_generator(size=4, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))
