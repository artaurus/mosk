from mongoengine.document import Document
from mongoengine.fields import StringField, EmailField

class User(Document):
    name = StringField(required=True, min_length=3, max_length=20)
    email = EmailField(required=True, unique=True, min_length=3, max_length=40)
    # requires js max_length validation
    password = StringField(required=True, min_length=3, max_length=100)
    meta = {'collection': 'users'}

class Login(Document):
    email = EmailField(required=True, min_length=3, max_length=40)
    password = StringField(required=True, min_length=3, max_length=20)

class ModifyProfile(Document):
    name = StringField(required=True, min_length=3, max_length=20)
    email = EmailField(required=True, unique=True, min_length=3, max_length=40)
