from app import app
from flask import Blueprint, render_template, request, redirect, flash, session, url_for, abort
from models import *
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from helpers.upload import s3, upload as imgupload

followers_blueprint = Blueprint('followers',
                            __name__,
                            template_folder='templates')

@followers_blueprint.route('/follow/<user_id>',methods=['POST'])
@login_required
def follow_user(user_id):
    follow_user = user.User.get_by_id(user_id)
    follow = follows.Follow(user_id=user_id, follower_id = current_user.id)
    if follow.save():
        flash(f"You are now following {follow_user.username}","success")
        return redirect(url_for('sessions.profile',user_id=follow_user.id))
    else:
        flash("Sorry, something went wrong. Please try again later!","error")
        return redirect(url_for('sessions.profile',user_id=follow_user.id))

@followers_blueprint.route('/unfollow/<user_id>',methods=['POST'])
@login_required
def unfollow_user(user_id):
    check_user = user.User.get_by_id(int(user_id))
    unfollow_user = follows.Follow.get(follows.Follow.user_id == int(user_id), follows.Follow.follower_id == current_user.id)
    try:
        unfollow_user.delete_instance()
        flash(f"You have unfollowed {check_user.username}","success")
        return redirect(url_for('sessions.profile',user_id=check_user.id))
    except:
        flash("Sorry, something went wrong. Please try again later!","error")
        return redirect(url_for('sessions.profile',user_id=check_user.id))