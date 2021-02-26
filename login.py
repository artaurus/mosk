from functools import wraps
from flask import redirect, request, url_for

class LoginHandler:
    def __init__(self):
        self.reset_user()

    def get_user(self):
        return self.user

    def set_user(self, name, email):
        self.log = True
        self.user = {
            'name': name,
            'email': email,
        }

    def reset_user(self):
        self.log = False
        self.user = {
            'name': '',
            'email': '',
        }

    def login_required(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self.log:
                return redirect(url_for('login', next=request.url))
            return func(*args, **kwargs)
        return wrapper
