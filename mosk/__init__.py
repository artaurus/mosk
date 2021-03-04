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
        from mosk.gen import gen
        from mosk.users import users
        app.register_blueprint(gen)
        app.register_blueprint(users)

        return app
