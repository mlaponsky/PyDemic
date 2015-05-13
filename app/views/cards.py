from app import app
from ..src.game import Game
from ..src.constants import *
from flask import render_template, flash, redirect, url_for, request, jsonify, \
                    session, Blueprint, g
import json
import random
import pickle
from copy import copy

cards = Blueprint('cards', __name__)

@cards.route('/_give_card')
def give():
    game = pickle.loads(session['game'])
    actions = session['actions']

    card = request.args.get('card', -1, type=int)
    recip = request.args.get('recip', 0, type=int)
    recip_id = (game.active + recip) % game.num_players
    player = game.players[game.active]
    team = game.players[game.active+1:] + game.players[:game.active]

    recipients = []
    for t in team:
        if player.can_give(card, t):
            recipients.append(t)
    if recip != game.active:
        recipients = [t for t in team if player.can_give(card, t)]
    if len(recipients) == 1:
        action = game.give_card(recip_id, card)
        actions.append(action)
        available, new_dispatch, origin, player_id = game.set_available(player)
        session['game'] = pickle.dumps(game)
        session['actions'] = actions
        return jsonify( card=str(card),
                        recipient=recipients[0].get_id(),
                        available=available,
                        num_cards=len(recipients[0].hand) )

    else:
        session['game'] = pickle.dumps(game)
        session['actions'] = actions
        return jsonify( card=str(card),
                        recipients=[r.get_id() for r in recipients] )

@cards.route('/_select_recipient')
def select_recipient():
    game = pickle.loads(session['game'])
    actions = session['actions']

    player = game.players[game.active]
    card = request.args.get('card', -1, type=int)
    recip = request.args.get('selected', 0, type=int)
    recipient = game.players[(game.active + recip) % game.num_players]

    action = game.give_card(recip, card)
    available, new_dispatch, origin, player_id = game.set_available(0)
    actions.append(action)
    session['game'] = pickle.dumps(game)
    session['actions'] = actions
    return jsonify( card=str(card),
                    recipient=action['taker'],
                    recipients=[r.get_id() for r in game.players[game.active+1:] + game.players[:game.active]],
                    available=available,
                    num_cards=len(recipient.hand) )

@cards.route('/_take')
def take():
    game = pickle.loads(session['game'])
    actions = session['actions']

    player = game.players[game.active]
    card = request.args.get('card', -1, type=int)
    source = request.args.get('id', 0, type=int)

    action = game.take_card(source, card)
    actions.append(action)

    available, new_dispatch, origin, player_id = game.set_available(player)
    session['game'] = pickle.dumps(game)
    session['actions'] = actions
    return jsonify( card=str(card),
                    source_id=action['giver'],
                    available=available,
                    num_cards=len(player.hand) )

@cards.route('/_trash')
def trash():
    game = pickle.loads(session['game'])
    actions = session['actions']

    card = request.args.get('card', -1, type=int)
    player = game.players[game.active]
    for p in game.players:
        if card in p.hand:
            owner = p
    prev_avail, dispatch, origin, player_id = game.set_available(player)

    action = { 'act': 'trash',
               'cards': str(card),
               'owner': owner.get_id(),
               'available': prev_avail }
    actions[-1]['trash'] = action
    owner.discard(card, game.player_cards)
    available, dispatch, origin, player_id = game.set_available(player)
    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( available=available,
                    origin=str(origin),
                    card=str(card) )
