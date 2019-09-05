from app import app, login_manager
from flask import Blueprint, render_template, request, redirect, flash, session, url_for, abort
from models import *
from werkzeug.security import check_password_hash
from flask_login import current_user, login_user, logout_user, login_required, UserMixin
from helpers.google_oauth import oauth

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@login_manager.user_loader
def login_check(user_id):
    return user.User.get_by_id(int(user_id))

@sessions_blueprint.route('/login')
def login():
    return render_template('sessions/login.html')

@sessions_blueprint.route('/login', methods=["POST"])
def login_user_check():
    try:
        user.User.get(user.User.username == request.form['userlogin'])
        user_check = user.User.get(user.User.username == request.form['userlogin'])
        pwd_check = request.form['pwdlogin']
        result = check_password_hash(user_check.password,pwd_check)
        if result:
            login_user(user_check)
            flash("Login successful! Welcome back~","success")
            return redirect("/")
        else:
            flash("password is incorrect. please try again","error")
            return render_template("sessions/login.html")
    except:
        flash("user does not exist","error")
        return render_template("sessions/login.html")

@sessions_blueprint.route('/logout')
@login_required
def logout():
    flash("Logout successful! See you next time~","success")
    logout_user()
    return redirect("/")

@sessions_blueprint.route('/<user_id>')
@login_required
def profile(user_id):
    user_view = user.User.get_or_none(user.User.id == user_id)
    check_following = follows.Follow.get_or_none(follows.Follow.user_id == user_view.id, follows.Follow.follower_id == current_user.id)
    return render_template("sessions/profile.html", user_view = user_view, check_following = check_following)

@sessions_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    check_user = user.User.get_by_id(id)
    return render_template('sessions/settings.html')

@sessions_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    check_user = user.User.get_by_id(id)
    if check_user.id == current_user.id:
        if check_user.name == request.form["name_edit"] and check_user.username == request.form["username_edit"] and check_user.bio == request.form["bio_edit"] and check_user.email == request.form["email_edit"] and check_user.privacy_status == request.form["privacy_setting"]:
            flash("nothing has been changed","error")
            return redirect(f"/users/{id}/edit")
        else:
            check_user.name = request.form["name_edit"]
            check_user.username = request.form["username_edit"]
            check_user.bio = request.form["bio_edit"]
            check_user.email = request.form["email_edit"]
            check_user.privacy_status = request.form["privacy_setting"]
            if check_user.save():
                flash("profile has been successfully updated", "success")
                return redirect(url_for("sessions.profile",user_id=check_user.id))
            else:
                flash('<br>'.join(check_user.errors),'error')
                return redirect(f"/users/{id}/edit")

@sessions_blueprint.route('/google_login/authorize', methods=['GET'])
def authorize():
    token = oauth.google.authorize_access_token()

    if token:
        email = oauth.google.get(
            'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
        check_user = user.User.get_or_none(user.User.email == email)
        if not check_user:
            flash('No user registered with this Google email!', 'error')
            return redirect(url_for('sessions.login'))
    login_user(check_user)
    flash("Login successful! Welcome back~","success")
    return redirect("/")

@sessions_blueprint.route('/google_login', methods=['GET'])
def google_login():
        redirect_uri = url_for('sessions.authorize', _external=True)
        return oauth.google.authorize_redirect(redirect_uri)

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Please login to proceed","error")
    return render_template('sessions/login.html')