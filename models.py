from flask_mongoengine import MongoEngine
from mongoengine import *

db = MongoEngine()


class User(db.Document):
    meta = {'collection': 'users'}
    user_name = StringField(required=True, unique=True, min_length=3)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)


class ImageUpload(db.Document):
    meta = {'collection': 'images', 'allow_inheritance': True}
    user = ReferenceField(User, required=True, unique=False)
    image = FileField(required=True)
    tags = ListField(StringField(), required=False, default=[])
    processed = BooleanField(required=False, default=False)
