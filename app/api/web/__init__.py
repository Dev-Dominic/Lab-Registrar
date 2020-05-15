# Python Modules
import os

# Flask Modules

from flask import Blueprint

web = Blueprint('web', __name__, static_folder='static')
from . import views
