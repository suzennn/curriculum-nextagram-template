import os
import config
from app import app
from flask import render_template, abort 
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.followers.views import followers_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from helpers.google_oauth import oauth
from flask_login import current_user
from models import *

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/users")
app.register_blueprint(images_blueprint, url_prefix="/users")
app.register_blueprint(donations_blueprint, url_prefix="/users")
app.register_blueprint(followers_blueprint, url_prefix="/users")

oauth.init_app(app)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def home():
    return render_template('home.html', follow=follows.Follow)
    # return abort(500)

@app.context_processor
def inject_users():
    return {"users": user.User}
