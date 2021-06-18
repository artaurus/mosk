from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from mosk.config import Config
from mosk.manager import UserManager

app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
um = UserManager(app)

from mosk.gen import gen
from mosk.users import users
from mosk.errors import errors
app.register_blueprint(gen)
app.register_blueprint(users)
app.register_blueprint(errors)
