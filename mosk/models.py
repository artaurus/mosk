from mosk import db

class User(db.Document):
    name = db.StringField(required=True, min_length=3, max_length=20)
    email = db.EmailField(required=True, unique=True, min_length=3, max_length=40)
    password = db.StringField(required=True, min_length=3, max_length=100)
    meta = {'collection': 'users'}
