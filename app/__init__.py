from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth
from config import basedir, GOOGLE
from .src.session import *
import logging

app = Flask(__name__)
app.config.from_object('config')
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
app.session_interface=RedisSessionInterface()
db = SQLAlchemy(app)
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=GOOGLE['id'],
    consumer_secret=GOOGLE['secret'],
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# facebook = oauth.remote_app(
#     'facebook',
#     consumer_key=app.config.get(FACEBOOK_APP_ID),
#     consumer_secret=app.config.get(FACEBOOK_APP_SECRET),
#     request_token_params={'scope': 'email'},
#     base_url='https://graph.facebook.com',
#     request_token_url=None,
#     access_token_url='/oauth/access_token',
#     access_token_method='GET',
#     authorize_url='https://www.facebook.com/dialog/oauth'
# )

# PROVIDERS = { 'google': google, 'fb': facebook }

from app import views, models

db.create_all()
db.session.commit()

from .views.load import load
from .views.movement import movement
from .views.cubes import disease
from .views.stations import stations
from .views.undo import undo
from .views.cures import cures
from .views.cards import cards
from .views.events import events
from .views.phase import phase
from .views.login import login

app.register_blueprint(load)
app.register_blueprint(movement)
app.register_blueprint(disease)
app.register_blueprint(stations)
app.register_blueprint(undo)
app.register_blueprint(cures)
app.register_blueprint(cards)
app.register_blueprint(events)
app.register_blueprint(phase)
app.register_blueprint(login)
