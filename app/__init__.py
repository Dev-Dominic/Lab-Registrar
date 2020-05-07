# Python Modules

# Flask Modules
from flask import Flask

# Blueprint Imports
from .local import local
from .web import web

app = Flask(__name__)

# Blueprints registering
app.register_blueprint(local, url_prefix='/local')
app.register_blueprint(web, url_prefix='/web')
