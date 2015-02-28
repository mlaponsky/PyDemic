from app import app
from .src.game import Game
from .src.constants import *
from flask import render_template, flash, redirect, url_for, request, jsonify, g, \
                    session
import json
from .forms import SetupForm
import random
import pickle

@app.route('/', methods=['GET','POST'])
@app.route('/setup', methods=['GET','POST'])
def setup():
    available_roles = [CP, DISPATCHER, MEDIC, OE, QS, RESEARCHER, SCIENTIST]
    form = SetupForm()
    if form.validate_on_submit():
        roles = [ form.char0.data, form.char1.data, form.char2.data, form.char3.data ]
        chosen = []
        for role in roles:
            if role == "random":
                a = random.choice(available_roles)
                available_roles.remove(a)
                chosen.append(a)
            elif role != 'none':
                available_roles.remove(role)
                chosen.append(role)
        if len(chosen) < 2:
            flash("You must select at least 2 players.")
            return render_template("setup.html",
                                    title="Pandemic Setup",
                                    form=form)
        game = Game(chosen, form.difficulty.data)
        session['game'] = pickle.dumps(game)
        return redirect(url_for('index'))
    return render_template("setup.html",
                            title="Pandemic Setup",
                            form=form)

@app.route('/_load')
def set_cities():
    game = pickle.loads(session['game'])
    player = game.players[game.active]
    data = []
    neighbors = game.board.get_neighbors(player.get_position())
    for city in player.can_move(player, game.research_stations, neighbors):
        data.append(str(city))
    session['game'] = pickle.dumps(game)
    return json.dumps(data)

@app.route('/index')
def index():
    game = pickle.loads(session['game'])
    active = game.active
    active_player = game.players[active]
    team = game.players[active+1:] + game.players[:active]
    session['game'] = pickle.dumps(game)
    return render_template("index.html",
                            title = 'GAME',
                            game = game,
                            active_player = active_player,
                            team = team,
                            cards = CARDS,
                            colors = COLOR_STRINGS)
