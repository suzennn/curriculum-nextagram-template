from models.base_model import BaseModel
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
import peewee as pw
import re

class User(UserMixin,BaseModel):
    name = pw.CharField(null=False)
    email = pw.CharField(unique=True,null=False)
    username = pw.CharField(unique=True,null=False)
    password = pw.CharField(null=False)


    def validate(self):
        pattern_pwd = "(?=.*[A-Z])(?=.*[!@#$&*\^%\*\.])(?=.*[0-9])(?=.*[a-z]).{6,}$"
        check_pwd = re.match(pattern_pwd,self.password)     #match & findall works the same

        if not len(self.name):
            self.errors.append("name field is empty")
        if not len(self.username):
            self.errors.append("username field is empty")
        if not len(self.email):
            self.errors.append("email field is empty")
        if not len(self.password):
            self.errors.append("password field is empty")
        if not check_pwd:
            self.errors.append("password does not meet minimum requirement")
        else:
            self.password = generate_password_hash(self.password)