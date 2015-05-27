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

    game.phase = DRAW
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
    has_rp = game.has_rp()

    session['game'] = pickle.dumps(game)
    return jsonify( card=card,
                    color=color,
                    rows=game.board.rows,
                    outbreaks=game.outbreaks,
                    cure=game.cures[color],
                    added=MAX_CUBES-orig,
                    drawn=game.drawn_epidemics,
                    infected = game.infected,
                    at_risk=game.at_risk,
                    has_rp=has_rp )

@phase.route('/_infect')
def infect_phase():
    game = pickle.loads(session['game'])
    game.phase += 1
    orig_cubes = deepcopy(game.cubes)
    game.reset_infection()
    num_infect = game.get_infect_number()
    card = game.draw_infect_card(1)
    color = card//CITIES_PER_COLOR
    session['game'] = pickle.dumps(game)
    return jsonify( infected=game.infected,
                    card=card,
                    color=color,
                    cure=game.cures[color],
                    outbreaks=game.outbreaks,
                    rows=game.board.rows,
                    at_risk=game.at_risk,
                    counter=game.phase - DRAW,
                    total=num_infect )

@phase.route('/_has_rp')
def has_rp():
    game = pickle.loads(session['game'])
    has_rp = False
    for p in game.players:
        if RP in p.hand or (p.get_role() == CP and p.event == RP):
            has_rp = True
    session['game'] = pickle.dumps(game)
    return jsonify( has_rp=has_rp )

@phase.route('/_finish_ep')
def finish_epidemic():
    game = pickle.loads(session['game'])
    game.finish_epidemic()
    has_rp = game.has_rp()
    session['game'] = pickle.dumps(game)
    return jsonify(at_risk=game.at_risk,
                   has_rp=has_rp)

@phase.route('/_ep_rp')
def ep_rp():
    game = pickle.loads(session['game'])
    card = request.args.get('card', 0, type=int)
    index = 0
    for p in game.players:
        if RP in p.hand or (p.get_role() == CP and p.event == RP):
            index = game.players.index(p)
    action = game.play_rp(card, index)
    game.finish_epidemic()
    session['game'] = pickle.dumps(game)
    return jsonify( is_stored=action['is_stored'],
                    owner=action['owner'] )

@phase.route('/_next_turn')
def next_turn():
    game = pickle.loads(session['game'])
    actions = session['actions']
    actions = []
    game.phase = ACTION_0
    game.active = (game.active+1) % game.num_players
    game.selected = game.active
    board = game.board
    available = []
    pieces = []
    roles = []
    positions = []

    player = game.players[game.active]
    team = game.players[game.active:] + game.players[:game.active]
    if game.players[game.active].get_role() == DISPATCHER:
        for p in team:
            if p != game.players[game.active] and p.get_position() != game.players[game.active].get_position():
                available.append(p.get_position())
    for p in team:
        pieces.append(ROLES[p.get_role()]['piece_img'])
        roles.append(p.get_id())
        positions.append(str(p.get_position()))

    can_take, can_give, team_hands = game.set_share()
    can_build = player.can_build( player.get_position(), game.research_stations)
    can_cure = player.can_cure(game.research_stations)
    for city in player.can_move(player.hand, game.research_stations, board):
        available.append(str(city))

    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( available=available,
                    pieces=pieces,
                    roles=roles,
                    icon=player.piece,
                    positions=positions,
                    can_build=can_build,
                    can_cure=can_cure,
                    role_img=ROLES[player.get_role()]['title_img'],
                    hand=player.hand,
                    team_hands=team_hands,
                    can_give=can_give,
                    can_take=can_take,
                    forecast=game.infect_cards.deck[:6],
                    at_risk=game.at_risk,
                    phase=game.phase )
