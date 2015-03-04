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
    board = game.board
    available = []
    pieces = []
    roles = []
    positions = []
    for city in player.can_move(game.research_stations, board):
        available.append(str(city))
    team = game.players[game.active:] + game.players[:game.active]
    for x in team:
        pieces.append(ROLES[x.get_role()]['piece_img'])
        roles.append(x.get_id())
        positions.append(str(x.get_position()))
    session['game'] = pickle.dumps(game)
    return jsonify( available=available, pieces=pieces, roles=roles, positions=positions )

@app.route('/_move', methods=["GET", "POST"])
def set_move():
    game = pickle.loads(session['game'])
    player = game.players[game.active]
    board = game.board
    origin = player.get_position()
    new_pos = request.args.get('id', 0, type=int)
    discard = ""
    player_id = player.get_id()
    available = []
    move = ""

    selectable = []

    # neighbors = game.board.get_neighbors(origin)
    new_neighbors = game.board.get_neighbors(new_pos)
    can_charter = player.can_charter(game.research_stations, board)
    can_fly_direct = player.can_fly_direct(board)

    if new_pos in player.can_drive(board):
        player.move(new_pos, board, game.cures, game.cubes, game.quarantined)
        move = "drive"
    elif new_pos in player.can_shuttle(game.research_stations):
        player.move(new_pos, board, game.cures, game.cubes, game.quarantined)
        move = "shuttle"
    elif new_pos in can_fly_direct and new_pos not in can_charter:
        player.discard(new_pos)
        player.move(new_pos, board, game.cures, game.cubes, game.quarantined)
        move = "fly"
        discard = str(new_pos)
    elif new_pos in can_charter and new_pos not in can_fly_direct and player.get_role() != OE:
        player.discard(origin)
        discard = origin
        player.move(new_pos, board, game.cures, game.cubes, game.quarantined)
        move = "charter"
    elif new_pos in can_charter and player.get_role() == OE:
        if player.get_position() in game.research_stations:
            for card in player.hand:
                if card in range(NUM_CITIES):
                    selectable.append( str(card) )
            if len(selectable) == 1:
                player.discard( int(selectable[0]) )
                discard = selectable[0]
                player.move(new_pos, board, game.cures, game.cubes, game.quarantined)
                move = "charter"
        else:
            player.discard(origin)
            player.move(new_pos, board, game.cures, game.cubes, game.quarantined)
            move = "charter"
            discard = str(origin)
    elif new_pos in can_charter and new_pos in can_fly_direct:
        selectable.append( str(new_pos) )
        selectable.append( str(origin) )

    if len(selectable) > 1:
        session['game'] = pickle.dumps(game)
        return jsonify(selectable=selectable)
    else:
        for city in player.can_move(game.research_stations, board):
            available.append(str(city))
        session['game'] = pickle.dumps(game)
        return jsonify( available=available,
                        player_id=player_id,
                        move=move,
                        discard=discard )

@app.route('/_select_card_for_move')
def select_move_card():
    game = pickle.loads(session['game'])
    board = game.board
    player = game.players[game.active]
    card = request.args.get('card', 0, type=int)
    new_pos = request.args.get('city_id', 0, type=int)

    available = []
    player_id = player.get_id()

    player.discard(card)
    player.move(new_pos, board, game.cures, game.cubes, game.quarantined)
    for city in player.can_move(game.research_stations, board):
        available.append(str(city))
    session['game'] = pickle.dumps(game)
    return jsonify( available=available,
                    player_id=player_id )

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
                            cities = CITIES,
                            colors = COLOR_STRINGS)
