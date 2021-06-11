from flask import render_template
from werkzeug.exceptions import HTTPException
from mosk.errors import errors

@errors.app_errorhandler(HTTPException)
def error_handler(error):
    return render_template(
        'error.html',
        title=error.name,
        error=error
    ), error.code
