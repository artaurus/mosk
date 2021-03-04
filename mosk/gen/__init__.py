from flask import Blueprint

gen = Blueprint('gen', __name__)

from . import views
