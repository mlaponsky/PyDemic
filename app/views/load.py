from app import app
from ..src.game import Game
from ..src.constants import *
from flask import render_template, flash, redirect, url_for, request, jsonify, \
                    session, Blueprint
import json
from ..forms import SetupForm
import random
import pickle

load = Blueprint('load', __name__)

@load.route('/', methods=['GET','POST'])
@load.route('/setup', methods=['GET','POST'])
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

@load.route('/index')
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
                            cities = CITIES,
                            colors = COLOR_STRINGS)
