from flask import Flask
from flask_mongoengine import MongoEngine
from .config import Config
from .login import LoginHandler

db = MongoEngine()
log = LoginHandler()

def init_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    log.init_app(app)

    with app.app_context():
        from .gen import gen
        from .users import users
        from .errors import errors
        app.register_blueprint(gen)
        app.register_blueprint(users)
        app.register_blueprint(errors)

        return app
