from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from .views.load import load
from .views.movement import movement
from .views.cubes import disease
from .views.stations import stations
from .views.undo import undo

app.register_blueprint(load)
app.register_blueprint(movement)
app.register_blueprint(disease)
app.register_blueprint(stations)
app.register_blueprint(undo)
