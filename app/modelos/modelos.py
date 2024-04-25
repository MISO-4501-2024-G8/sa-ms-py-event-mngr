from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Evento(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.String(255), primary_key=True)
    event_name = db.Column(db.String(255))
    event_description = db.Column(db.String(500))
    event_location = db.Column(db.String(255))
    event_type = db.Column(db.String(255))
    sport = db.Column(db.String(255))
    link = db.Column(db.String(500))
    event_date = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)



class EventoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Evento
        include_relationships = True
        load_instance = True