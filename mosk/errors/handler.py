from flask import render_template
from werkzeug.exceptions import HTTPException
from . import errors

@errors.app_errorhandler(Exception)
def error_handler(error):
    code = 500
    if isinstance(error, HTTPException):
        code = error.code
    return render_template('error.html', error=error), code
