import os
import braintree
from app import app, login_manager
from flask import Blueprint, render_template, request, redirect, flash, session, url_for, abort
from models import *
from werkzeug.security import check_password_hash
from flask_login import current_user, login_user, logout_user, login_required, UserMixin
from helpers.upload import s3, upload as imgupload
from helpers.donate import TRANSACTION_SUCCESS_STATUSES, generate_client_token, transact, find_transaction
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

@login_manager.user_loader
def login_check(user_id):
    return user.User.get_by_id(int(user_id))

@users_blueprint.route('/new')
def new():
    return render_template('users/new.html')

@users_blueprint.route('/new', methods=['POST'])
def create():
    if request.form["password"] != request.form["confirmpwd"]:
        flash('passwords do not match','error')
        return render_template("users/new.html")
    else:
        new_user = user.User(name=request.form["name"],username=request.form["username"],email=request.form["email"],password=request.form["password"])
        if new_user.save():
            flash("Successfully saved!",'success')
            return redirect("/")
        else:
            flash('<br>'.join(new_user.errors),'error')
            return render_template("users/new.html",errors=new_user.errors)

@users_blueprint.route('/search', methods=["POST"])
def show():
    username = request.form["user_search"]
    user_view = user.User.get_or_none(user.User.username == username)
    if user_view:
        return redirect(url_for('sessions.profile',user_id=user_view.id))
    else:
        return abort(404)

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Please login to proceed","error")
    return render_template('sessions/login.html')