# Python Modules

from app.api.web import web
from app.api.local import local
import sys
import os

# Flask Modules

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Loading environment variables

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.getenv('BASEDIR'))  # adding project app root

# Blueprint Imports


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Blueprints registering

app.register_blueprint(local, url_prefix='/local')
app.register_blueprint(web, url_prefix='/web')

# Database configuration

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login Manager

login_manager = LoginManager()
login_manager.init_app(app)

# Views and models imports

from app.classes.models.user import User, LabTech
from app.classes.models.timeslot import Event, TimeSlot 
from app.classes.models.request import SwapRequest, UserRequest
from app.classes.models.clockin import ClockInEntry, TemporarySwap
