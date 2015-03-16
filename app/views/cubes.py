from app import app
from ..src.game import Game
from ..src.constants import *
from flask import render_template, flash, redirect, url_for, request, jsonify, \
                    session, Blueprint
import json
import random
import pickle
from copy import copy

disease = Blueprint('disease', __name__)

@disease.route('/_treat_disease')
def remove_cubes():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]
    board = game.board
    city = player.get_position()

    colors = []
    for color in COLORS:
        if game.cubes[city][color] != 0:
            colors.append(color)

    if len(colors) > 1:
        session['game'] = pickle.dumps(game)
        return jsonify( colors=colors )
    else:
        c = colors[0]
        starting_cubes = game.cubes[city][c]
        rows = copy(board.rows[city])
        player.treat(c, game.cures, game.cubes, game.cubes_left, board)
        cubes_removed = starting_cubes - game.cubes[city][c]
        cubes_left = game.cubes_left[c]
        action = { 'act': "treat", 'data': { 'origin': str(city),
                                             'color': str(c),
                                             'cubes': starting_cubes,
                                             'removed': cubes_removed,
                                             'rows': rows,
                                             'color_img': COLOR_IMG }}
        actions.append(action)
        session['actions'] = actions
        session['game'] = pickle.dumps(game)
        return jsonify( c=str(c),
                        num_cubes=cubes_removed,
                        cubes_left=cubes_left )

@disease.route('/_select_color')
def get_treatment_color():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]
    board = game.board
    city = player.get_position()
    color = request.args.get('color', 0, type=int)
    starting_cubes = game.cubes[city][color]
    rows = copy(board.rows[city])
    player.treat(color, game.cures, game.cubes, game.cubes_left, board)
    cubes_removed = starting_cubes - game.cubes[city][color]
    cubes_left = game.cubes_left[color]
    action = { 'act': "treat",  'data': { 'origin': str(city),
                                          'color': str(color),
                                          'cubes': starting_cubes,
                                          'removed': cubes_removed,
                                          'rows': rows,
                                          'color_img': COLOR_IMG }}
    actions.append(action)
    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( num_cubes=cubes_removed,
                    cubes_left=cubes_left )
