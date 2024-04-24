import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from app import app
import json
import random
import string
from flask_restful import Api
from flask import Flask
from flask_restful import Resource
from modelos.modelos import db
from urllib.parse import urlparse

class TestVistaHealthCheck(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app = app.test_client()

    def test_health_check(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"message": "OK", "code": 200})

class TestVistaEvento(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app = app.test_client()
        print(db.engine.url)
        self.app.testing = True

    def test_get_eventos(self):
        response = self.app.get('/eventos')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"message": "OK", "content": [], "code": 200})
    
    def test_post_eventos(self):
        response = self.app.post('/eventos', json={
            "event_name": "Evento de prueba",
            "event_description": "Descripcion del evento de prueba",
            "event_location": "Ubicacion del evento de prueba",
            "event_type": "Tipo de evento de prueba",
            "sport":"Atletismo",
            "link": "https://eventodeprueba.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['message'], "Evento creado")
        self.assertEqual(json.loads(response.data)['code'], 201)
        self.assertEqual(json.loads(response.data)['content']['event_name'], "Evento de prueba")
        self.assertEqual(json.loads(response.data)['content']['event_description'], "Descripcion del evento de prueba")
        self.assertEqual(json.loads(response.data)['content']['event_location'], "Ubicacion del evento de prueba")
        self.assertEqual(json.loads(response.data)['content']['event_type'], "Tipo de evento de prueba")
        self.assertEqual(json.loads(response.data)['content']['link'], "https://eventodeprueba.com")
        self.assertIsNotNone(json.loads(response.data)['content']['id'])
        self.assertIsNotNone(json.loads(response.data)['content']['createdAt'])
        self.assertIsNotNone(json.loads(response.data)['content']['updatedAt'])
    
    def test_put_eventos(self):
        response = self.app.post('/eventos', json={
            "event_name": "Evento de prueba",
            "event_description": "Descripcion del evento de prueba",
            "event_location": "Ubicacion del evento de prueba",
            "event_type": "Tipo de evento de prueba",
            "sport":"Atletismo",
            "link": "https://eventodeprueba.com"
        })
        evento_id = json.loads(response.data)['content']['id']
        response = self.app.put(f'/eventos/{evento_id}', json={
            "event_name": "Evento de prueba 2",
            "event_description": "Descripcion del evento de prueba 2",
            "event_location": "Ubicacion del evento de prueba 2",
            "event_type": "Tipo de evento de prueba 2",
            "sport":"Ciclismo",
            "link": "https://eventodeprueba2.com"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], "Evento actualizado")
        self.assertEqual(json.loads(response.data)['code'], 200)
        self.assertEqual(json.loads(response.data)['content']['event_name'], "Evento de prueba 2")
        self.assertEqual(json.loads(response.data)['content']['event_description'], "Descripcion del evento de prueba 2")
        self.assertEqual(json.loads(response.data)['content']['event_location'], "Ubicacion del evento de prueba 2")
        self.assertEqual(json.loads(response.data)['content']['event_type'], "Tipo de evento de prueba 2")
        self.assertEqual(json.loads(response.data)['content']['link'], "https://eventodeprueba2.com")
        self.assertIsNotNone(json.loads(response.data)['content']['id'])
        self.assertIsNotNone(json.loads(response.data)['content']['createdAt'])
        self.assertIsNotNone(json.loads(response.data)['content']['updatedAt'])
        response_2 = self.app.put('/eventos/noexiste', json={
            "event_name": "Evento de prueba 2",
            "event_description": "Descripcion del evento de prueba 2",
            "event_location": "Ubicacion del evento de prueba 2",
            "event_type": "Tipo de evento de prueba 2",
            "sport":"Ciclismo",
            "link": "https://eventodeprueba2.com"
        })
        self.assertEqual(response_2.status_code, 404)
        self.assertEqual(json.loads(response_2.data)['message'], "Evento no encontrado")

        response_4 = self.app.put(f'/eventos/{evento_id}', json={
            "event_name": "Evento de prueba 2",
            "event_description": "Descripcion del evento de prueba 2",
            "event_location": "Ubicacion del evento de prueba 2",
            "event_type": "Tipo de evento de prueba 2",
            "sport":"Atletismo",
            "link": "https://eventodeprueba2.com"
        })
        self.assertEqual(response_4.status_code, 200)
        self.assertEqual(json.loads(response_4.data)['message'], "Evento actualizado")

        response_5 = self.app.put(f'/eventos/{evento_id}', json={
            "event_name": "Evento de prueba 2",
            "event_description": "Descripcion del evento de prueba 2",
            "event_location": "Ubicacion del evento de prueba 2",
            "event_type": "Tipo de evento de prueba 2",
            "sport":"Atletismo",
            "link": "https://eventodeprueba2.com"
        })
        self.assertEqual(response_5.status_code, 200)
        self.assertEqual(json.loads(response_5.data)['message'], "No hay cambios")

    
    def test_delete_eventos(self):
        response = self.app.post('/eventos', json={
            "event_name": "Evento de prueba",
            "event_description": "Descripcion del evento de prueba",
            "event_location": "Ubicacion del evento de prueba",
            "event_type": "Tipo de evento de prueba",
            "sport":"Atletismo",
            "link": "https://eventodeprueba.com"
        })
        evento_id = json.loads(response.data)['content']['id']
        response = self.app.delete(f'/eventos/{evento_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], "Evento eliminado")
        self.assertEqual(json.loads(response.data)['code'], 200)
        self.assertEqual(json.loads(response.data)['content']['event_name'], "Evento de prueba")
        self.assertEqual(json.loads(response.data)['content']['event_description'], "Descripcion del evento de prueba")
        self.assertEqual(json.loads(response.data)['content']['event_location'], "Ubicacion del evento de prueba")
        self.assertEqual(json.loads(response.data)['content']['event_type'], "Tipo de evento de prueba")
        self.assertEqual(json.loads(response.data)['content']['link'], "https://eventodeprueba.com")
        self.assertIsNotNone(json.loads(response.data)['content']['id'])
        self.assertIsNotNone(json.loads(response.data)['content']['createdAt'])
        self.assertIsNotNone(json.loads(response.data)['content']['updatedAt'])
        response_2 = self.app.delete('/eventos/noexiste')
        self.assertEqual(response_2.status_code, 404)
        self.assertEqual(json.loads(response_2.data)['message'], "Evento no encontrado")
    
    def test_get_evento(self):
        response = self.app.get('/eventos/noexiste')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data), {"message": "Evento no encontrado", "code": 404})
        response = self.app.post('/eventos', json={
            "event_name": "Evento de prueba",
            "event_description": "Descripcion del evento de prueba",
            "event_location": "Ubicacion del evento de prueba",
            "event_type": "Tipo de evento de prueba",
            "sport":"Atletismo",
            "link": "https://eventodeprueba.com"
        })
        evento_id = json.loads(response.data)['content']['id']
        response = self.app.get(f'/eventos/{evento_id}')
        self.assertEqual(response.status_code, 200)
        self.app.delete(f'/eventos/{evento_id}')

