#modelo bd
from app import db
import datetime

class User(db.Document):
    username = db.StringField(required=True)
    name = db.StringField(required=True)
    lastname = db.StringField(required=True)
    city = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    created = db.DateTimeField(default=datetime.datetime.now)