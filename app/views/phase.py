from app import app, db, google, models
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
    if len(game.player_cards.deck) <= 2:
        game.lose = True
        game_store = models.GameStore.query.filter_by(game_id=game.id).first()
        game_store.game = game
        db.session.commit()
        return jsonify( lose=game.lose )
    draw0 = player_deck.pop(0)
    draw1 = player_deck.pop(0)
    draw = [draw0, draw1]
    for card in draw:
        if card != EPIDEMIC:
            player.add_card(card)
        else:
            game.player_cards.discard.append(EPIDEMIC)
    oqn = game.oqn
    game.oqn = False

    session['game'] = pickle.dumps(game)
    session['actions'] = []
    return jsonify( draw_0=draw0,
                    draw_1=draw1,
                    num_cards=len(player.hand),
                    cards_left=len(game.player_cards.deck),
                    oqn=oqn )

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
    oqn = game.oqn
    game.oqn = False
    game.phase = EP
    if game.num_outbreaks >= 8:
        game.lose = True
    for cubes in game.cubes_left:
        if cubes <= 0:
            game.lose = True
    medic = None
    for p in game.players:
        if p.get_role() == MEDIC:
            medic = p
    if medic != None:
        for city in game.infected:
            for color in COLORS:
                if medic.get_position() == city and game.cures[color] == CURED:
                    game.cubes_left[color] += game.infected[city][color]
                    game.cubes[citty][color] -= game.infect[city][color]
                    game.infected[city][color] = 0

    session['game'] = pickle.dumps(game)
    if game.lose:
        game_store = models.GameStore.query.filter_by(game_id=game.id).first()
        game_store.game = game
        db.session.commit()
    return jsonify( card=card,
                    color=color,
                    rows=game.board.rows,
                    outbreaks=game.outbreaks,
                    cure=game.cures[color],
                    added=MAX_CUBES-orig,
                    drawn=game.drawn_epidemics,
                    infected = game.infected,
                    at_risk=game.at_risk,
                    has_rp=has_rp,
                    forecast=game.infect_cards.deck[:6],
                    oqn=oqn,
                    lose=game.lose )

@phase.route('/_infect')
def infect_phase():
    game = pickle.loads(session['game'])
    if game.phase < INFECT_1:
        game.phase = INFECT_1
    else:
        game.phase += 1
    orig_cubes = deepcopy(game.cubes)
    game.reset_infection()
    num_infect = game.get_infect_number()
    card = game.draw_infect_card(1)
    color = card//CITIES_PER_COLOR
    medic = None
    for p in game.players:
        if p.get_role() == MEDIC:
            medic = p
    if medic != None:
        for city in game.infected:
            for c in COLORS:
                if medic.get_position() == city and game.cures[c] == CURED:
                    game.cubes_left[c] += game.infected[city][c]
                    game.cubes[city][c] -= game.infect[city][c]
                    game.infected[city][c] = 0
    if game.lose:
        game_store = models.GameStore.query.filter_by(game_id=game.id).first()
        game_store.game = game
        db.session.commit()
    session['game'] = pickle.dumps(game)
    return jsonify( infected=game.infected,
                    card=card,
                    color=color,
                    cure=game.cures[color],
                    outbreaks=game.outbreaks,
                    rows=game.board.rows,
                    at_risk=game.at_risk,
                    counter=game.phase - EP,
                    total=num_infect,
                    forecast=game.infect_cards.deck[:6],
                    phase=game.phase,
                    lose=game.lose )

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
    oqn = game.oqn
    game.oqn = False
    session['game'] = pickle.dumps(game)
    return jsonify(at_risk=game.at_risk,
                   has_rp=has_rp,
                   oqn=oqn,
                   forecast=game.infect_cards.deck[:6])

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

    game.next_turn()

    player = game.players[game.active]
    board = game.board
    available = []
    pieces = []
    roles = []
    positions = []

    team = game.players[game.active:] + game.players[:game.active]
    available, dispatch, origin, player_id = game.set_available(0)
    available = available + dispatch
    for p in team:
        pieces.append(ROLES[p.get_role()]['piece_img'])
        roles.append(p.get_id())
        positions.append(str(p.get_position()))

    can_take, can_give, team_hands = game.set_share()
    can_build = player.can_build( player.get_position(), game.research_stations)
    can_cure = player.can_cure(game.research_stations)

    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    if 'google_token' in session:
        game_store = models.GameStore.query.filter_by(game_id=game.id).first()
        game_store.game = game
        game_store.actions = actions
        db.session.commit()

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
