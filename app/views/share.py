from app import app
from ..src.game import Game
from ..src.constants import *
from flask import render_template, flash, redirect, url_for, request, jsonify, \
                    session, Blueprint
import json
import random
import pickle
from copy import copy

share = Blueprint('share', __name__)

@share.route('/_give_card')
def give():
    game = pickle.loads(session['game'])
    actions = session['actions']

    card = request.args.get('card', -1, type=int)
    player = game.players[game.active]
    team = game.players[game.active+1:] + game.players[:game.active]

    recipients = []
    for t in team:
        if player.can_give(card, t):
            recipients.append(t)
    prev_avail, dispatch, origin, player_id = game.set_available(player)
    if len(recipients) == 1:
        action = { 'act': 'give', 'data': { 'card': str(card),
                                            'giver': player.get_id(),
                                            'taker': recipients[0].get_id(),
                                            'available': prev_avail }}
        actions.append(action)

        player.give_card(card, recipients[0])
        available, new_dispatch, origin, player_id = game.set_available(player)
        session['game'] = pickle.dumps(game)
        session['actions'] = actions
        return jsonify( card=str(card),
                        recipient=recipients[0].get_id(),
                        available=available )

    else:
        session['game'] = pickle.dumps(game)
        session['actions'] = actions
        return jsonify( card=str(card),
                        recipients=[r.get_id() for r in recipients] )

@share.route('/_select_recipient')
def select_recipient():
    game = pickle.loads(session['game'])
    actions = session['actions']

    player = game.players[game.active]
    card = request.args.get('card', -1, type=int)
    index = request.args.get('selected', -1, type=int)
    recipient = game.players[(game.active + index) % game.num_players]
    prev_avail, dispatch, origin, player_id = game.set_available(player)

    action = { 'act': 'give', 'data': { 'card': str(card),
                                        'giver': player.get_id(),
                                        'taker': recipient.get_id(),
                                        'available': prev_avail }}
    actions.append(action)

    player.give_card(card, recipient)
    available, new_dispatch, origin, player_id = game.set_available(player)
    session['game'] = pickle.dumps(game)
    session['actions'] = actions
    return jsonify( card=str(card),
                    recipient=recipient.get_id(),
                    available=available )

@share.route('/_take')
def take():
    game = pickle.loads(session['game'])
    actions = session['actions']

    player = game.players[game.active]
    card = request.args.get('card', -1, type=int)
    source_id = request.args.get('id', '', type=str)
    for p in game.players:
        if p.get_id() == source_id:
            source = p

    prev_avail, dispatch, origin, player_id = game.set_available(player)

    action = { 'act': 'take', 'data': { 'card': str(card),
                                        'taker': player.get_id(),
                                        'giver': source.get_id(),
                                        'available': prev_avail }}
    print(prev_avail)
    actions.append(action)

    player.take_card(card, source)
    available, new_dispatch, origin, player_id = game.set_available(player)
    session['game'] = pickle.dumps(game)
    session['actions'] = actions
    return jsonify( card=str(card),
                    source_id=source.get_id(),
                    available=available )
