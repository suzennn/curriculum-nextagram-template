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
    bio = pw.CharField(null=True)
    dp = pw.CharField(null=True)
    privacy_status = pw.CharField(null=True)

    def validate(self):
        pattern_pwd = "(?=.*[A-Z])(?=.*[!@#$&*\^%\*\.])(?=.*[0-9])(?=.*[a-z]).{6,}$"
        check_pwd = re.match(pattern_pwd,self.password)     #match & findall works the same
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

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
        if duplicate_username and not (duplicate_username.id == self.id):
            self.errors.append('Username already exists')
        if duplicate_email and not (duplicate_email.id == self.id):
            self.errors.append('Email is already in use')
        elif not self.id:
            self.password = generate_password_hash(self.password)