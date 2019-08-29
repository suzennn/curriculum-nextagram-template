from models.base_model import BaseModel
from models.user import User
from flask_login import UserMixin
import peewee as pw

class Image(UserMixin,BaseModel):
    user = pw.ForeignKeyField(User,backref='images')
    path = pw.CharField(null=True)
