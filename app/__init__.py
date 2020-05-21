# Python Modules

import sys
import os
from datetime import timedelta

# Application Modules


# Flask Modules

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt import JWT, _default_jwt_payload_handler

# Loading environment variables

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.getenv('APP'))  # adding project app root


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# Database configuration

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# JWT Configuration

from app.classes.controllers.access_controller import AccessController 

app.config['JWT_AUTH_URL_RULE'] = '/web/auth/login' 
app.config['JWT_AUTH_USERNAME_KEY'] = 'uwiIssuedID' 
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)
jwt = JWT(app, AccessController.authenticate, AccessController.identity)

# Views and models imports

from app.classes.models.user import User, LabTech
from app.classes.models.timeslot import Event, TimeSlot 
from app.classes.models.request import SwapRequest, UserRequest
from app.classes.models.clockin import ClockInEntry, TemporarySwap

# Blueprints registering

from app.api.web import web
from app.api.local import local
from app.api.default import default

app.register_blueprint(default, url_prefix='/default')
app.register_blueprint(local, url_prefix='/local')
app.register_blueprint(web, url_prefix='/web')
