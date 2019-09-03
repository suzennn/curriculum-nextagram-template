from models.base_model import BaseModel
from models.user import User
from flask_login import UserMixin
import peewee as pw

class Follow(UserMixin,BaseModel):
    user = pw.ForeignKeyField(User,backref='follows')
    user_follow = pw.ForeignKeyField(User,backref='followers')
