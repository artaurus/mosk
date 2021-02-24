from mongoengine.document import Document
from mongoengine.fields import StringField, EmailField

class User(Document):
    name = StringField(required=True, min_length=3, max_length=20)
    email = EmailField(required=True, min_length=3, max_length=40)
    meta = {'collection': 'users'}
