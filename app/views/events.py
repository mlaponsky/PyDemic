from app import app
from ..src.game import Game
from ..src.constants import *
from flask import render_template, flash, redirect, url_for, request, jsonify, \
                    session, Blueprint
import json
import random
import pickle
from copy import copy

events = Blueprint('events', __name__)

@events.route('/_execute_forecast')
def forecast():
    game = pickle.loads(session['game'])
    player = game.players[game.active]
    infect = game.infect_cards.get_deck()
    card0 = request.args.get('card0', infect[0], type=int)
    card1 = request.args.get('card1', infect[1], type=int)
    card2 = request.args.get('card2', infect[2], type=int)
    card3 = request.args.get('card3', infect[3], type=int)
    card4 = request.args.get('card0', infect[4], type=int)
    card5 = request.args.get('card0', infect[5], type=int)
    index = request.args.get('index', 0, type=int)
    owner = game.players[(game.active + index) % game.num_players]
    forecast = [ card0, card1, card2, card3, card4, card5 ]
    game.infect_cards.deck = forecast+infect[6:]

    owner.discard(FORECAST, game.player_cards)

    available, dispatch, origin, player_id = game.set_available(player)
    session['game'] = pickle.dumps(game)
    return jsonify( available=available,
                    owner=owner.get_id(),
                    position=origin )

@events.route('/_execute_rp')
def rp():
    game = pickle.loads(session['game'])
    actions = session['actions']

    player = game.players[game.active]
    card = request.args.get('remove', -1, type=int)
    index = request.args.get('index', 0, type=int)
    owner = game.players[(game.active + index) % game.num_players]

    game.infect_cards.remove_from_discard(card)
    game.infect_cards.add_to_graveyard(card)
    owner.discard(RP, game.player_cards)

    action = { 'act': 'rp',
                'owner': owner.get_id(),
                'deleted': card }
    actions.append(action)
    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( deleted=card )
