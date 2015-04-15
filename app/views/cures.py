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

cures = Blueprint('cures', __name__)

@cures.route('/_make_cure')
def make_cure():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]

    prev_avail, dispatch, origin, player_id = game.set_available(player)

    needed = 5 if player.get_role() != SCIENTIST else 4
    if player.can_cure(game.research_stations):
        cure_cards = player.get_cure_cards()
    cure_color = cure_cards[0] // CITIES_PER_COLOR
    if len(cure_cards) == needed:
        execute_cure(cure_color, cure_cards, player, game, actions, prev_avail)

        available, new_dispatch, origin, player_id = game.set_available(player)
        session['actions'] = actions
        session['game'] = pickle.dumps(game)
        return jsonify( c=cure_color,
                        cured=game.cures[cure_color],
                        cards=[str(card) for card in cure_cards],
                        role=player.get_id(),
                        position=str(player.get_position()),
                        cubes_left=game.cubes_left[cure_color],
                        available=available )
    else:
        session['game'] = pickle.dumps(game)
        return jsonify( cards=[str(card) for card in cure_cards],
                        needed=needed )

@cures.route('/_select_cure')
def select_cure():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]

    prev_avail, dispatch, origin, player_id = game.set_available(player)
    card0 = request.args.get('card0', -1, type=int)
    card1 = request.args.get('card1', -1, type=int)
    card2 = request.args.get('card2', -1, type=int)
    card3 = request.args.get('card3', -1, type=int)
    card4 = request.args.get('card4', -1, type=int)

    cure_cards = [ card0, card1, card2, card3, card4 ]
    cure_cards = [ card for card in cure_cards if card != -1]

    needed = 5 if player.get_role() != SCIENTIST else 4
    cure_color = cure_cards[0] // CITIES_PER_COLOR
    execute_cure(cure_color, cure_cards, player, game, actions, prev_avail)
    available, new_dispatch, origin, player_id = game.set_available(player)
    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( c=cure_color,
                    cured=game.cures[cure_color],
                    role=player.get_id(),
                    position=str(player.get_position()),
                    cubes_left=game.cubes_left[cure_color],
                    available=available )


def execute_cure(cure_color, cure_cards, player, game, actions, prev_avail):
    game.cures[ cure_color ] = CURED
    player.make_cure(cure_cards, game.player_cards)
    orig_cubes = game.cubes[player.get_position()][cure_color]
    orig_rows = copy(game.board.get_all_rows(player.get_position()))
    for p in game.players:
        if p.get_role() == MEDIC:
            game.cubes_left[cure_color] += game.cubes[player.get_position()][cure_color]
            game.cubes[player.get_position()][cure_color] = 0
            game.board.delete_row(player.get_position(), cure_color)
            break
    eradicated = game.is_eradicated(cure_color)
    if eradicated:
        game.cures[ cure_color ] = ERADICATED

    action = { 'act': 'cure',
                'color': cure_color,
                'cured': 0,
                'cards': [str(card) for card in cure_cards],
                'origin': str(player.get_position()),
                'cubes': orig_cubes,
                'rows': orig_rows,
                'color_img': COLOR_IMG,
                'card_data': [CARDS[card] for card in cure_cards],
                'available': prev_avail }
    actions.append(action)
