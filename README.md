# mongo db + flask

config.py file to be initialised in root directory:
```
class Config:
  SECRET_KEY = <secret_key>
  MONGODB_SETTINGS = {
    'db': <db_name>,
    'host': <mongo_uri>,
  }
```
