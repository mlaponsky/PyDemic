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
    player = game.players[game.active]
    position = player.get_position()
    to_remove = request.args.get('id', 0, type=int)
    discard = (player.get_role() != OE)
    available = []
    prev_avail = []

    for city in player.can_move(game.research_stations, game.board):
        prev_avail.append(str(city))
    action = { 'act': "build", 'data': { 'position': str(position),
                                        'discard': str(position) if discard else 'none',
                                        'card': CARDS[position],
                                        'available': prev_avail }}
    actions.append(action)

    game.research_stations.remove(to_remove)
    player.build_station(position, game.research_stations, game.player_cards)

    player.can_move(game.research_stations, game.board)
    for city in player.can_move(game.research_stations, game.board):
        available.append(str(city))

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
    available = []
    prev_avail = []

    for city in player.can_move(game.research_stations, game.board):
        prev_avail.append(str(city))
    action = { 'act': "build", 'data': { 'position': str(position),
                                        'discard': str(position) if discard else 'none',
                                        'card': CARDS[position],
                                        'available': prev_avail }}
    actions.append(action)

    if num_stations < MAX_STATIONS:
        player.build_station(position, game.research_stations, game.player_cards)

    for city in player.can_move(game.research_stations, game.board):
        available.append(str(city))

    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( position=position,
                    num_stations=num_stations,
                    discard=discard,
                    available=available )
