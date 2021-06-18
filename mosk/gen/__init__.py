from flask import Blueprint

gen = Blueprint(
    'gen',
    __name__,
    static_folder='static',
    static_url_path='/gen/static'
)

from mosk.gen import views
