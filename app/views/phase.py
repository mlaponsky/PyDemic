from app import app
from ..src.game import Game
from ..src.constants import *
from flask import render_template, flash, redirect, url_for, request, jsonify, \
                    session, Blueprint, g
import json
from ..forms import SetupForm
import random
import pickle
from copy import copy, deepcopy

phase = Blueprint('phase', __name__)

@phase.route('/_end_turn')
def end_turn():
    game = pickle.loads(session['game'])
    player = game.players[game.active]
    player_deck = game.player_cards.deck

    game.phase = 8
    draw0 = player_deck.pop(0)
    draw1 = player_deck.pop(0)
    draw = [draw0, draw1]
    for card in draw:
        if card != EPIDEMIC:
            player.add_card(card)

    session['game'] = pickle.dumps(game)
    session['actions'] = []
    return jsonify( draw_0=draw0,
                    draw_1=draw1,
                    num_cards=len(player.hand),
                    forecast=player_deck[:6] )

@phase.route('/_epidemic')
def execute_epidemic():
    game = pickle.loads(session['game'])
    player = game.players[game.active]
    orig_cubes = deepcopy(game.cubes)
    card = game.epidemic()
    color = card//CITIES_PER_COLOR
    orig = orig_cubes[card][color]
    row = game.board.get_row(card, color)
    session['game'] = pickle.dumps(game)
    return jsonify( card=card,
                    color=color,
                    rows=game.board.rows,
                    outbreak=game.outbreaks,
                    cure=game.cures[color],
                    added=MAX_CUBES-orig,
                    infected = game.infected,
                    outbreaks=game.num_outbreaks,
                    at_risk=game.at_risk )

@phase.route('/_infect')
def infect_phase():
    game = pickle.loads(session['game'])
    orig_cubes = deepcopy(game.cubes)
    game.reset_infection()
    outbreaks = []
    cards = []
    num_infect = game.get_infect_number()
    for i in range(num_infect):
        card = game.draw_infect_card(1)
        cards.append(card)
        outbreaks.append(copy(game.outbreaks))
    game.phase = ACTION_0
    session['game'] = pickle.dumps(game)
    return jsonify( infected=game.infected,
                    cards=cards,
                    outbreaks=outbreaks,
                    rows=game.board.rows,
                    at_risk=game.at_risk )

@phase.route('/_has_rp')
def has_rp():
    game = pickle.loads(session['game'])
    has_rp = False
    for p in game.players:
        if RP in p.hand or (p.get_role() == CP and p.event == RP):
            has_rp = True
    game = pickle.loads(session['game'])
    return jsonify( has_rp=has_rp )
