from flask import render_template, flash, redirect, session, url_for, request, g, Blueprint, jsonify
from app import app, db, google
from ..models import User, GameStore
from config import *

login = Blueprint('login', __name__)

# @login.route('/')
# def index():
#     if 'google_token' in session:
#         me = google.get('userinfo')
#         return jsonify(data=me.data)
#     return redirect(url_for('load.setup'))


@login.route('/login')
def login_user():
    return google.authorize(callback=url_for('login.authorized', _external=True))


@login.route('/logout')
def logout_user():
    session.pop('google_token', None)
    return redirect(url_for('load.setup'))


@login.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    data = google.get('userinfo').data
    if User.query.filter_by(email=data['email']).first() == None:
        user = User(nickname=data['name'], email=data['email'])
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('load.setup'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
