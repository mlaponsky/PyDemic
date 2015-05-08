# -*- coding: utf-8 -*-

from .player import *
from .board import Board
from .deck import Deck, PlayerCards, InfectCards
from .constants import *
from random import shuffle
from uuid import uuid4

class Game:
    def __init__(self, roles, epidemics):
        self.lose = False
        self.day = 0
        self.phase = 4
        self.id = uuid4()

        self.num_outbreaks = 0
        self.num_epidemics = 0
        self.drawn_epidemics = 0

        self.num_players = 0
        self.players = []

        self.from_discard = []

        # cubes[city][color]
        self.cubes = []
        for city in range(NUM_CITIES):
             self.cubes.append([0] * 4)
        self.cubes_left = [NUM_CUBES] * 4
        self.cures = [0] * 4

        self.research_stations = []
        self.quarantined = []
        self.outbreaks = []

        self.board = Board()
        self.num_epidemics = epidemics
        self.num_players = len(roles)
        self.research_stations.append(ATL)
        self.infect_cards = InfectCards()

        self.initial_infect()
        self.oqn = False

        for role in roles:
            self.players.append(self.assign_player(role))

        self.player_cards = PlayerCards(self.players, self.num_epidemics)
        self.active = self.set_order()
        self.selected = self.active

    ## Manage game phase
    def get_phase(self):
        return self.phase

    def set_phase(self, phase):
        self.phase = phase

    def assign_player(self, role):
        if role == MEDIC:
            player = Medic()
        elif role == DISPATCHER:
            player = Dispatcher()
        elif role == CP:
            player = ContingencyPlanner()
        elif role == OE:
            player = OperationsExpert()
        elif role == QS:
            player = QuarantineSpecialist(self.quarantined, self.board.get_neighbors(ATL))
        elif role == RESEARCHER:
            player = Researcher()
        elif role == SCIENTIST:
            player = Scientist()
        else:
            player = None
        return player

    def set_order(self):
        first_player_index = -1
        highest_card = 0
        for player in self.players:
            for card in player.hand:
                if CARDS[card]['population'] > highest_card:
                    highest_card = CARDS[card]['population']
                    first_player_index = self.players.index(player)
        return first_player_index

    def select_player(self, index):
        self.selected = (index + self.active) % self.num_players
        return self.players[self.selected]

    def dispatcher_availability(self, available):
        dispatch = []
        for p in self.players:
            if self.selected != p and self.selected.get_position() != p.get_position():
                available.append(str(p.get_position()))
                dispatch.append(p.get_position())
        return dispatch

    def set_available(self, is_airlift):
        dispatch = []
        available = []
        player = self.players[self.active]
        selected = self.players[self.selected]
        player_id = selected.get_id()
        origin = selected.get_position()

        if is_airlift == 1:
            available = []
            for city in range(NUM_CITIES):
                if city != position:
                    available.append(str(city))
        else:
            if player.get_id() == 'dispatcher':
                dispatch = self.dispatcher_availability(available)
            for city in player.can_move(self.research_stations, self.board):
                available.append(str(city))
        return available, dispatch, origin, player_id

    def set_share(self):
        can_give = {}
        can_take = {}
        player = self.players[self.active]
        team = self.players[self.active:] + self.players[:self.active]
        team_hands = {}
        for p in team[1:]:
            can_take[p.get_id()] = []
            can_give[p.get_id()] = []
            team_hands[p.get_id()] = copy(p.hand)
            for card in p.hand:
                can_take[p.get_id()].append(player.can_take(card, p))
            for card in player.hand:
                can_give[p.get_id()].append(player.can_give(card, p))
        return can_take, can_give, team_hands

    ## The procedures for adding cubes.
    '''
    The below function is a generic cube adding function. It takes the color and number of cubes to be added, and the city to infect. This function is implemented in all situations in which a city would be infected. A normal infect city action will just call the function directly with numCubes = 1. The other cube-adding scenarios are outbreak and epidemic. Notice the recursive coupling between infect and outbreak below, and infect will call outbreak when it would go over the cube limit, and outbreaks will infect, potentially chaining into other outbreaks. The outbreak function handles all conditions for outbreaks, and tracks outbreaks that have already occurred on a turn so as not to repeat. The function to reset the outbreak array is called after each epidemic AND each infect stage.
    '''
    def initial_infect(self):
        for i in reversed(range(9)):
            city = self.infect_cards.draw_card(0)
            self.infect(city, city//CITIES_PER_COLOR, i//3 + 1)

    def draw_infect_card(self):
        card = self.infect_cards.draw_card(0)
        self.infect_cards.add_to_discard(card)
        self.infect(card, card // CITIES_PER_COLOR, 1)
        self.reset_outbreaks()
        return card

    def infect(self, city, color, num_cubes):
        if city not in self.quarantined and self.cures[color] != ERADICATED:
            if self.cubes[city][color] == 0:
                self.board.set_row(city, color)
            if self.cubes[city][color] + num_cubes <= MAX_CUBES:
                self.cubes[city][color] += num_cubes
                self.cubes_left[color] -= num_cubes
            else:
                self.cubes[city][color] = MAX_CUBES
                self.cubes_left[color] -= MAX_CUBES - num_cubes
                self.outbreak(city, color)

    def outbreak(self, city, color):
        if city not in self.outbreaks \
                and city not in self.quarantined \
                and self.cures[color] != ERADICATED:
            self.num_outbreaks += 1
            self.outbreaks.append(city)
            neighbors = self.board.get_neighbors(city)
            for n in neighbors:
                self.infect(n, color, 1)

    def reset_outbreaks(self):
        self.outbreaks = []

    def epidemic(self):
        self.num_epidemics += 1
        card = self.infect_cards.draw_card(-1)
        self.infect_cards.add_to_discard(card)
        self.infect(card, card // CITIES_PER_COLOR, MAX_CUBES)
        self.reset_outbreaks()
        self.infect_cards.recombine_decks()

    def remove_cubes(self, color, number, city):
        game.cubes_left[color] += number;
        game.cubes[city][color] -= number
        if game.cubes[city][color] == 0:
            board.delete_row(city, color)

    # Handles all functions relating to research stations.
    def check_num_stations(self):
        return len(self.research_stations)

    def is_eradicated(self, color):
        eradicated = True
        for city in range(NUM_CITIES):
            if self.cubes[city][color] != 0:
                return False
        return True
# Basic actions
    def move(self, new_pos, index, discard, method):
        player = self.players[self.active]
        mover = self.players[self.selected]
        owner = self.players[(self.active + index) % self.num_players]

        prev_avail, dispatch, origin, player_id = self.set_available(0)
        prev_hand = copy(player.hand)
        prev_take, prev_give, prev_hands = self.set_share()
        prev_build = player.can_build(origin, self.research_stations)
        prev_cure = player.can_cure(self.research_stations)
        orig_cubes = copy(self.cubes[new_pos])
        orig_rows = copy(self.board.rows[new_pos])
        action = { 'act': method,
                    'id': player.get_id(),
                    'is_stored': 0,
                    'origin': origin,
                    'destination': new_pos,
                    'cards': discard,
                    'owner': owner.get_id(),
                    'available': prev_avail,
                    'can_build': prev_build,
                    'can_cure': prev_cure,
                    'cubes': orig_cubes,
                    'rows': orig_rows,
                    'hand': prev_hand,
                    'team_hands': prev_hands,
                    'give': prev_give,
                    'take': prev_take }
        mover.move(new_pos, self.board, self.cures, self.cubes, self.cubes_left, self.quarantined)
        if discard != '':
            owner.discard(discard, self.player_cards)
        if player.get_role() != DISPATCHER:
            self.selected = self.active
        if method == 'station-fly':
            player.has_stationed = True
        return action

    def build(self, to_remove):
        player = self.players[self.active]
        num_stations = len(self.research_stations)
        prev_avail, dispatch, origin, player_id = self.set_available(0)

        can_build = player.get_position() not in self.research_stations and (player.get_position() in player.hand or player.get_role() == OE)
        discard = player.get_position() if player.get_role() != OE else -1

        action = { 'act': "build",
                   'origin': str(player.get_position()),
                   'can_build': can_build,
                   'discard': str(discard),
                   'removed': str(to_remove),
                   'owner': player.get_id(),
                   'card_data': CARDS[discard],
                   'available': prev_avail }
        self.research_stations.append(player.get_position())
        if discard != -1:
            player.discard(discard, self.player_cards)
        return action

    def treat(self, color):
        player = self.players[self.active]
        city = player.get_position()
        orig_cubes = copy(self.cubes[city][color])
        orig_rows = copy(self.board.rows[city])
        player.treat(color, self.cures, self.cubes, self.cubes_left, self.board)
        cubes_removed = orig_cubes - self.cubes[city][color]
        action = { 'act': "treat",
                   'origin': str(city),
                    'color': str(color),
                    'cubes': orig_cubes,
                    'removed': cubes_removed,
                    'rows': orig_rows }
        return action

    def make_cure(self, cards):
        player = self.players[self.active]
        prev_avail, dispatch, origin, player_id = self.set_available(0)
        orig_cubes = game.cubes[player.get_position()][cure_color]
        orig_rows = copy(game.board.get_all_rows(player.get_position()))

        cure_color = cards[0] // CITIES_PER_COLOR
        player.make_cure(cards, self.cures, self.player_cards)
        orig_cubes = game.cubes[player.get_position()][cure_color]
        orig_rows = copy(game.board.get_all_rows(player.get_position()))

        medic_pos = -1
        for p in self.players:
            if p.get_role() == MEDIC:
                self.cubes_left[cure_color] += self.cubes[p.get_position()][cure_color]
                self.cubes[p.get_position()][cure_color] = 0
                self.board.delete_row(p.get_position(), cure_color)
                medic_pos = p.get_position()
                break

        if self.is_eradicated(cure_color):
            self.cures[ cure_color ] = ERADICATED

        action = { 'act': 'cure',
                    'color': cure_color,
                    'cards': [str(card) for card in cure_cards],
                    'origin': str(player.get_position()),
                    'medic_pos': medic_pos,
                    'cubes': orig_cubes,
                    'rows': orig_rows,
                    'available': prev_avail }
        return action

    def give_card(recipient, card):
        giver = self.players[self.active]
        receiver = self.players[(self.recipient + self.active) % self.num_players]
        prev_avail, dispatch, origin, player_id = self.set_available(0)
        giver.give_card(card, reciever)
        action = { 'act': 'give',
                    'card': str(card),
                    'giver': giver.get_id(),
                    'taker': receiver.get_id(),
                    'available': prev_avail }
        return action

    def take_card(giver, card):
        taker = self.players[self.active]
        source = self.players[(self.source + self.active) % self.num_players]
        prev_avail, dispatch, origin, player_id = game.set_available(is_airlift)
        taker.take_card(card, source)
        action = { 'act': 'take',
                    'card': str(card),
                    'taker': player.get_id(),
                    'giver': source.get_id(),
                    'available': prev_avail }
        return action

# Event card handling
    def play_airlift(self, owner_index, new_pos):
        owner = self.players[(self.active + owner_index) % self.num_players]
        mover = self.players[self.selected]
        owner = self.players[(self.active + index) % self.num_players]

        prev_avail, dispatch, origin, player_id = self.set_available(0)
        prev_hand = copy(player.hand)
        prev_take, prev_give, prev_hands = self.set_share()
        prev_build = player.can_build(origin, self.research_stations)
        prev_cure = player.can_cure(self.research_stations)
        orig_cubes = copy(self.cubes[new_pos])
        orig_rows = copy(self.board.rows[new_pos])
        action = { 'act': method,
                    'id': player.get_id(),
                    'is_stored': 1,
                    'origin': origin,
                    'destination': new_pos,
                    'cards': discard,
                    'owner': owner.get_id(),
                    'available': prev_avail,
                    'can_build': prev_build,
                    'can_cure': prev_cure,
                    'cubes': orig_cubes,
                    'rows': orig_rows,
                    'hand': prev_hand,
                    'team_hands': prev_hands,
                    'give': prev_give,
                    'take': prev_take }
        mover.move(new_pos, self.board, self.cures, self.cubes, self.cubes_left, self.quarantined)

        if is_stored == 0:
            owner.discard(AIRLIFT, self.plater_cards)
        else:
            owner.play_event(self.player_cards)
        self.selected = self.active
        return action

    def play_gg(self, city, index, to_remove, is_stored):
        player = self.players[self.active]
        owner = self.players[(self.active + index) % self.num_players]
        can_build = player.get_position() not in self.research_stations and (player.get_position() in player.hand or player.get_role() == OE)

        action = { 'act': "gg",
                   'origin': str(position),
                   'can_build': can_build,
                   'discard': str(GG),
                   'removed': str(to_remove),
                   'owner': owner.get_id(),
                   'card_data': CARDS[GG],
                   'available': prev_avail }
        if is_stored == 0:
            owner.discard(GG, self.player_cards)
        else:
            owner.play_event(self.player_cards)
        self.research_stations(city)
        if to_remove != -1:
            self.research_stations.remove(to_remove)
        return action


    def play_forecast(self, index, reorded, is_stored):
        owner = self.players[(self.active + index) % self.num_players]
        self.infect_cards.set_deck(reorded + self.infect_cards.deck[:6])
        if is_stored == 0:
            owner.discard(FORECAST, self.plater_cards)
        else:
            owner.play_event(self.player_cards)

    def play_rp(card, index, is_stored):
        owner = self.players[(self.active + index) % self.num_players]
        self.infect_cards.remove_from_discard(card)
        self.infect_cards.add_to_graveyard(card)
        if is_stored == 0:
            owner.discard(RP, self.plater_cards)
        else:
            owner.play_event(self.player_cards)

        action = { 'act': 'rp',
                    'owner': owner.get_id(),
                    'store': is_stored,
                    'deleted': card }
        return action

    def play_oqn(index, is_stored):
        owner = self.players[(self.active + index) % self.num_players]
        self.oqn = True
        if is_stored == 0:
            owner.discard(OQN, self.plater_cards)
        else:
            owner.play_event(self.player_cards)

        action = { 'act': 'oqn',
                    'store': is_stored,
                    'owner': owner.get_id() }
        return action

    def store_on_cp(card):
        player = self.players[self.active]
        player.get_event_from_discard(card, self.player_cards)
        action = { 'act': 'store',
                    'card': card }
        return action

## End conditions
    # Win
    def is_win(self):
        for have_cure in self.cures:
            if not have_cure:
                return False
        return True

    # Lose
    def is_cube_lose(self, color, added):
        self.lose = self.cubes_left[color] - added < 0
        return self.lose

    def is_outbreak_lose(self):
        self.lose = self.num_outbreaks >= MAX_OUTBREAKS
        return self.lose

    def is_card_lose(self):
        self.lose = self.player_cards.getSize() < 2
        return self.lose
