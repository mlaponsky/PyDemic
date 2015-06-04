from app import app, db, google, models
from ..src.game import Game
from ..src.constants import *
from flask import render_template, g, flash, redirect, url_for, request, jsonify, \
                    session, Blueprint
import json
from ..forms import SetupForm
import random
import pickle
import flask_oauthlib
from copy import copy

load = Blueprint('load', __name__)

@load.route('/', methods=['GET','POST'])
@load.route('/index', methods=['GET', 'POST'])
@load.route('/setup', methods=['GET','POST'])
def setup():
    available_roles = [CP, DISPATCHER, MEDIC, OE, QS, RESEARCHER, SCIENTIST]
    form = SetupForm()
    if form.validate_on_submit():
        roles = [ form.char0.data, form.char1.data, form.char2.data, form.char3.data ]
        chosen = []
        for role in roles:
            if role != 'random' and role != 'none':
                available_roles.remove(role)
                chosen.append(role)
        for role in roles:
            if role == "random":
                r = random.choice(available_roles)
                available_roles.remove(r)
                chosen.append(r)
        if len(chosen) < 2:
            flash("You must select at least 2 players.")
            return render_template("setup.html",
                                    title="Pandemic Setup",
                                    form=form)
        game = Game(chosen, form.difficulty.data)
        actions = []
        if 'google_token' in session:
            data = google.get('userinfo').data
            user = models.User.query.filter_by(email=data['email']).first()
            prev_game = models.GameStore.query.filter_by(game_id=user.game_id).first()
            if prev_game != None and not prev_game.game.win and not prev_game.game.lose:
                db.session.delete(prev_game)
            user.game_id = game.id
            game_store = models.GameStore(game_id=game.id, game=game, actions=actions, original=game, author=user)
            db.session.add(game_store)
            db.session.commit()
        session['game'] = pickle.dumps(game)
        session['original'] = pickle.dumps(game)
        session['actions'] = actions
        return redirect(url_for('load.start_game'))
    if 'google_token' in session:
        data = google.get('userinfo').data
        if 'email' in data:
            user = models.User.query.filter_by(email=data['email']).first()
        else:
            return redirect(url_for('login.logout_user'))

        try:
            if user.game_id != None:
                game_id = user.game_id
                game = models.GameStore.query.filter_by(game_id=game_id).first().game
                print('Logged in with saved game finished', game.win, game.lose)
                can_resume = not game.win and not game.lose
            else:
                print('Logged in with no saved game.')
                can_resume = False
        except AttributeError:
            session.pop('google_token')
            return redirect(url_for('load.setup'))
    else:
        print('Not logged in.')
        can_resume = False
    return render_template("setup.html",
                            title="Pandemic Setup",
                            form=form,
                            can_resume=can_resume)

@load.route('/_resume')
def resume():
    data = google.get('userinfo').data
    user = models.User.query.filter_by(email=data['email']).first()
    game_store = models.GameStore.query.filter_by(game_id=user.game_id).first()
    game = game_store.game
    actions = game_store.actions
    game.new = True;
    session['game'] = pickle.dumps(game)
    session['actions'] = actions
    return redirect(url_for('load.start_game'))

@load.route('/_load')
def set_game():
    try:
        data = google.get('userinfo').data
        user = models.User.query.filter_by(email=data['email']).first()
        game_store = models.GameStore.query.filter_by(game_id=user.game_id).first()
        game = game_store.game
        actions = game_store.actions
        game_store.game.new = False;
    except flask_oauthlib.client.OAuthException:
        game = pickle.loads(session['game'])
        actions = session['actions']
    player = game.players[game.active]
    board = game.board
    available = []
    pieces = []
    roles = []
    positions = []

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

    research_stations = copy(game.research_stations)
    can_build = player.can_build( player.get_position(), research_stations)
    can_cure = player.can_cure(research_stations)
    available, dispatch, origin, player_id = game.set_available(0)
    available = available+dispatch
    cubes = {}
    rows = {}
    cures = game.cures
    hand = player.hand

    for city in range(NUM_CITIES):
        if not all(v==0 for v in game.cubes[city]):
            cubes[city] = game.cubes[city]
            rows[city] = board.get_all_rows(city)

    store = None
    for p in game.players:
        if p.get_role() == CP:
            store = p.event

    session['actions'] = actions
    session['game'] = pickle.dumps(game)
    return jsonify( available=available,
                    pieces=pieces,
                    roles=roles,
                    positions=positions,
                    cubes=cubes,
                    cube_rows=rows,
                    cures=cures,
                    rs=research_stations,
                    can_build=can_build,
                    can_cure=can_cure,
                    role_img=ROLES[player.get_role()]['title_img'],
                    hand=hand,
                    team_hands=team_hands,
                    can_give=can_give,
                    can_take=can_take,
                    forecast=game.infect_cards.deck[:6],
                    store=store,
                    player_discard=game.player_cards.discard,
                    player_grave=game.player_cards.graveyard,
                    infect_discard=game.infect_cards.discard,
                    infect_grave=game.infect_cards.graveyard,
                    at_risk=game.at_risk,
                    drawn_epidemics=game.drawn_epidemics,
                    num_outbreaks=game.num_outbreaks,
                    actions=actions,
                    phase=game.phase )

@load.route('/game')
def start_game():
    try:
        print('Getting game from user.')
        data = google.get('userinfo').data
        user = models.User.query.filter_by(email=data['email']).first()
        game_store = models.GameStore.query.filter_by(game_id=user.game_id).first()
        game = game_store.game
        actions = game_store.actions
    except flask_oauthlib.client.OAuthException:
        try:
            game = pickle.loads(session['game'])
        except:
            return redirect(url_for('load.setup'))
    if not game.new:
        return redirect(url_for('load.setup'))

    active_player = game.players[game.active]
    team = game.players[game.active:] + game.players[:game.active]
    game.new = False

    session['game'] = pickle.dumps(game)
    return render_template("index.html",
                            title = 'GAME',
                            game = game,
                            active_player = active_player,
                            team = team,
                            cards = CARDS,
                            cities = CITIES,
                            colors = COLOR_STRINGS,
                            num_cities=NUM_CITIES,
                            num_epidemics=game.num_epidemics )

@load.route('/_restart')
def restart_game():
    session['game'] = session['original']
    if 'google_token' in session:
        data = google.get('userinfo').data
        user = models.User.query.filter_by(email=data['email']).first()
        game_store = models.GameStore.query.filter_by(game_id=user.game_id).first()
        game_store.game = game_store.original
        db.session.add(game_store)
        db.session.commit()
    return redirect(url_for('load.start_game'))
