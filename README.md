# mosk (mongo db + flask) user portal

initialise config.py within the mosk subdirectory:
```
# /mosk/config.py
class Config:
  SECRET_KEY = <secret_key>
  FLASK_APP = 'wsgi.py'
  STATIC_FOLDER = 'static'
  TEMPLATES_FOLDER = 'templates'
  MONGODB_SETTINGS = {
    'db': <db_name>,
    'host': <mongo_uri>,
  }
```
