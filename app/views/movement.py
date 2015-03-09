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

@movement.route('/_move', methods=["GET", "POST"])
def set_move():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]
    board = game.board
    origin = player.get_position()
    new_pos = request.args.get('id', 0, type=int)
    discard = ""
    player_id = player.get_id()
    if player_id == 'dispatcher':
        player_id = player.selected.get_id()
    available = []
    cures = copy(game.cures)
    move = ""

    selectable = []

    # neighbors = game.board.get_neighbors(origin)
    new_neighbors = game.board.get_neighbors(new_pos)
    can_charter = player.can_charter(game.research_stations, board)
    can_fly_direct = player.can_fly_direct(board)

    prev_avail = []
    for city in player.can_move(game.research_stations, board):
        prev_avail.append(str(city))
    prev_build = player.can_build(origin, game.research_stations)
    prev_cure = player.can_cure(game.research_stations)
    orig_cubes = copy(game.cubes[new_pos])
    orig_rows = copy(board.rows[new_pos])

    if new_pos in player.can_drive(board):
        player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
        move="drive"
    elif new_pos in player.can_shuttle(game.research_stations):
        player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
        move = "shuttle"
    elif new_pos in can_fly_direct and new_pos not in can_charter:
        player.discard(new_pos, game.player_cards)
        player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
        discard = str(new_pos)
        move = "fly"
    elif new_pos in can_charter and new_pos not in can_fly_direct and player.get_role() != OE:
        player.discard(origin, game.player_cards)
        discard = origin
        player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
        move = "charter"
    elif new_pos in can_charter and player.get_role() == OE:
        if player.get_position() in game.research_stations:
            for card in player.hand:
                if card in range(NUM_CITIES):
                    selectable.append( str(card) )
            if len(selectable) == 1:
                player.discard( int(selectable[0]), game.player_cards )
                discard = selectable[0]
                player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
                move = "charter"
        else:
            player.discard(origin, game.player_cards)
            player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
            discard = str(origin)
            move = "charter"
    elif new_pos in can_charter and new_pos in can_fly_direct:
        selectable.append( str(new_pos) )
        selectable.append( str(origin) )

    if len(selectable) > 1:
        session['actions'] = actions
        session['game'] = pickle.dumps(game)
        return jsonify(selectable=selectable)
    else:
        action = { 'act': move, 'data': { 'role': player_id,
                                          'origin': origin,
                                          'destination': new_pos,
                                          'discard': discard,
                                          'available': prev_avail,
                                          'can_build': prev_build,
                                          'can_cure': prev_cure,
                                          'cubes': orig_cubes,
                                          'rows': orig_rows,
                                          'color_img': COLOR_IMG,
                                          'card': CARDS[int(discard)] if discard != '' else 'none' }}
        actions.append(action)
        for city in player.can_move(game.research_stations, board):
            available.append(str(city))
        if player.get_role() == MEDIC:
            cubes_left = copy(game.cubes_left)
            can_build = player.can_build(new_pos, game.research_stations)
            can_cure = player.can_cure(game.research_stations)

            session['actions'] = actions
            session['game'] = pickle.dumps(game)
            return jsonify( available=available,
                            player_id=player_id,
                            move=move,
                            discard=discard,
                            cures=cures,
                            cubes_left=cubes_left,
                            can_build=can_build,
                            can_cure=can_cure )
        else:
            can_build = player.can_build(new_pos, game.research_stations)
            can_cure = player.can_cure(game.research_stations)

            session['actions'] = actions
            session['game'] = pickle.dumps(game)
            return jsonify( available=available,
                            player_id=player_id,
                            move=move,
                            discard=discard,
                            can_build=can_build,
                            can_cure=can_cure )

@movement.route('/_select_card_for_move')
def select_move_card():
    game = pickle.loads(session['game'])
    actions = session['actions']
    board = game.board
    player = game.players[game.active]
    discard = request.args.get('card', 0, type=int)
    origin = player.get_position()
    new_pos = request.args.get('city_id', 0, type=int)

    available = []
    player_id = player.get_id()
    cubes_left = copy(game.cubes_left)
    cures = copy(game.cures)
    action = 0

    prev_avail = []
    for city in player.can_move(game.research_stations, board):
        prev_avail.append(str(city))
    prev_build = player.can_build(origin, game.research_stations)
    prev_cure = player.can_cure(game.research_stations)
    orig_cubes = game.cubes[new_pos]
    orig_rows = board.rows[new_pos]

    player.discard(discard, game.player_cards)
    if discard == origin:
        move = "charter"
    else:
        move = "fly"

    action = { 'act': move, 'data': { 'role': player_id,
                                      'origin': origin,
                                      'destination': new_pos,
                                      'discard': discard,
                                      'available': prev_avail,
                                      'can_build': prev_build,
                                      'can_cure': prev_cure,
                                      'cubes': orig_cubes,
                                      'rows': orig_rows,
                                      'color_img': COLOR_IMG,
                                      'card': CARDS[int(discard)] if discard != '' else     'none'
                                      }}
    actions.append(action)

    player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
    can_build = player.can_build(new_pos, game.research_stations)
    can_cure = player.can_cure(game.research_stations)
    for city in player.can_move(game.research_stations, board):
        available.append(str(city))
    if player.get_role() == MEDIC:
        session['actions'] = actions
        session['game'] = pickle.dumps(game)
        return jsonify( available=available,
                        player_id=player_id,
                        move=move,
                        cures=cures,
                        cubes_left=cubes_left,
                        can_build=can_build,
                        can_cure=can_cure )
    else:
        session['actions'] = actions
        session['game'] = pickle.dumps(game)
        return jsonify( available=available,
                        player_id=player_id,
                        can_build=can_build,
                        can_cure=can_cure )
