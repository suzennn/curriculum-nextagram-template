from models.base_model import BaseModel
from models.user import User
from flask_login import UserMixin
import peewee as pw

class Follow(UserMixin,BaseModel):
    user_id = pw.ForeignKeyField(User,backref='followers')
    follower_id = pw.ForeignKeyField(User,backref='users')
