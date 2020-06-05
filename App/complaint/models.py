from app import db
from user.model import User

class Complaint(db.Document):
    name = db.StringField(requiered=True)
    place = db.StringField(requiered=True)
    location = db.PointField(required=True)
    complaint_photo = db.StringField()
    description = db.StringField(required=True)
    complainer = db.ObjectIdField(requiered=True)
    cancel = db.BooleanField(default=False)
    follow = db.ListField(db.ReferenceField(User))
    



    