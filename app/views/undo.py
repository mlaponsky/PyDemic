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
    elif action['act'] == "cure":
        undo_cure(data, player, game)
    elif action['act'] == "take":
        undo_take(data, game)

    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify(result=action)

def undo_move(data, player, game):
    if player.get_id() == 'dispatcher':
        for p in game.players:
            if p.get_id() == data['id']:
                p.position = data['origin']
                game.quarantined = game.board.get_neighbors(p.get_position())
                game.quarantined.append(p.get_position())
    else:
        player.position = data['origin']
        game.quarantined = game.board.get_neighbors(player.get_position())
        game.quarantined.append(player.get_position())

    for color in COLORS:
        number = data['cubes'][color]
        if number != game.cubes[data['destination']][color]:
            game.cubes[data['destination']][color] = number
            game.cubes_left[color] += number
    game.board.rows[data['destination']] = data['rows']

def undo_discard(data, player, game):
    game.player_cards.remove_from_discard(int(data['cards']))
    player.add_card(int(data['cards']))

def undo_station(data, player, game):
    game.research_stations.remove(int(data['origin']))
    if data['removed'] != 'none':
        game.research_stations.append(int(data['removed']))
    if data['cards'] != 'none':
        game.player_cards.remove_from_discard(int(data['origin']))
        player.add_card(int(data['origin']))

def undo_treatment(data, game):
    game.cubes_left[int(data['color'])] -= data['removed']
    game.cubes[int(data['origin'])][int(data['color'])] = data['cubes']
    game.board.rows[int(data['origin'])] = data['rows']

def undo_cure(data, player, game):
    for card in data['cards']:
        game.player_cards.remove_from_discard(int(card))
        player.add_card(int(card))
    game.cures[data['color']] = LIVE
    game.cubes_left[data['color']] -= data['cubes']
    game.cubes[player.get_position()][data['color']] = data['cubes']
    game.board.rows[player.get_position()] = data['rows']

def undo_take(data, game):
    for p in game.players:
        if p.get_id() == data['taker']:
            taker = p
        elif p.get_id() == data['giver']:
            giver = p
    giver.take_card(int(data['card']), taker)
