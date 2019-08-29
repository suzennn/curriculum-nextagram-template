from models.base_model import BaseModel
from models.user import User
from flask_login import UserMixin
import peewee as pw

class Images(UserMixin,BaseModel):
    store = pw.ForeignKeyField(User,backref='users')
    images = pw.CharField(null=True)
