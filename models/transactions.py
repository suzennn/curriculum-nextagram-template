from models.base_model import BaseModel
from models.user import User
from models.images import Image
from flask_login import UserMixin
import peewee as pw

class Transaction(UserMixin,BaseModel):
    user = pw.ForeignKeyField(User,backref='transactions')
    image = pw.ForeignKeyField(Image,backref='transactions')
    trans = pw.CharField(null=True)
    amount = pw.DecimalField(null=True, decimal_places="2")
