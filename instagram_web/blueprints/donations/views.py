import os
import braintree
from app import app
from flask import Blueprint, render_template, request, redirect, flash, session, url_for, abort
from models import *
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from helpers.donate import TRANSACTION_SUCCESS_STATUSES, generate_client_token, transact, find_transaction
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def login_check(user_id):
    return user.User.get_by_id(int(user_id))
    
@donations_blueprint.route('/donate-to/<image_id>')
@login_required
def new_checkout(image_id):
    client_token = generate_client_token()
    return render_template("donations/payment.html", client_token=client_token, image_id=image_id)

@donations_blueprint.route('/checkout/<transaction_id>', methods=['GET'])
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

    return render_template('donations/show.html', transaction=transaction, result=result)

@donations_blueprint.route('/checkout/<image_id>', methods=['POST'])
@login_required
def create_checkout(image_id):
    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options':{
            "submit_for_settlement": True
        }
    })
    transaction = find_transaction(transaction_id)
    check_user =  user.User.get(user.User.id == current_user.id)
    check_image = images.Image.get(images.Image.id == image_id)
    message = Mail(
        from_email='communities@nextagram.com',
        to_emails= check_user.email,
        subject='Thank you for your kind contribution!',
        html_content=render_template('donations/email.html',transaction=transaction,check_image=check_image))

    if result.is_success: 
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        flash("Transaction successful! Thanks so much :)","success")
        transact_user = transactions.Transaction(trans=result.transaction.id, user_id=check_user.id, image_id=image_id, amount=request.form['amount'])
        if transact_user.save():
            return redirect(url_for('donations.show_checkout',transaction_id=result.transaction.id))
        else:
            flash("Something went wrong! :( Please try again","error")
            return redirect(url_for('donations.new_checkout',image_id=image_id))
    else:
        flash("Something went wrong! :( Please try again","error")
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message),'error')
        return redirect(url_for('donations.new_checkout',image_id=image_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Please login to proceed","error")
    return render_template('sessions/login.html')