from introductions import db
from sqlalchemy.dialects.postgresql import UUID


class Conveyancer(db.Model):

    lrid = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=True)
    address = db.Column(db.String(), nullable=True)

class Relationship(db.Model):

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    token = db.Column(db.String(), nullable=False)
    conveyancer_lrid = db.Column(UUID(as_uuid=True), db.ForeignKey('conveyancer.lrid'),nullable=False)
    client_lrid = db.Column(UUID(as_uuid=True), nullable=False)
    title_number = db.Column(db.String(), nullable=False)
    task = db.Column(db.String(), nullable=False)
    confirmed = db.Column(db.DateTime)
    expiry_date = db.Column(db.Date)
