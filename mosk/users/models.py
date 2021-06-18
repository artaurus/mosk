from mosk import db
from datetime import datetime

class User(db.Document):
    email = db.EmailField(min_length=3, max_length=254)
    password = db.StringField(min_length=3, max_length=256)
    datetime = db.DateTimeField(default=datetime.utcnow)
    verified = db.BooleanField(default=False)

    meta = {'collection': 'users'}
