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

movement = Blueprint('movement', __name__)

@movement.route('/_move', methods=["GET", "POST"])
def set_move():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]
    board = game.board
    origin = player.get_position()
    new_pos = request.args.get('id', 0, type=int)
    is_airlift = request.args.get('airlift', 0, type=int)
    index = request.args.get('index', 0, type=int)
    adding = request.args.get('adding', 0, type=int)
    owner = game.players[(game.active + index) % game.num_players ]
    discard = ""
    cures = copy(game.cures)
    move = ""

    selectable = []

    # neighbors = game.board.get_neighbors(origin)
    new_neighbors = game.board.get_neighbors(new_pos)
    can_charter = player.can_charter(game.research_stations, board)
    can_fly_direct = player.can_fly_direct(board)

    prev_avail, dispatch, origin, player_id = game.set_available(player)
    prev_hand = copy(player.hand)
    prev_take, prev_give, prev_hands = game.set_share()
    prev_build = player.can_build(origin, game.research_stations)
    prev_cure = player.can_cure(game.research_stations)
    orig_cubes = copy(game.cubes[new_pos])
    orig_rows = copy(board.rows[new_pos])

    if is_airlift == 1:
        player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
        discard = str(AIRLIFT)
        owner.discard(AIRLIFT, game.player_cards)
        move = "airlift"
    elif new_pos in player.can_drive(board):
        player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
        move="drive"
    elif new_pos in dispatch:
        player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
        move="dispatch"
    elif new_pos in player.can_shuttle(game.research_stations):
        player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
        move = "shuttle"
    elif player.get_role() == OE and new_pos in player.can_station_fly(game.research_stations, board):
        for card in player.hand:
            if card in range(NUM_CITIES):
                selectable.append( str(card) )
        if len(selectable) == 1:
            player.discard( int(selectable[0]), game.player_cards )
            discard = selectable[0]
            player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
            move = "station-fly"
    elif new_pos in can_fly_direct and new_pos not in can_charter:
        player.discard(new_pos, game.player_cards)
        player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
        discard = str(new_pos)
        move = "fly"
    elif new_pos in can_charter and new_pos not in can_fly_direct:
        player.discard(origin, game.player_cards)
        discard = origin
        player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
        move = "charter"

    elif new_pos in can_charter and new_pos in can_fly_direct:
        selectable.append( str(new_pos) )
        selectable.append( str(origin) )
    else:
        player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
        move = "shuttle"

    if len(selectable) > 1:
        session['actions'] = actions
        session['game'] = pickle.dumps(game)
        return jsonify(selectable=selectable)
    else:
        action = { 'act': move,
                    'id': player_id,
                    'origin': origin,
                    'destination': new_pos,
                    'cards': discard,
                    'owner': owner.get_id(),
                    'available': prev_avail,
                    'can_build': prev_build,
                    'can_cure': prev_cure,
                    'cubes': orig_cubes,
                    'rows': orig_rows,
                    'color_img': COLOR_IMG,
                    'card_data': CARDS[int(discard)] if discard != '' else 'none',
                    'hand': prev_hand,
                    'team_hands': prev_hands,
                    'give': prev_give,
                    'take': prev_take }
        if adding == 0:
            actions.append(action)
        else:
            actions[0]['trash'] = action
        available, new_dispatch, origin, player_id = game.set_available(player)
        can_take, can_give, team_hands = game.set_share()

        if is_airlift == 1 or player.get_role() != DISPATCHER:
            player.selected = player
        if player.get_role() == MEDIC:
            cubes_left = copy(game.cubes_left)
            can_build = player.can_build(new_pos, game.research_stations)
            can_cure = player.can_cure(game.research_stations)
            session['actions'] = actions
            session['game'] = pickle.dumps(game)
            print(can_give)
            return jsonify( available=available,
                            player_id=player_id,
                            move=move,
                            origin=action['origin'],
                            discard=discard,
                            cures=cures,
                            cubes_left=cubes_left,
                            can_build=can_build,
                            hand=player.hand,
                            team_hands=team_hands,
                            can_cure=can_cure,
                            can_take=can_take,
                            can_give=can_give,
                            num_cards=len(owner.hand) )
        else:
            can_build = player.can_build(new_pos, game.research_stations)
            can_cure = player.can_cure(game.research_stations)
            session['actions'] = actions
            session['game'] = pickle.dumps(game)
            print(player.hand)
            return jsonify( available=available,
                            player_id=player_id,
                            move=move,
                            origin=action['origin'],
                            discard=discard,
                            can_build=can_build,
                            can_cure=can_cure,
                            hand=player.hand,
                            team_hands=team_hands,
                            can_take=can_take,
                            can_give=can_give,
                            num_cards=len(owner.hand) )

