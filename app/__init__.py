from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
from .src.session import *

app = Flask(__name__)
app.config.from_object('config')
app.session_interface=RedisSessionInterface()
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, users

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
