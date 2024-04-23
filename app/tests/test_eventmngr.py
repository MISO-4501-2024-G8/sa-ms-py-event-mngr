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

os.environ['DATABASE_URL'] = 'sqlite:///eventm.db'

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

