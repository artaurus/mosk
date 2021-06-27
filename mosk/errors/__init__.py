from flask import Blueprint

errors = Blueprint(
    'errors',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/errors/static',
)

from mosk.errors import handler
