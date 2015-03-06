from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from .views.load import load
from .views.movement import movement
from .views.cubes import disease

app.register_blueprint(load)
app.register_blueprint(movement)
app.register_blueprint(disease)
