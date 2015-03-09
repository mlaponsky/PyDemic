from app import app
from ..src.game import Game
from ..src.constants import *
from flask import render_template, flash, redirect, url_for, request, jsonify, \
                    session, Blueprint
import json
import random
import pickle
from copy import copy
import sys

undo = Blueprint('undo', __name__)

@undo.route('/_undo')
def undo_action():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]
    action = actions.pop(-1)
    data = action['data']

    if action['act'] == "drive" or action['act'] == "shuttle":
        undo_move(data, player, game)
    elif action['act'] == "charter" or action['act'] == "fly":
        undo_move(data, player, game)
        undo_discard(data, player, game)
    elif action['act'] == "build":
        undo_station(data, player, game)
    elif action['act'] == "treat":
        undo_treatment(data, game)

    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify(result=action)

def undo_move(data, player, game):
    if player.get_id() == 'dispatcher':
        for p in game.players:
            if p.get_id() == data['role']:
                p.position = data['origin']
    else:
        player.position = data['origin']
    for color in COLORS:
        number = data['cubes'][color]
        if number != game.cubes[data['destination']][color]:
            game.cubes[data['destination']][color] = number
            game.cubes_left[color] += number
    game.board.rows[data['destination']] = data['rows']

def undo_discard(data, player, game):
    game.player_cards.remove_from_discard(int(data['discard']))
    player.add_card(int(data['discard']))

def undo_station(data, player, game):
    game.research_stations.remove(int(data['position']))
    if data['discard'] != 'none':
        game.player_cards.remove_from_discard(int(data['position']))
        player.add_card(int(data['position']))

def undo_treatment(data, game):
    game.cubes_left[int(data['color'])] -= data['removed']
    game.cubes[int(data['city'])][int(data['color'])] = data['num_cubes']
    game.board.rows[int(data['city'])] = data['rows']
