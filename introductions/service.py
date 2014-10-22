import random
import string
import uuid
import datetime
import logging

from introductions import db
from introductions.models import Conveyancer, Relationship


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())


def save_relationship(data):
    conveyancer_lrid = data["conveyancer_lrid"]
    conveyancer = get_converyancer(conveyancer_lrid)
    if conveyancer is None:
        return None

    # get client details out (should only be 1 for now)
    # TODO: be able to handle an array of clients or do not send in the clients as an array.
    for client in data.get("clients"):
        client_lrid = uuid.UUID(client["lrid"])

    relationship = Relationship()
    relationship.token = code_generator()
    relationship.conveyancer_lrid = conveyancer_lrid
    relationship.client_lrid = client_lrid
    relationship.task = data["task"]
    relationship.title_number = data["title_number"]

    db.session.add(relationship)
    db.session.commit()

    return relationship.token


def get_converyancer(conveyancer_lrid):
    return db.session.query(Conveyancer).filter(Conveyancer.lrid == conveyancer_lrid).first()


def update_relationship(token, client_lrid):
    relationship = Relationship.query.filter_by(token=token, client_lrid=client_lrid).first()

    if relationship:
        relationship.confirmed = datetime.datetime.now()
        db.session.add(relationship)
        db.session.commit()
        return relationship.conveyancer_lrid
    else:
        logger.error("No relationship found.")
        return None


def get_relationship_by_token(token):
    relationship = db.session.query(Relationship).filter(Relationship.token == token).first()
    if relationship:
        conveyancer_details = get_converyancer(relationship.conveyancer_lrid)
        logger.info(conveyancer_details.lrid)
        if conveyancer_details:
            return {"conveyancer_lrid": str(conveyancer_details.lrid),
                    "conveyancer_name": conveyancer_details.name,
                    "conveyancer_address": conveyancer_details.address,
                    "client_lrid": str(relationship.client_lrid),
                    "task": relationship.task,
                    "title_number": relationship.title_number}
        else:
            return None
    else:
        return None


def code_generator(size=4, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))