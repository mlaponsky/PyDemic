from app import app
from ..src.game import Game
from ..src.constants import *
from flask import render_template, flash, redirect, url_for, request, jsonify, \
                    session, Blueprint, g
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
    city = player.get_position()

    colors = []
    for color in COLORS:
        if game.cubes[city][color] != 0:
            colors.append(color)

    if len(colors) > 1:
        session['game'] = pickle.dumps(game)
        return jsonify( colors=colors )
    else:
        color = colors[0]
        action = game.treat(color)
        actions.append(action)
        session['actions'] = actions
        session['game'] = pickle.dumps(game)
        return jsonify( c=str(color),
                        num_cubes=action['removed'],
                        cubes_left=game.cubes_left[color],
                        at_risk=game.at_risk )

@disease.route('/_select_color')
def get_treatment_color():
    game = pickle.loads(session['game'])
    actions = session['actions']
    player = game.players[game.active]
    color = request.args.get('color', 0, type=int)
    action = game.treat(color)
    actions.append(action)
    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( num_cubes=action['removed'],
                    cubes_left=game.cubes_left,
                    at_risk=game.at_risk )
