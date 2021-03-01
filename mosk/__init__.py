from flask import Flask
from flask_mongoengine import MongoEngine
from mosk.config import Config
from mosk.login import LoginHandler

db = MongoEngine()
log = LoginHandler()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

from mosk import views
