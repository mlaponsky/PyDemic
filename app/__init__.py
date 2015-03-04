from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from .views.load import load
from .views.movement import movement

app.register_blueprint(load)
app.register_blueprint(movement)
