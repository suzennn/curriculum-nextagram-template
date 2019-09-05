from app import app
from flask import Blueprint, render_template, request, redirect, flash, session, url_for, abort, jsonify
from models import *
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from helpers.upload import s3, upload as imgupload

followers_blueprint = Blueprint('followers',
                            __name__,
                            template_folder='templates')

@followers_blueprint.route('/follow/<user_id>',methods=['get'])
@login_required
def follow_user(user_id):
    follow_user = user.User.get_by_id(user_id)
    if (follow_user.privacy_status ==  "private"):
        follow = follows.Follow(user_id=user_id, follower_id=current_user.id, status=0)
        follow.save()
        response = {
            "status": "success",
            "new_follower_count": follow_user.followers.where(follows.Follow.status==1).count()
        }
        return jsonify(response)
    else:
        follow = follows.Follow(user_id=user_id, follower_id=current_user.id, status=1)
        if follow.save():
            response = {
                "status": "success",
                "new_follower_count": follow_user.followers.where(follows.Follow.status==1).count()
            }
            flash(f"You are now following {follow_user.username}","success")
            return jsonify(response)
        else:
            flash("Sorry, something went wrong. Please try again later!","error")
            return redirect(url_for('sessions.profile',user_id=follow_user.id))

@followers_blueprint.route('/unfollow/<user_id>',methods=['get'])
@login_required
def unfollow_user(user_id):
    check_user = user.User.get_by_id(int(user_id))
    unfollow_user = follows.Follow.get(follows.Follow.user_id == int(user_id), follows.Follow.follower_id == current_user.id)
    try:
        unfollow_user.delete_instance()
        response = {
            "status": "success",
            "new_follower_count": check_user.followers.count()
        }
        flash(f"You have unfollowed {check_user.username}","success")
        return jsonify(response)
    except:
        flash("Sorry, something went wrong. Please try again later!","error")
        return redirect(url_for('sessions.profile',user_id=check_user.id))

@followers_blueprint.route('/accept-request/<follower_id>',methods=['get'])
@login_required
def accept_request(follower_id):
    update_follow = follows.Follow.update(status=1).where(follows.Follow.follower_id == follower_id, follows.Follow.user_id == current_user.id)
    try:
        update_follow.execute()
        response = {
            "status": "success",
            "new_follower_count": check_user.followers.count()
        }
        return jsonify(response)
    except:
        return redirect('/')

@followers_blueprint.route('/reject-request/<follower_id>',methods=['get'])
@login_required
def reject_request(follower_id):
    update_follow = follows.Follow.update(status=2).where(follows.Follow.follower_id == follower_id, follows.Follow.user_id == current_user.id)
    try:
        update_follow.execute()
        response = {
            "status": "success",
            "new_follower_count": check_user.followers.count()
        }
        return jsonify(response)
    except:
        return redirect('/')