from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
import os
from modelos.modelos import db
from vistas import VistaHealthCheck, VistaEvento


#export DB_HOST=databasesportapp.cvweuasge1pc.us-east-1.rds.amazonaws.com DB_USER=admin DB_DATABASE=db_event DB_PASSWORD=123456789

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_DATABASE = os.environ.get('DB_DATABASE')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

DATABASE_URI = os.environ['DATABASE_URL'] 
if DATABASE_URI is None or DATABASE_URI == '':
    DATABASE_URI = 'sqlite:///test_event.db'

print(' * DATABASE_URI: ')
print(DATABASE_URI)

app=Flask(__name__) # NOSONAR
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'MISO-4501-2024-G8'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=120)
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaHealthCheck, '/')
api.add_resource(VistaEvento, '/eventos')

jwt = JWTManager(app)

print(' * EVENT MANAGEMENT corriendo ----------------')

if __name__=='__main__':
    app.run(port=5001)
