from app import app
from ..src.game import Game
from ..src.constants import *
from flask import render_template, flash, redirect, url_for, request, jsonify, \
                    session, Blueprint, g
import json
import random
import pickle
from copy import copy
import sys

movement = Blueprint('movement', __name__)

@movement.route('/_move', methods=["GET", "POST"])
def set_move():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]
    selected = game.players[game.active]
    board = game.board
    origin = player.get_position()
    new_pos = request.args.get('id', 0, type=int)
    is_airlift = request.args.get('airlift', 0, type=int)
    index = (request.args.get('index', 0, type=int) + game.active) % game.num_players
    trashing = request.args.get('trashing', 0, type=int)
    owner = game.players[(game.active + index) % game.num_players ]
    discard = ""
    cures = copy(game.cures)
    move = ""

    selectable = []

    # neighbors = game.board.get_neighbors(origin)
    new_neighbors = game.board.get_neighbors(new_pos)
    can_charter = selected.can_charter(player.hand, board)
    can_fly_direct = selected.can_fly_direct(player.hand, board)
    prev_avail, dispatch, origin, player_id = game.set_available(0)

    if is_airlift == 1:
        discard=AIRLIFT
        action = game.play_airlift(index, new_pos)
    elif new_pos in player.can_drive(board):
        action = game.move(new_pos, index, '', 'drive')
    elif new_pos in dispatch:
        action = game.move(new_pos, index, '', 'dispatch')
    elif new_pos in player.can_shuttle(game.research_stations):
        action = game.move(new_pos, index, '', 'shuttle')
    elif player.get_role() == OE and new_pos in player.can_station_fly(game.research_stations, board):
        for card in player.hand:
            if card in range(NUM_CITIES):
                selectable.append( str(card) )
        if len(selectable) == 1:
            action = game.move(new_pos, index, selectable[0], 'station-fly')
    elif new_pos in can_fly_direct and new_pos not in can_charter:
        discard = str(new_pos)
        action = game.move(new_pos, index, discard, 'fly')
    elif new_pos in can_charter and new_pos not in can_fly_direct:
        discard = origin
        action = game.move(new_pos, index, discard, 'charter')
    elif new_pos in can_charter and new_pos in can_fly_direct:
        selectable.append( str(new_pos) )
        selectable.append( str(origin) )
    else:
        action = game.move(new_pos, index, '', 'shuttle')

    if len(selectable) > 1:
        session['actions'] = actions
        session['game'] = pickle.dumps(game)
        return jsonify(selectable=selectable)
    else:
        if game.phase < DRAW:
            if trashing == 0:
                actions.append(action)
            else:
                actions[-1]['trash'] = action

        available, new_dispatch, origin, player_id = game.set_available(0)
        can_take, can_give, team_hands = game.set_share()

        cubes_left = copy(game.cubes_left)
        can_build = player.can_build(new_pos, game.research_stations)
        can_cure = player.can_cure(game.research_stations)
        for i in range(len(game.board.neighbors)):
            if i in game.board.neighbors[i]:
                print(action['act'], i, game.board.neighbors[i])
        session['actions'] = actions
        session['game'] = pickle.dumps(game)
        return jsonify( available=available,
                        player_id=player_id,
                        mover_id=action['mover'],
                        move=action['act'],
                        origin=action['origin'],
                        player_pos=player.get_position(),
                        discard=discard,
                        cures=cures,
                        cubes_left=cubes_left,
                        can_build=can_build,
                        hand=copy(player.hand),
                        team_hands=team_hands,
                        can_cure=can_cure,
                        can_take=can_take,
                        can_give=can_give,
                        num_cards=len(owner.hand),
                        phase=game.phase )

@movement.route('/_select_card_for_move')
def select_move_card():
    game = pickle.loads(session['game'])
    actions = session['actions']
    board = game.board
    player = game.players[game.active]
    discard = request.args.get('card', 0, type=int)
    origin = player.get_position()
    new_pos = request.args.get('city_id', 0, type=int)

    cubes_left = copy(game.cubes_left)
    cures = copy(game.cures)
    action = 0

    if discard == origin:
        action = game.move(new_pos, game.active, discard, 'charter')
    elif discard == new_pos:
        action = game.move(new_pos, game.active, discard, 'fly')
    elif player.get_role() == OE:
        action = game.move(new_pos, game.active, discard, 'station-fly')
    actions.append(action)

    can_build = player.can_build(new_pos, game.research_stations)
    can_cure = player.can_cure(game.research_stations)
    available, new_dispatch, origin, player_id = game.set_available(0)
    can_take, can_give, team_hands = game.set_share()

    for i in range(len(game.board.neighbors)):
        if i in game.board.neighbors[i]:
            print(method['act'], i, game.board.neighbors[i])
    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( available=available,
                    player_id=player_id,
                    player_pos=player.get_position(),
                    mover_id=action['mover'],
                    move=action['act'],
                    origin=action['origin'],
                    cures=cures,
                    cubes_left=cubes_left,
                    can_build=can_build,
                    can_cure=can_cure,
                    hand=player.hand,
                    team_hands=team_hands,
                    can_take=can_take,
                    can_give=can_give,
                    num_cards=len(player.hand),
                    phase=game.phase )


@movement.route('/_select_player')
def select_player():
    game = pickle.loads(session['game'])
    index = (request.args.get('index', 0, type=int) + game.active) % game.num_players
    is_airlift = request.args.get('airlift', 0, type=int)
    player = game.players[game.active]
    selected = game.select_player(index)
    position = selected.get_position()
    if is_airlift == 1:
        available = []
        for city in range(NUM_CITIES):
            if city != position:
                available.append(str(city))
    else:
        available, dispatch, origin, player_id = game.set_available(is_airlift)
    can_build = player.can_build(player.get_position(), game.research_stations)
    can_cure = player.can_cure(game.research_stations)
    session['game'] = pickle.dumps(game)
    return jsonify( available=available,
                    role=selected.get_id(),
                    position=position,
                    can_build=can_build,
                    can_cure=can_cure,
                    phase=game.phase )
