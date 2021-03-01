from mosk import db

class SignUp(db.Document):
    name = db.StringField(required=True, min_length=3, max_length=20)
    email = db.EmailField(required=True, unique=True, min_length=3, max_length=40)
    password = db.StringField(required=True, min_length=3, max_length=20)

class Login(db.Document):
    email = db.EmailField(required=True, min_length=3, max_length=40)
    password = db.StringField(required=True, min_length=3, max_length=20)

class ModifyProfile(db.Document):
    name = db.StringField(required=True, min_length=3, max_length=20)
    email = db.EmailField(required=True, unique=True, min_length=3, max_length=40)
