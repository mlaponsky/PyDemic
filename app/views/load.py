from app import app
from ..src.game import Game
from ..src.constants import *
from flask import render_template, flash, redirect, url_for, request, jsonify, \
                    session, Blueprint
import json
from ..forms import SetupForm
import random
import pickle
from copy import copy

load = Blueprint('load', __name__)

@load.route('/', methods=['GET','POST'])
@load.route('/index', methods=['GET', 'POST'])
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
        actions = []
        session.clear()
        session['game'] = pickle.dumps(game)
        session['actions'] = actions
        return redirect(url_for('load.start_game'))
    return render_template("setup.html",
                            title="Pandemic Setup",
                            form=form)

@load.route('/_load')
def set_game():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]
    board = game.board
    available = []
    pieces = []
    roles = []
    positions = []

    team = game.players[game.active:] + game.players[:game.active]
    if game.players[game.active].get_role() == DISPATCHER:
        game.players[game.active].select(game.players[game.active])
        for p in team:
            if p != game.players[game.active] and p.get_position() != game.players[game.active].get_position():
                available.append([].get_position())
    for p in team:
        pieces.append(ROLES[p.get_role()]['piece_img'])
        roles.append(p.get_id())
        positions.append(str(p.get_position()))

    can_take, can_give, team_hands = game.set_share()

    research_stations = copy(game.research_stations)
    can_build = player.can_build( player.get_position(), research_stations)
    can_cure = player.can_cure(research_stations)
    for city in player.can_move(game.research_stations, board):
        available.append(str(city))
    cubes = {}
    rows = {}
    cures = game.cures
    hand = player.hand

    for city in range(NUM_CITIES):
        if not all(v==0 for v in game.cubes[city]):
            cubes[city] = game.cubes[city]
            rows[city] = board.get_all_rows(city)

    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( available=available,
                    pieces=pieces,
                    roles=roles,
                    positions=positions,
                    cubes=cubes,
                    cube_rows=rows,
                    colors=COLOR_IMG,
                    cures=cures,
                    rs=research_stations,
                    can_build=can_build,
                    can_cure=can_cure,
                    role_img=ROLES[player.get_role()]['title_img'],
                    hand=hand,
                    team_hands=team_hands,
                    can_give=can_give,
                    can_take=can_take,
                    cards=CARDS,
                    actions=actions )

@load.route('/game')
def start_game():
    try:
        game = pickle.loads(session['game'])
    except:
        return redirect(url_for('setup'))
    active = game.active
    active_player = game.players[active]
    team = game.players[active:] + game.players[:active]

    session['game'] = pickle.dumps(game)
    return render_template("index.html",
                            title = 'GAME',
                            game = game,
                            active_player = active_player,
                            team = team,
                            cards = CARDS,
                            cities = CITIES,
                            colors = COLOR_STRINGS,
                            num_cities=NUM_CITIES )
