from app import app
from ..src.game import Game
from ..src.constants import *
from flask import render_template, flash, redirect, url_for, request, jsonify, \
                    session, Blueprint
import json
import random
import pickle
from copy import copy

movement = Blueprint('movement', __name__)

@movement.route('/_load')
def set_cities():
    game = pickle.loads(session['game'])
    player = game.players[game.active]
    board = game.board
    available = []
    pieces = []
    roles = []
    positions = []
    research_stations = copy(game.research_stations)
    for city in player.can_move(game.research_stations, board):
        available.append(str(city))
    team = game.players[game.active:] + game.players[:game.active]
    for x in team:
        pieces.append(ROLES[x.get_role()]['piece_img'])
        roles.append(x.get_id())
        positions.append(str(x.get_position()))
    cubes = {}
    rows = {}
    for city in range(NUM_CITIES):
        if not all(v==0 for v in game.cubes[city]):
            cubes[city] = game.cubes[city]
            rows[city] = board.get_all_rows(city)
    session['game'] = pickle.dumps(game)
    return jsonify( available=available,
                    pieces=pieces,
                    roles=roles,
                    positions=positions,
                    cubes=cubes,
                    cube_rows=rows,
                    colors=COLOR_IMG,
                    rs=research_stations )

@movement.route('/_move', methods=["GET", "POST"])
def set_move():
    game = pickle.loads(session['game'])
    player = game.players[game.active]
    board = game.board
    origin = player.get_position()
    new_pos = request.args.get('id', 0, type=int)
    discard = ""
    player_id = player.get_id()
    available = []
    cures = copy(game.cures)
    move = ""

    selectable = []

    # neighbors = game.board.get_neighbors(origin)
    new_neighbors = game.board.get_neighbors(new_pos)
    can_charter = player.can_charter(game.research_stations, board)
    can_fly_direct = player.can_fly_direct(board)

    if new_pos in player.can_drive(board):
        player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
        move = "drive"
    elif new_pos in player.can_shuttle(game.research_stations):
        player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
        move = "shuttle"
    elif new_pos in can_fly_direct and new_pos not in can_charter:
        player.discard(new_pos)
        player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
        move = "fly"
        discard = str(new_pos)
    elif new_pos in can_charter and new_pos not in can_fly_direct and player.get_role() != OE:
        player.discard(origin)
        discard = origin
        player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
        move = "charter"
    elif new_pos in can_charter and player.get_role() == OE:
        if player.get_position() in game.research_stations:
            for card in player.hand:
                if card in range(NUM_CITIES):
                    selectable.append( str(card) )
            if len(selectable) == 1:
                player.discard( int(selectable[0]) )
                discard = selectable[0]
                player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
                move = "charter"
        else:
            player.discard(origin)
            player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
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
        if player.get_role() == MEDIC:
            cubes_left = copy(game.cubes_left)
            session['game'] = pickle.dumps(game)
            return jsonify( available=available,
                            player_id=player_id,
                            move=move,
                            discard=discard,
                            cures=cures,
                            cubes_left=cubes_left )
        else:
            session['game'] = pickle.dumps(game)
            return jsonify( available=available,
                            player_id=player_id,
                            move=move,
                            discard=discard )

@movement.route('/_select_card_for_move')
def select_move_card():
    game = pickle.loads(session['game'])
    board = game.board
    player = game.players[game.active]
    card = request.args.get('card', 0, type=int)
    new_pos = request.args.get('city_id', 0, type=int)

    available = []
    player_id = player.get_id()
    cubes_left = copy(game.cubes_left)
    cures = copy(game.cures)

    player.discard(card)
    player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
    for city in player.can_move(game.research_stations, board):
        available.append(str(city))
    if player.get_role() == MEDIC:
        session['game'] = pickle.dumps(game)
        return jsonify( available=available,
                        player_id=player_id,
                        cures=cures,
                        cubes_left=cubes_left )
    else:
        session['game'] = pickle.dumps(game)
        return jsonify( available=available,
                        player_id=player_id )
