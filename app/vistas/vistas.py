from modelos.modelos import ( Evento, EventoSchema, db)
from datetime import datetime, timedelta
import hashlib
from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource
import os
import requests
import uuid


evento_schema = EventoSchema()

def generate_uuid():
    uid = uuid.uuid4()
    parts = str(uid).split('-')
    return parts[0]


class VistaHealthCheck(Resource):
    def get(self):
        return {"message": "OK", "code": 200}, 200
    
class VistaEvento(Resource):
    def get(self):
        eventos = Evento.query.all()
        eventos = evento_schema.dump(eventos, many=True)
        return {"message": "OK", "content": eventos, "code":200}, 200
    
    def post(self):
        data = request.get_json()
        data['id'] = generate_uuid()
        data['createdAt'] = datetime.now()
        data['updatedAt'] = datetime.now()
        evento = Evento(**data)
        db.session.add(evento)
        db.session.commit()
        return {"message": "Evento creado", "code": 201, "content": evento_schema.dump(evento)}, 201

class VistaEventoID(Resource):
    def put(self, evento_id):
        data = request.get_json()
        evento = Evento.query.filter_by(id=evento_id).first()
        if evento is None:
            return {"message": "Evento no encontrado", "code": 404}, 404
        
        # Cambios de campos
        if evento.event_name != data['event_name']:
            evento.event_name = data['event_name']
        if evento.event_description != data['event_description']:
            evento.event_description = data['event_description']
        if evento.event_location != data['event_location']:
            evento.event_location = data['event_location']
        if evento.event_type != data['event_type']:
            evento.event_type = data['event_type']
        if evento.link != data['link']:
            evento.link = data['link']

        evento.updatedAt = datetime.now()
        db.session.commit()
        return {"message": "Evento actualizado", "code": 200, "content": evento_schema.dump(evento)}, 200
    
    def delete(self, evento_id):
        evento = Evento.query.filter_by(id=evento_id).first()
        if evento is None:
            return {"message": "Evento no encontrado", "code": 404}, 404
        db.session.delete(evento)
        db.session.commit()
        return {"message": "Evento eliminado", "code": 200, "content": evento_schema.dump(evento)}, 200