@movement.route('/_select_card_for_move')
def select_move_card():
    game = pickle.loads(session['game'])
    actions = session['actions']
    board = game.board
    player = game.players[game.active]
    discard = request.args.get('card', 0, type=int)
    origin = player.get_position()
    new_pos = request.args.get('city_id', 0, type=int)

    cubes_left = copy(game.cubes_left)
    cures = copy(game.cures)
    action = 0

    prev_avail, dispatch, origin, player_id = game.set_available(player)
    prev_build = player.can_build(origin, game.research_stations)
    prev_cure = player.can_cure(game.research_stations)
    prev_hand = copy(player.hand)
    prev_take, prev_give, prev_hands = game.set_share()
    orig_cubes = game.cubes[new_pos]
    orig_rows = board.rows[new_pos]

    player.discard(discard, game.player_cards)
    if discard == origin:
        move = "charter"
    elif discard == new_pos:
        move = "fly"
    elif player.get_role() == OE:
        player.has_stationed = True
        move = "station-fly"

    action = { 'act': move,
                'id': player_id,
                'origin': origin,
                'destination': new_pos,
                'cards': discard,
                'owner': player.get_id(),
                'available': prev_avail,
                'can_build': prev_build,
                'can_cure': prev_cure,
                'cubes': orig_cubes,
                'rows': orig_rows,
                'color_img': COLOR_IMG,
                'card_data': CARDS[int(discard)] if discard != '' else 'none',
                'hand': prev_hand,
                'team_hands': prev_hands,
                'give': prev_give,
                'take': prev_take }
    actions.append(action)

    player.move(new_pos, board, game.cures, game.cubes, game.cubes_left, game.quarantined)
    can_build = player.can_build(new_pos, game.research_stations)
    can_cure = player.can_cure(game.research_stations)
    available, new_dispatch, origin, player_id = game.set_available(player)
    can_take, can_give, team_hands = game.set_share()

    if player.get_role() != DISPATCHER:
        player.selected = player
    if player.get_role() == MEDIC:
        session['actions'] = actions
        session['game'] = pickle.dumps(game)
        return jsonify( available=available,
                        player_id=player_id,
                        move=move,
                        origin=action['origin'],
                        cures=cures,
                        cubes_left=cubes_left,
                        can_build=can_build,
                        can_cure=can_cure,
                        hand=player.hand,
                        team_hands=team_hands,
                        can_take=can_take,
                        can_give=can_give,
                        num_cards=len(owner.hand) )
    else:
        session['actions'] = actions
        session['game'] = pickle.dumps(game)
        return jsonify( available=available,
                        player_id=player_id,
                        move=move,
                        origin=action['origin'],
                        can_build=can_build,
                        can_cure=can_cure,
                        hand=player.hand,
                        team_hands=team_hands,
                        can_take=can_take,
                        can_give=can_give,
                        num_cards=len(owner.hand) )

@movement.route('/_select_player')
def select_player():
    game = pickle.loads(session['game'])
    index = request.args.get('index', 0, type=int)
    is_airlift = request.args.get('airlift', 0, type=int)
    player = game.players[game.active]
    selected = game.players[(game.active + index) % game.num_players]
    player.selected = selected
    position = selected.get_position()
    if is_airlift == 1:
        available = []
        for city in range(NUM_CITIES):
            if city != position:
                available.append(str(city))
    else:
        available, dispatch, origin, player_id = game.set_available(player)
    can_build = player.can_build(player.get_position(), game.research_stations)
    can_cure = player.can_cure(game.research_stations)
    session['game'] = pickle.dumps(game)
    return jsonify( available=available,
                    role=selected.get_id(),
                    position=position,
                    can_build=can_build,
                    can_cure=can_cure )
