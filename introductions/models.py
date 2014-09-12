from introductions import db
from sqlalchemy.dialects.postgresql import UUID


class Conveyancer(db.Model):

    code = db.Column(db.String(), primary_key=True, nullable=False)
    lrid = db.Column(UUID(as_uuid=True), nullable=False)
    name = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    title_number = db.Column(db.String(), nullable=False)


class Token(db.Model):

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    code = db.Column(db.String(), db.ForeignKey('conveyancer.code'), nullable=False)
    conveyancer_lrid = db.Column(UUID(as_uuid=True), nullable=False)
    title_number = db.Column(db.String(), nullable=False)
    client_details = db.Column(db.Text, nullable=False)
    task = db.Column(db.String(), nullable=False)
    confirmed = db.Column(db.DateTime)
    expiry_date = db.Column(db.Date)