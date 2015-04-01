from app import app
from ..src.game import Game
from ..src.constants import *
from flask import render_template, flash, redirect, url_for, request, jsonify, \
                    session, Blueprint
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
    prev_avail, dispatch, origin, player_id = game.set_available(player)

    if position != -1:
        discard = GG
        action = { 'act': "gg", 'data': { 'origin': str(position),
                                          'discard': str(GG),
                                          'removed': str(to_remove),
                                          'card_data': CARDS[discard],
                                          'available': prev_avail } }
    else:
        discard = player.get_position() if player.get_role() != OE else -1
        position = player.get_position()
        action = { 'act': "build", 'data': { 'origin': str(player.get_position()),
                                             'discard': str(discard),
                                             'removed': str(to_remove),
                                             'card_data': CARDS[discard],
                                             'available': prev_avail } }
    actions.append(action)

    game.research_stations.remove(to_remove)
    player.build_station(position, discard, game.research_stations, game.player_cards)

    available, new_dispatch, origin, player_id = game.set_available(player)

    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( position=player.get_position(),
                    station=position,
                    discard=discard,
                    available=available )

@stations.route('/_build_station')
def build_station():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]
    num_stations = len(game.research_stations)
    prev_avail, dispatch, origin, player_id = game.set_available(player)

    position = request.args.get('position', -1, type=int)
    if position != -1:
        discard = GG
    else:
        position = player.get_position()
        discard = player.get_position() if player.get_role() != OE else -1

    if num_stations < MAX_STATIONS:
        action = { 'act': "build" if position == -1 else 'gg',
                   'data': { 'origin': str(position),
                             'discard': str(discard),
                             'removed': 'none',
                             'card_data': CARDS[discard],
                             'available': prev_avail }}
        actions.append(action)
        player.build_station(position, discard, game.research_stations, game.player_cards)

    available, new_dispatch, origin, player_id = game.set_available(player)
    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( position=player.get_position(),
                    station=position,
                    num_stations=num_stations,
                    discard=discard,
                    available=available )

@stations.route('/_escape_gg')
def escape_gg():
    game = pickle.loads(session['game'])
    return jsonify( position=game.players[game.active].get_position() )
