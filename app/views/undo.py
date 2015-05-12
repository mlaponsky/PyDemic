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

undo = Blueprint('undo', __name__)

@undo.route('/_undo')
def undo_action():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]
    action = actions.pop(-1)
    data = action

    if 'trash' in data:
        trash = data['trash']

    if action['act'] == "drive" or action['act'] == "shuttle" or action['act'] == "dispatch":
        undo_move(data, player, game)
    elif action['act'] == "charter" or action['act'] == "fly" or action['act'] == "airlift":
        for p in game.players:
            if p.get_id() == data['owner']:
                owner = p
        undo_move(data, player, game)
        undo_discard(data, owner, game)
    elif action['act'] == "station-fly":
        undo_move(data, player, game)
        undo_discard(data, player, game)
        player.has_stationed = False
    elif action['act'] == "build" or action['act'] == "gg":
        undo_station(data, player, game)
    elif action['act'] == "treat":
        undo_treatment(data, game)
    elif action['act'] == "cure":
        undo_cure(data, player, game)
    elif action['act'] == "take":
        undo_take(data, game)
    elif action['act'] == "give":
        undo_give(data, game)
    elif action['act'] == "rp":
        undo_rp(data, game)
    elif action['act'] == "oqn":
        undo_oqn(data, game)

    undo_trash(data, game, player)

    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify(result=action)

def undo_move(data, player, game):
    if player.get_id() != data['mover']:
        for p in game.players:
            if p.get_id() == data['mover']:
                p.position = data['origin']
                if data['mover'] == 'qs':
                    game.quarantined = game.board.get_neighbors(p.get_position())
                    game.quarantined.append(p.get_position())
    else:
        player.position = data['origin']
        if data['id'] == 'qs':
            game.quarantined = game.board.get_neighbors(player.get_position())
            game.quarantined.append(player.get_position())

    for color in COLORS:
        number = data['cubes'][color]
        if number != game.cubes[data['destination']][color]:
            game.cubes[data['destination']][color] = number
            game.cubes_left[color] += number
    game.board.rows[data['destination']] = data['rows']
    if 'trash' in data:
        undo_trash

def undo_discard(data, player, game):
    if int(data['cards']) in game.player_cards.discard:
        game.player_cards.remove_from_discard(int(data['cards']))
        player.add_card(int(data['cards']))
    elif int(data['cards']) in game.player_cards.graveyard:
        game.player_cards.remove_from_graveyard(int(data['cards']))
        player.event = int(data['cards'])

def undo_station(data, player, game):
    game.research_stations.remove(int(data['origin']))
    if data['removed'] != 'none':
        game.research_stations.append(int(data['removed']))
    if data['discard'] != -1:
        for p in game.players:
            if p.get_id() == data['owner']:
                owner = p
        undo_discard(int(data['discard']), owner, game)

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

def undo_give(data, game):
    for p in game.players:
        if p.get_id() == data['taker']:
            taker = p
        elif p.get_id() == data['giver']:
            giver = p
    taker.give_card(int(data['card']), giver)

def undo_rp(data, game):
    game.infect_cards.graveyard.remove(data['deleted'])
    game.infect_cards.add_to_discard(data['deleted'])
    for p in game.players:
        if p.get_id() == data['owner']:
            owner = p
    undo_discard(RP, owner, game)

def undo_oqn(data, game):
    game.oqn = False
    for p in game.players:
        if p.get_id() == data['owner']:
            owner = p
    undo_discard(OQN, owner, game)

def undo_trash(data, game, player):
    if 'trash' in data:
        trash = data['trash']
        if 'owner' in trash:
            for p in game.players:
                if p.get_id() == trash['owner']:
                    owner = p
        if trash['act'] == 'airlift':
            undo_move(trash, player, game)
            undo_discard(trash, owner, game)
        elif trash['act'] == 'gg':
            undo_station(trash, player, game)
        elif trash['act'] == 'rp':
            undo_rp(trash, game)
        elif trash['act'] == 'oqn':
            undo_oqn(trash, game)
        else:
            undo_discard(trash, owner, game)
