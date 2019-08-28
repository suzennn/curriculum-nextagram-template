from app import app
from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from models import *
from werkzeug.security import check_password_hash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

login_manager = LoginManager()
login_manager.init_app(app)

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

@users_blueprint.route('/login')
def login():
    return render_template('users/login.html')

@users_blueprint.route('/login', methods=["POST"])
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
            return render_template("users/login.html")
    except:
        flash("user does not exist","error")
        return render_template("users/login.html")

@users_blueprint.route('/logout')
@login_required
def logout():
    flash("Logout successful! See you next time~","success")
    logout_user()
    return redirect("/")

@users_blueprint.route('/<user_id>')
@login_required
def profile(user_id):
    return render_template("users/profile.html")

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"

@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    check_user = user.User.get_by_id(id)
    return render_template('users/settings.html')

@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    check_user = user.User.get_by_id(id)
    if check_user.name == request.form["name_edit"] and check_user.username == request.form["username_edit"] and check_user.bio == request.form["bio_edit"] and check_user.email == request.form["email_edit"]:
        flash("nothing has been changed","error")
        return redirect(f"/users/{id}/edit")
    else:
        if check_user.name != request.form["name_edit"]:
            check_user.name = request.form["name_edit"]
        if check_user.username != request.form["username_edit"]:
            check_user.username = request.form["username_edit"]
        if check_user.bio != request.form["bio_edit"]:
            check_user.bio = request.form["bio_edit"]
        if check_user.email != request.form["email_edit"]:
            check_user.email = request.form["email_edit"]
    
    try:
        if check_user.save():
            flash("profile has been successfully updated", "success")
            return redirect(url_for("users.profile",user_id=check_user.id))
    except:
        flash('<br>'.join(check_user.errors),'error')
        return render_template("users/settings.html",errors=check_user.errors)


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Please login to proceed","error")
    return render_template('users/login.html')


