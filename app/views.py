from app import app
from .src.game import Game
from .src.constants import *
from flask import render_template, jsonify
import json

game = Game([CP, OE, QS], 5)

@app.route('/_load')
def set_cities():
    player = game.players[game.active]
    data = []
    neighbors = game.board.get_neighbors(player.get_position())
    for city in player.can_move(player, game.research_stations, neighbors):
        data.append(str(city))
    return json.dumps(data)

@app.route('/')
@app.route('/index')
def index():
    active = game.active
    active_player = game.players[active]
    team = game.players[active+1:] + game.players[:active]
    data = []
    neighbors = game.board.get_neighbors(active_player.get_position())
    for city in active_player.can_move(active_player, game.research_stations, neighbors):
        data.append(str(city))

    return render_template("index.html",
                            title = 'GAME',
                            game = game,
                            active_player = active_player,
                            team = team,
                            cards = CARDS,
                            colors = COLOR_STRINGS,
                            data = data)
