from flask import redirect, request, url_for
from flask_bcrypt import Bcrypt

class LoginHandler:
    def __init__(self, app=None):
        self._app = None
        self._path = None
        if app:
            self.init_app(app)
        self.reset_user()
        self.bcrypt = Bcrypt()

    def init_app(self, app):
        self._app = app.name
        try:
            self._path = app.config['USER_PATH']
        except KeyError:
            pass
        self.bcrypt.init_app(app)

    def status(self):
        return bool(self._user)

    def encrypt(self, password):
        return self.bcrypt.generate_password_hash(password).decode('utf-8')

    def _write_json(self, user=None):
        if not self._path:
            if self._app:
                self._path = self._app + url_for('users.static', filename='js/user.json')
            else:
                return
        try:
            with open(self._path, 'w') as file:
                if user:
                    file.write(user.to_json())
                else:
                    file.write('{}')
        except:
            pass

    def get_user(self):
        return self._user

    def set_user(self, user):
        if not self.status():
            try:
                del user.password
            except AttributeError:
                pass
            self._user = user
            self._write_json(user)

    def reset_user(self):
        self._user = {}
        self._write_json()

    def authenticate(self, user, password):
        if user and self.bcrypt.check_password_hash(user['password'], password):
            self.set_user(user)

    def access_required(self, func):
        def wrapper(*args, **kwargs):
            if not self.status():
                # need fixing for more blueprints
                return redirect(url_for('users.login', next=url_for('users.'+func.__name__)[1:]))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper

    def access_denied(self, func):
        def wrapper(*args, **kwargs):
            if self.status():
                return redirect('/')
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
