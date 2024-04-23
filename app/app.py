from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
import os
from modelos.modelos import db
from vistas import VistaHealthCheck, VistaEvento, VistaEventoID
import uuid

def generate_uuid():
    uid = uuid.uuid4()
    parts = str(uid).split('-')
    return parts[0]


#export DB_HOST=databasesportapp.cvweuasge1pc.us-east-1.rds.amazonaws.com DB_USER=admin DB_DATABASE=db_event DB_PASSWORD=123456789
#export DATABASE_URL=mysql+pymysql://admin:123456789@databasesportapp.cvweuasge1pc.us-east-1.rds.amazonaws.com/db_event
#export DATABASE_URL=
# DB_HOST = os.environ.get('DB_HOST')
# DB_USER = os.environ.get('DB_USER')
# DB_DATABASE = os.environ.get('DB_DATABASE')
# DB_PASSWORD = os.environ.get('DB_PASSWORD')

DATABASE_URI = os.environ['DATABASE_URL'] 
if DATABASE_URI is None or DATABASE_URI == '':
    new_uuid = generate_uuid()
    DATABASE_URI = f"sqlite:///test_event_{new_uuid}.db"

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
api.add_resource(VistaEventoID, '/eventos/<string:evento_id>')


jwt = JWTManager(app)

print(' * EVENT MANAGEMENT corriendo ----------------')

if __name__=='__main__':
    app.run(port=5001)
