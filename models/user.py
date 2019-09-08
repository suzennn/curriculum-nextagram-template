from models.base_model import BaseModel
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property
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

    @hybrid_property
    def following_images(self):
        from models.images import Image
        from models.follows import Follow
        return (i for i in (Image.select().join(User,on=(Image.user_id == User.id)).join(Follow, on=(Image.user_id == Follow.user_id)).where(Follow.follower_id == self.id, Follow.status == 1).order_by(Image.created_at.desc()))) 
    
    @hybrid_property
    def pending_requests(self):
        from models.follows import Follow
        return (u for u in (Follow.select().join(User, on=(User.id == Follow.user_id)).where(Follow.user_id == self.id, Follow.status == 0))) 
    
    @hybrid_property
    def user_following(self):
        from models.follows import Follow
        return (u for u in (User.select().join(Follow, on=(User.id == Follow.user_id)).where(Follow.follower_id == self.id, Follow.status == 1))) 
    
    @hybrid_property
    def user_followers(self):
        from models.follows import Follow
        return (u for u in (User.select().join(Follow, on=(User.id == Follow.follower_id)).where(Follow.user_id == self.id, Follow.status == 1))) 

    # @hybrid_property
    # def user_suggestions(self):
    #     from models.follows import Follow
    #     return (s for s in (User.select().join(Follow, on=(User.id == Follow.user_id)).where(Follow.follower_id == self.id, User.id.not_in(Follow.select(Follow.user_id)))))