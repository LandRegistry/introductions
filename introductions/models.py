from introductions import db
from sqlalchemy.dialects.postgresql import UUID

class Conveyancer(db.Model):

    code = db.Column(db.String(), primary_key=True, nullable=False)
    lrid = db.Column(UUID(as_uuid=True), nullable=False)
    title_number = db.Column(db.String(), nullable=False)

class Client(db.Model):

    code = db.Column(db.String(), db.ForeignKey('conveyancer.code'))
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    lrid = db.Column(UUID(as_uuid=True), nullable=False)
    confirmed = db.Column(db.DateTime)
