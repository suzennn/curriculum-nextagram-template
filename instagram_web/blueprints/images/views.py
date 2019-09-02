from app import app
from flask import Blueprint, render_template, request, redirect, flash, session, url_for, abort
from models import *
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from helpers.upload import s3, upload as imgupload

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def login_check(user_id):
    return user.User.get_by_id(int(user_id))

@images_blueprint.route('/upload/<user_id>')
@login_required
def upload_form(user_id):
    return render_template('images/uploadimg.html')

@images_blueprint.route('/upload/<user_id>',methods=['POST'])
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
        return render_template('images/uploadimg.html')

@images_blueprint.route('/upload-image/<user_id>')
@login_required
def upload_img_form(user_id):
    return render_template('images/uploadimages.html')

@images_blueprint.route('/upload-image/<user_id>',methods=['POST'])
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
        return render_template('images/uploadimages.html')

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Please login to proceed","error")
    return redirect(url_for('sessions.login'))