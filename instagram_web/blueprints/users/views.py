from flask import Blueprint, render_template, request, redirect, flash, session
from models import *
from werkzeug.security import check_password_hash

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


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
def login_user():
    try:
        user.User.get(user.User.username == request.form['userlogin'])
        user_check = user.User.get(user.User.username == request.form['userlogin'])
        pwd_check = request.form['pwdlogin']
        result = check_password_hash(user_check.password,pwd_check)
        if result:
            session["logged_in"] = True
            session["user_id"] = user_check.id
            flash("Login successful! Welcome back~","success")
            return redirect("/")
        else:
            flash("password is incorrect. please try again","error")
            return render_template("users/login.html")
    except:
        flash("user does not exist","error")
        return render_template("users/login.html")

@users_blueprint.route('/logout')
def logout():
    session["logged_in"] = False
    flash("Logout successful! See you next time~","success")
    return redirect("/")

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass


