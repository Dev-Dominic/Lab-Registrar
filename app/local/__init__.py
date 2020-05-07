# Python Modules
import os

# Flask Modules

from flask import Blueprint

local = Blueprint('local', __name__, static_folder='static')
from . import views
