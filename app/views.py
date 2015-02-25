from app import app
from .src.game import Game
from .src.constants import *
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    game = None
    if game == None:
        game = Game([CP, OE, QS], 5)
    active = game.set_order()
    active_player = game.players[active]
    team = game.players[active+1:] + game.players[:active]
    return render_template("index.html",
                            title = 'GAME',
                            active_player = active_player,
                            team = team,
                            cards = CARDS,
                            colors = COLOR_STRINGS)
