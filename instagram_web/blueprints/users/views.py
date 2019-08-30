import braintree
from app import app
from flask import Blueprint, render_template, request, redirect, flash, session, url_for, abort
from models import *
from werkzeug.security import check_password_hash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from helpers.upload import s3, upload as imgupload
from helpers.donate import TRANSACTION_SUCCESS_STATUSES, generate_client_token, transact, find_transaction

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
    user_view = user.User.get_or_none(user.User.id == user_id)
    return render_template("users/profile.html", user_view = user_view)

@users_blueprint.route('/search', methods=["POST"])
def show():
    username = request.form["user_search"]
    user_view = user.User.get_or_none(user.User.username == username)
    if user_view:
        return redirect(url_for('users.profile',user_id=user_view.id))
    else:
        return abort(404)

# @users_blueprint.route('/', methods=["GET"])
# def index():
#     return "USERS"

@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    check_user = user.User.get_by_id(id)
    return render_template('users/settings.html')

@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    check_user = user.User.get_by_id(id)
    if check_user.id == current_user.id:
        if check_user.name == request.form["name_edit"] and check_user.username == request.form["username_edit"] and check_user.bio == request.form["bio_edit"] and check_user.email == request.form["email_edit"]:
            flash("nothing has been changed","error")
            return redirect(f"/users/{id}/edit")
        else:
            check_user.name = request.form["name_edit"]
            check_user.username = request.form["username_edit"]
            check_user.bio = request.form["bio_edit"]
            check_user.email = request.form["email_edit"]
            if check_user.save():
                flash("profile has been successfully updated", "success")
                return redirect(url_for("users.profile",user_id=check_user.id))
            else:
                flash('<br>'.join(check_user.errors),'error')
                return redirect(f"/users/{id}/edit")

@users_blueprint.route('/upload/<user_id>')
@login_required
def upload_form(user_id):
    return render_template('users/uploadimg.html')

@users_blueprint.route('/upload/<user_id>',methods=['POST'])
@login_required
def upload(user_id):
    try:
        imgupload("profile-pic")
        check_user = user.User.get_by_id(user_id)
        file = request.files.get('user_file').filename
        check_user.dp = file
        check_user.save()
        flash("profile picture successfully changed","success")
        return redirect(f'/users/{user_id}')
    except:
        flash("Something went wrong. Please try again!","error")
        return render_template('users/uploadimg.html')

@users_blueprint.route('/upload-image/<user_id>')
@login_required
def upload_img_form(user_id):
    return render_template('users/uploadimages.html')

@users_blueprint.route('/upload-image/<user_id>',methods=['POST'])
@login_required
def upload_img(user_id):
    try:
        imgupload("user-images")
        check_user = user.User.get(user.User.id == current_user.id)
        file = request.files.get('user_file').filename
        img = images.Image(path=file, user_id=check_user.id)
        img.save()
        flash("image successfully uploaded","success")
        return redirect(f'/users/{user_id}')
    except:
        flash("Something went wrong. Please try again!","error")
        return render_template('users/uploadimages.html')

@users_blueprint.route('/donate-to/<image_id>')
@login_required
def new_checkout(image_id):
    client_token = generate_client_token()
    return render_template("checkout/payment.html", client_token=client_token, image_id=image_id)

@users_blueprint.route('/checkout/<transaction_id>', methods=['GET'])
@login_required
def show_checkout(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Thank you for your generosity, you kind soul!',
            'icon': 'success',
            'message': 'Transaction has successfully gone through.'
        }
    else:
        result = {
            'header': 'Transaction Failed :(',
            'icon': 'fail',
            'message': 'Transaction has a status of ' + transaction.status + '.'
        }

    return render_template('checkout/show.html', transaction=transaction, result=result)

@users_blueprint.route('/checkout/<image_id>', methods=['POST'])
@login_required
def create_checkout(image_id):
    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options':{
            "submit_for_settlement": True
        }
    })
    check_user =  user.User.get(user.User.id == current_user.id)

    if result.is_success:
        flash("Transaction successful! Thanks so much :)","success")
        transact_user = transactions.Transaction(trans=result.transaction.id, user_id=check_user.id, image_id=image_id, amount=request.form['amount'])
        if transact_user.save():
            return redirect(url_for('users.show_checkout',transaction_id=result.transaction.id))
        else:
            flash("Something went wrong! :( Please try again","error")
            return redirect(url_for('users.new_checkout',image_id=image_id))
    else:
        flash("Something went wrong! :( Please try again","error")
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message),'error')
        return redirect(url_for('users.new_checkout',image_id=image_id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Please login to proceed","error")
    return render_template('users/login.html')


