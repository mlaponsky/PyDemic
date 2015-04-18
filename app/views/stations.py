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
    to_remove = request.args.get('id', 0, type=int)
    position = request.args.get('position', -1, type=int)
    index = request.args.get('index', 0, type=int)
    trashing = request.args.get('trashing', 0, type=bool)
    owner = game.players[(game.active + index) % game.num_players]
    prev_avail, dispatch, origin, player_id = game.set_available(player)
    can_build = player.get_position() not in game.research_stations and (player.get_position() in player.hand or player.get_role == OE)
    if position != -1:
        discard = GG
        action = { 'act': "gg",
                    'origin': str(position),
                    'can_build': can_build,
                    'discard': str(GG),
                    'owner': owner.get_id(),
                    'removed': str(to_remove),
                    'card_data': CARDS[discard],
                    'available': prev_avail }
    else:
        discard = player.get_position() if player.get_role() != OE else -1
        position = player.get_position()
        action = { 'act': "build",
                    'origin': str(player.get_position()),
                    'can_build': can_build,
                    'discard': str(discard),
                    'owner': owner.get_id(),
                    'removed': str(to_remove),
                    'card_data': CARDS[discard],
                    'available': prev_avail }
    if trashing == 0:
        actions.append(action)
    else:
        actions[-1]['trash'] = action

    game.research_stations.remove(to_remove)
    owner.build_station(position, discard, game.research_stations, game.player_cards)

    available, new_dispatch, origin, player_id = game.set_available(player)

    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( position=player.get_position(),
                    station=position,
                    discard=discard,
                    can_build=can_build,
                    owner=owner.get_id(),
                    available=available )

@stations.route('/_build_station')
def build_station():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]
    num_stations = len(game.research_stations)
    prev_avail, dispatch, origin, player_id = game.set_available(player)

    can_build = player.get_position() not in game.research_stations and (player.get_position() in player.hand or player.get_role() == OE)
    position = request.args.get('position', -1, type=int)
    trashing = request.args.get('trashing', 0, type=int)
    if position != -1:
        discard = GG
    else:
        position = player.get_position()
        discard = player.get_position() if player.get_role() != OE else -1
    index = request.args.get('index', 0, type=int)
    owner = game.players[(game.active + index) % game.num_players]
    if num_stations < MAX_STATIONS:
        action = { 'act': "build" if position == -1 else 'gg',
                   'origin': str(position),
                   'can_build': can_build,
                    'discard': str(discard),
                    'removed': 'none',
                    'owner': owner.get_id(),
                    'card_data': CARDS[discard],
                    'available': prev_avail }
        if trashing == 0:
            actions.append(action)
        else:
            actions[-1]['trash'] = action
        owner.build_station(position, discard, game.research_stations, game.player_cards)
    available, new_dispatch, origin, player_id = game.set_available(player)
    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( position=player.get_position(),
                    station=position,
                    can_build=can_build,
                    num_stations=num_stations,
                    discard=discard,
                    available=available )

@stations.route('/_escape_gg')
def escape_gg():
    game = pickle.loads(session['game'])
    return jsonify( position=game.players[game.active].get_position() )
