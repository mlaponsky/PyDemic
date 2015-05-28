from app import app
from ..src.game import Game
from ..src.constants import *
from flask import render_template, flash, redirect, url_for, request, jsonify, \
                    session, Blueprint, g
import json
import random
import pickle
from copy import copy

stations = Blueprint('stations', __name__)

@stations.route('/_select_station')
def select_station():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]
    to_remove = request.args.get('id', -1, type=int)
    position = request.args.get('position', -1, type=int)
    index = (request.args.get('index', 0, type=int) + game.active) % game.num_players
    trashing = request.args.get('trashing', 0, type=int)
    is_gg = request.args.get('is_gg', 0, type=int)
    owner = game.players[(game.active+index) % game.num_players]

    if is_gg != 0:
        action = game.play_gg(position, index, to_remove)
    else:
        action = game.build(to_remove)

    if game.phase <= DRAW:
        if trashing == 0:
            actions.append(action)
        else:
            actions[-1]['trash'] = action
    available, new_dispatch, origin, player_id = game.set_available(player)
    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( position=player.get_position(),
                    station=position,
                    discard=action['cards'],
                    can_build=action['can_build'],
                    owner=action['owner'],
                    available=available,
                    num_cards=len(owner.hand),
                    phase=game.phase )

@stations.route('/_build_station')
def build_station():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]
    position = request.args.get('position', -1, type=int)
    trashing = request.args.get('trashing', 0, type=int)
    is_gg = request.args.get('is_gg', 0, type=int)
    index = (request.args.get('index', 0, type=int) + game.active) % game.num_players
    num_stations = len(game.research_stations)

    owner = game.players[index]
    if num_stations < MAX_STATIONS:
        if position != -1:
            action = game.play_gg(position, index, -1)
        else:
            position = player.get_position()
            action = game.build(-1)
        if game.phase <= DRAW:
            if trashing == 0:
                actions.append(action)
            else:
                actions[-1]['trash'] = action
        available, new_dispatch, origin, player_id = game.set_available(0)
        can_build = player.get_position() not in game.research_stations and (player.get_position()
                                                in player.hand or player.get_role() == OE)
        session['actions'] = actions
        session['game'] = pickle.dumps(game)
        return jsonify( position=player.get_position(),
                        station=position,
                        can_build=can_build,
                        num_stations=num_stations,
                        discard=action['cards'],
                        owner=action['owner'],
                        available=available,
                        num_cards=len(owner.hand),
                        phase=game.phase )
    else:
        position = position if position != -1 else player.get_position()
        available, new_dispatch, origin, player_id = game.set_available(0)
        session['actions'] = actions
        session['game'] = pickle.dumps(game)
        return jsonify( station=position,
                        available=available,
                        position=player.get_position() )

@stations.route('/_escape_gg')
def escape_gg():
    game = pickle.loads(session['game'])
    return jsonify( position=game.players[game.active].get_position() )
