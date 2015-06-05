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
    player = game.players[game.active]

    recipients = [game.players.index(p) for p in game.players if player.can_give(card, p)]
    if len(recipients) == 1:
        action = game.give_card(recipients[0], card)
        actions.append(action)
        available, new_dispatch, origin, player_id = game.set_available(player)
        session['game'] = pickle.dumps(game)
        session['actions'] = actions
        return jsonify( card=str(card),
                        origin=player.get_position(),
                        recipient=game.players[recipients[0]].get_id(),
                        available=available,
                        num_cards=len(game.players[recipients[0]].hand),
                        can_cure=player.can_cure(game.research_stations),
                        can_build=player.can_build(player.get_position(), game.research_stations),
                        phase=game.phase )

    else:
        session['game'] = pickle.dumps(game)
        session['actions'] = actions
        return jsonify( card=str(card),
                        recipients=[game.players[r].get_id() for r in recipients] )

@cards.route('/_select_recipient')
def select_recipient():
    game = pickle.loads(session['game'])
    actions = session['actions']

    player = game.players[game.active]
    card = request.args.get('card', -1, type=int)
    recip = ( request.args.get('selected', 0, type=int) + game.active) % game.num_players
    recipient = game.players[recip]

    action = game.give_card(recip, card)
    available, new_dispatch, origin, player_id = game.set_available(0)
    actions.append(action)
    session['game'] = pickle.dumps(game)
    session['actions'] = actions
    return jsonify( card=str(card),
                    recipient=action['taker'],
                    recipients=[r.get_id() for r in game.players[game.active+1:] + game.players[:game.active]],
                    origin=player.get_position(),
                    available=available,
                    num_cards=len(recipient.hand),
                    can_cure=player.can_cure(game.research_stations),
                    can_build=player.can_build(player.get_position(), game.research_stations),
                    phase=game.phase )

@cards.route('/_take')
def take():
    game = pickle.loads(session['game'])
    actions = session['actions']

    player = game.players[game.active]
    card = request.args.get('card', -1, type=int)
    source = (request.args.get('id', 0, type=int) + game.active) % game.num_players

    action = game.take_card(source, card)
    actions.append(action)

    available, new_dispatch, origin, player_id = game.set_available(player)
    session['game'] = pickle.dumps(game)
    session['actions'] = actions
    return jsonify( card=str(card),
                    source_id=action['giver'],
                    available=available,
                    num_cards=len(player.hand),
                    can_cure=player.can_cure(game.research_stations),
                    can_build=player.can_build(player.get_position(), game.research_stations),
                    phase=game.phase )

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
               'available': prev_avail}
    if game.phase < DRAW:
        actions[-1]['trash'] = action
    owner.discard(card, game.player_cards)
    available, dispatch, origin, player_id = game.set_available(player)
    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( available=available,
                    origin=str(origin),
                    owner=owner.get_id(),
                    card=str(card),
                    num_cards=len(owner.hand),
                    can_cure=player.can_cure(game.research_stations),
                    can_build=player.can_build(player.get_position(), game.research_stations),
                    phase=game.phase )
