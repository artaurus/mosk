# mosk (mongo db + flask) user portal

initialise config.py within the mosk subdirectory:
```
# /mosk/config.py
class Config:
  SECRET_KEY = <secret_key>
  MONGODB_SETTINGS = {
    'db': <db_name>,
    'host': <mongo_uri>,
  }
```
