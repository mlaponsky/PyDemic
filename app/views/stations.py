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
    position = player.get_position()
    to_remove = request.args.get('id', 0, type=int)
    discard = (player.get_role() != OE)

    prev_avail, dispatch, origin, player_id = game.set_available(player)

    action = { 'act': "build", 'data': { 'origin': str(position),
                                        'removed': str(to_remove),
                                        'cards': str(position) if discard else 'none',
                                        'card_data': CARDS[position],
                                        'available': prev_avail }}
    actions.append(action)

    game.research_stations.remove(to_remove)
    player.build_station(position, game.research_stations, game.player_cards)

    available, new_dispatch, origin, player_id = game.set_available(player)

    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( position=position,
                    discard=discard,
                    available=available )

@stations.route('/_build_station')
def build_station():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]
    position = player.get_position()
    num_stations = len(game.research_stations)
    discard = (player.get_role() != OE)

    prev_avail, dispatch, origin, player_id = game.set_available(player)

    if num_stations < MAX_STATIONS:
        action = { 'act': "build", 'data': { 'origin': str(position),
                                            'removed': 'none',
                                            'cards': str(position) if discard else 'none',
                                            'card_data': CARDS[position],
                                            'available': prev_avail }}
        actions.append(action)
        player.build_station(position, game.research_stations, game.player_cards)

    available, new_dispatch, origin, player_id = game.set_available(player)

    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( position=position,
                    num_stations=num_stations,
                    discard=discard,
                    available=available )
