from mosk import db

class User(db.Document):
    name = db.StringField(required=True, min_length=3, max_length=25)
    email = db.EmailField(required=True, min_length=3, max_length=40, unique=True)
    password = db.StringField(required=True, min_length=3, max_length=100)

    meta = {'collection': 'users',
            'indexes': [{'fields': ['$name', '$email'],
                        'default_language': 'english',
                        'weights': {'name':10, 'email':4}
                        }]
            }
