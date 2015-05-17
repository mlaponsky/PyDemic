from app import app
from ..src.game import Game
from ..src.constants import *
from flask import render_template, flash, redirect, url_for, request, jsonify, \
                    session, Blueprint, g
import json
from ..forms import SetupForm
import random
import pickle
from copy import copy

phase = Blueprint('phase', __name__)

@phase.route('/_end_turn')
def end_turn():
    game = pickle.loads(session['game'])
    player = game.players[game.active]
    player_deck = game.player_cards.deck

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
    orig_cubes = copy(game.cubes)
    card = game.epidemic()
    color = card // CITIES_PER_COLOR
    orig = orig_cubes[card][color]
    row = game.board.get_row(card, color)
    session['game'] = pickle.dumps(game)
    return jsonify( card=card,
                    color=color,
                    row=row,
                    outbreak=game.outbreak,
                    cure=game.cures[color],
                    added=MAX_CUBES-orig,
                    outbreaks=game.num_outbreaks )

@phase.route('/_infect_phase')
def infect_phase():
    game = pickle.loads
