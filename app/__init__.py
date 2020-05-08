# Python Modules

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

sys.path.append(os.getenv('BASEDIR')) # adding project app root

# Blueprint Imports

from app.local import local
from app.web import web

app = Flask(__name__) 

# Blueprints registering

app.register_blueprint(local, url_prefix='/local')
app.register_blueprint(web, url_prefix='/web')

# Database configuration

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(app)
migrate = Migrate(db)

# Login Manager

login_manager = LoginManager()
login_manager.init_app(app)
