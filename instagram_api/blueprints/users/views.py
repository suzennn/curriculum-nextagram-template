from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models.user import *
from models.images import *
from models.follows import *
from models.transactions import *

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

# GET REQUESTS
@users_api_blueprint.route('/users', methods=['GET'])
def index():
    response = [
        {
            "id": user.id,
            "username": user.username,
            "profileImage": f"https://nextagram-qwerty-flask.s3.amazonaws.com/profile-pic/{user.dp}"
        }
        for user in user.User.select()
    ]
    return jsonify(response)

@users_api_blueprint.route('/users/<user_id>', methods=['GET'])
def search(user_id):
    user = User.get_by_id(user_id)
    response = {
        "id": user.id,
        "username": user.username,
        "profileImage": f"https://nextagram-qwerty-flask.s3.amazonaws.com/profile-pic/{user.dp}"
    }
    return jsonify(response)

@users_api_blueprint.route('/users/check_name', methods=['GET'])
def check_username():
    search = request.args.get("username")
    search_username = User.get_or_none(User.username == search)
    if search_username:
        response = {
            "exists": True,
            "valid": False
        }
    else:
        response = {
            "exists": False,
            "valid": True
        }
    return jsonify(response)

@users_api_blueprint.route('/users/me', methods=['GET'])
@login_required
def search_curr():
    response = {
        "id": current_user.id,
        "username": current_user.username,
        "profileImage": f"https://nextagram-qwerty-flask.s3.amazonaws.com/profile-pic/{current_user.dp}"
    }
    return jsonify(response)

@users_api_blueprint.route('/images', methods=['GET'])
def show():
    search_id = request.args.get("userId")
    response = [f"https://nextagram-qwerty-flask.s3.amazonaws.com/user-images/{image.path}" for image in Image.select().where(Image.user_id == search_id)]
    return jsonify(response)

@users_api_blueprint.route('/images/me', methods=['GET'])
def show_curr():
    response = [f"https://nextagram-qwerty-flask.s3.amazonaws.com/user-images/{image.path}" for image in Image.select().where(Image.user_id == current_user.id)]
    return jsonify(response)

#POST REQUESTS
@users_api_blueprint.route('/users', methods=['POST'])
def create():
    user = User(
        username=request.json.get('username'),
        email=request.json.get('email'),
        password=request.json.get('password')
    )

    if user.save():
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'jwt': access_token
        })
    else:
        return jsonify(user.errors), 400
