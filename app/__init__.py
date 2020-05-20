# Python Modules

import sys
import os

# Application Modules

# from app.api.web import web

# Flask Modules

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

# Loading environment variables

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.getenv('APP'))  # adding project app root

# Blueprint Imports

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Blueprints registering

# app.register_blueprint(web, url_prefix='/web')

# Database configuration
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
print(os.getenv('DATABASE_URI'))
# Login Manager

login_manager = LoginManager()
login_manager.init_app(app)

# Views and models imports

from app.classes.models.user import User, LabTech
from app.classes.models.timeslot import Event, TimeSlot 
from app.classes.models.request import SwapRequest, UserRequest
from app.classes.models.clockin import ClockInEntry, TemporarySwap


from app.api.local import local
from app.api.default import default

app.register_blueprint(default, url_prefix='/default')
app.register_blueprint(local, url_prefix='/local')
