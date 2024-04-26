from modelos.modelos import ( Evento, EventoSchema, db)
from datetime import datetime, timedelta
import hashlib
from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource
import os
import requests
import uuid

evento_no_encontrado = "Evento no encontrado"
date_format = "%Y-%m-%d %H:%M:%S"

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
        if data['event_date'] is None:
            data['event_date'] = datetime.now()
        else:
            data['event_date'] = datetime.strptime(data['event_date'], date_format)
        
        data['id'] = generate_uuid()
        data['createdAt'] = datetime.now()
        data['updatedAt'] = datetime.now()
        evento = Evento(**data)
        db.session.add(evento)
        db.session.commit()
        return {"message": "Evento creado", "code": 201, "content": evento_schema.dump(evento)}, 201

class VistaEventoID(Resource):
    def get(self, evento_id):
        evento = Evento.query.filter_by(id=evento_id).first()
        if evento is None:
            return {"message": evento_no_encontrado, "code": 404}, 404
        return {"message": "OK", "content": evento_schema.dump(evento), "code": 200}, 200

    def put(self, evento_id):
        data = request.get_json()
        evento = Evento.query.filter_by(id=evento_id).first()
        if evento is None:
            return {"message": evento_no_encontrado, "code": 404}, 404
        
        changes = 0
        # Cambios de campos
        if evento.event_name != data['event_name']:
            evento.event_name = data['event_name']
            changes += 1
        if evento.event_description != data['event_description']:
            evento.event_description = data['event_description']
            changes += 1
        if evento.event_location != data['event_location']:
            evento.event_location = data['event_location']
            changes += 1
        if evento.event_type != data['event_type']:
            evento.event_type = data['event_type']
            changes += 1
        if evento.sport != data['sport']:
            evento.sport = data['sport']
            changes += 1
        if evento.link != data['link']:
            evento.link = data['link']
            changes += 1
        if evento.event_date != datetime.strptime(data['event_date'], date_format):
            evento.event_date = datetime.strptime(data['event_date'], date_format)
            changes += 1

        if changes == 0:
            return {"message": "No hay cambios", "code": 200}, 200
        
        evento.updatedAt = datetime.now()
        db.session.commit()
        return {"message": "Evento actualizado", "code": 200, "content": evento_schema.dump(evento)}, 200
    
    def delete(self, evento_id):
        evento = Evento.query.filter_by(id=evento_id).first()
        if evento is None:
            return {"message": evento_no_encontrado, "code": 404}, 404
        db.session.delete(evento)
        db.session.commit()
        return {"message": "Evento eliminado", "code": 200, "content": evento_schema.dump(evento)}, 200