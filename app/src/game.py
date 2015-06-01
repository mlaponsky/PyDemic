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
        self.turns = 0
        self.phase = ACTION_0
        self.id = str(uuid4())

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
        self.infected = {}
        self.at_risk = []

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

    def get_infect_number(self):
        if self.oqn:
            return 0
        if self.drawn_epidemics == 0:
            return 2
        return ( (self.drawn_epidemics-1) // 2 ) + 2

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
        self.selected = index
        selected = self.players[self.selected]
        if selected.get_role() == OE:
            selected.has_stationed = True
        return selected

    def dispatcher_availability(self, available):
        dispatch = []
        selected = self.players[self.selected]
        for p in self.players:
            if selected != p and selected.get_position() != p.get_position():
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
                if city != selected.get_position():
                    available.append(str(city))
        else:
            if player.get_id() == 'dispatcher':
                dispatch = self.dispatcher_availability(available)
            for city in selected.can_move(player.hand, self.research_stations, self.board):
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

    ## The procedures for adding cubes.     '''     The below function is a generic cube adding
## function. It takes the color and number of cubes to be added, and the city to infect. This
## function is implemented in all situations in which a city would be infected. A normal infect city
## action will just call the function directly with numCubes = 1. The other cube-adding scenarios
## are outbreak and epidemic. Notice the recursive coupling between infect and outbreak below, and
## infect will call outbreak when it would go over the cube limit, and outbreaks will infect,
## potentially chaining into other outbreaks. The outbreak function handles all conditions for
## outbreaks, and tracks outbreaks that have already occurred on a turn so as not to repeat. The
## function to reset the outbreak array is called after each epidemic AND each infect stage.     '''
    def initial_infect(self):
        for i in reversed(range(9)):
            self.draw_infect_card(i//3 + 1)

    def draw_infect_card(self, number):
        card = self.infect_cards.draw_card(0)
        self.execute_infect(card, card // CITIES_PER_COLOR, number)
        if card in self.at_risk:
            self.at_risk.remove(card)
        return card

    def execute_infect(self, city, color, num_cubes):
        self.reset_outbreaks()
        self.infect(city, color, num_cubes)
        print(self.outbreaks)

    def infect(self, city, color, num_cubes):
        if city not in self.quarantined and self.cures[color] != ERADICATED:
            if self.cubes[city][color] == 0:
                self.board.set_row(city, color)
            if self.cubes[city][color] + num_cubes <= MAX_CUBES:
                self.cubes[city][color] += num_cubes
                self.cubes_left[color] -= num_cubes
                if city in self.infected:
                    self.infected[city][color] += num_cubes
                else:
                    self.infected[city] = [0]*4
                    self.infected[city][color] = num_cubes
                risk = self.risk(city)
            else:
                self.cubes_left[color] -= MAX_CUBES - self.cubes[city][color]
                if city in self.infected:
                    self.infected[city][color] += MAX_CUBES - self.cubes[city][color]
                else:
                    self.infected[city] = [0]*4
                    self.infected[city][color] = MAX_CUBES - self.cubes[city][color]
                self.cubes[city][color] = MAX_CUBES
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

    def reset_infection(self):
        self.infected = {}

    def epidemic(self):
        self.reset_outbreaks()
        self.reset_infection()
        self.drawn_epidemics += 1
        card = self.infect_cards.draw_card(-1)
        self.execute_infect(card, card // CITIES_PER_COLOR, MAX_CUBES)
        if not self.has_rp():
            self.infect_cards.recombine()
            for city in range(NUM_CITIES):
                risk = self.risk(city)
        return card

    def finish_epidemic(self):
        self.infect_cards.recombine()
        for city in range(NUM_CITIES):
            risk = self.risk(city)

    def has_rp(self):
        has_rp = False
        for p in self.players:
            if RP in p.hand or (p.get_role() == CP and p.event == RP):
                return True
        return has_rp

    def remove_cubes(self, color, number, city):
        game.cubes_left[color] += number;
        game.cubes[city][color] -= number
        if game.cubes[city][color] == 0:
            board.delete_row(city, color)

    def risk(self, city):
        at_risk = False
        for c in COLORS:
            if self.cubes[city][c] == MAX_CUBES and city in self.infect_cards.deck:
                at_risk = True
        if not at_risk and city in self.at_risk:
            self.at_risk.remove(city)
        elif at_risk and city not in self.at_risk:
            self.at_risk.append(city)
        return at_risk

    # Handles all functions relating to research stations.
    def check_num_stations(self):
        return len(self.research_stations)

    def is_eradicated(self, color):
        return self.cubes_left[color] == NUM_CUBES and self.cures[color] == 1

    def next_turn(self):
        if self.phase == DRAW or self.phase == EP:
            self.oqn = False
        self.phase = ACTION_0
        self.active = (self.active+1) % self.num_players
        self.selected = self.active
        if self.players[self.active].get_role() == OE:
            self.players[self.active].has_stationed = False
        self.turns += 1

# Basic actions
    def move(self, new_pos, index, discard, method):
        player = self.players[self.active]
        mover = self.players[self.selected]
        owner = self.players[index]

        true_selected = self.selected
        self.selected = self.active
        prev_avail, dispatch, origin, player_id = self.set_available(0)
        prev_hand = copy(player.hand)
        prev_take, prev_give, prev_hands = self.set_share()
        prev_build = player.can_build(origin, self.research_stations)
        prev_cure = player.can_cure(self.research_stations)
        orig_cubes = copy(self.cubes[new_pos])
        orig_rows = copy(self.board.rows[new_pos])
        at_risk = copy(self.at_risk)
        self.selected = true_selected
        action = { 'act': method,
                    'id': player.get_id(),
                    'owner': owner.get_id(),
                    'mover': mover.get_id(),
                    'is_stored': 0,
                    'origin': mover.get_position(),
                    'destination': new_pos,
                    'cards': discard,
                    'owner': owner.get_id(),
                    'available': prev_avail,
                    'can_build': prev_build,
                    'can_cure': prev_cure,
                    'cubes': orig_cubes,
                    'rows': orig_rows,
                    'at_risk': self.at_risk,
                    'hand': prev_hand,
                    'team_hands': prev_hands,
                    'give': prev_give,
                    'take': prev_take,
                    'at_risk': at_risk }
        mover.move(new_pos, self.board, self.cures, self.cubes, self.cubes_left, self.quarantined)
        for c in COLORS:
            if self.is_eradicated(c):
                self.cures[c] = ERADICATED
        self.risk(new_pos)
        self.phase += 1
        if discard != '':
            owner.discard(int(discard), self.player_cards)
        self.selected = self.active
        if method == 'station-fly':
            player.has_stationed = True
        return action

    def build(self, to_remove):
        player = self.players[self.active]
        num_stations = len(self.research_stations)
        prev_avail, dispatch, origin, player_id = self.set_available(0)

        can_build = player.get_position() not in self.research_stations and (player.get_position() in
player.hand or player.get_role() == OE)
        discard = player.get_position() if player.get_role() != OE else -1

        action = { 'act': "build",
                   'origin': str(player.get_position()),
                   'can_build': can_build,
                   'cards': discard,
                   'removed': str(to_remove),
                   'owner': player.get_id(),
                   'card_data': CARDS[discard],
                   'available': prev_avail }
        self.research_stations.append(player.get_position())
        if to_remove != -1:
            self.research_stations.remove(to_remove)
        self.phase += 1
        if discard != -1:
            player.discard(discard, self.player_cards)
        return action

    def treat(self, color):
        player = self.players[self.active]
        city = player.get_position()
        orig_cubes = copy(self.cubes[city][color])
        orig_rows = copy(self.board.rows[city])
        at_risk = copy(self.at_risk)
        player.treat(color, self.cures, self.cubes, self.cubes_left, self.board)
        self.phase += 1
        cubes_removed = orig_cubes - self.cubes[city][color]
        self.risk(city)
        if self.is_eradicated(color):
            self.cures[color] = ERADICATED
        action = { 'act': "treat",
                   'origin': str(city),
                    'color': str(color),
                    'cubes': orig_cubes,
                    'removed': cubes_removed,
                    'rows': orig_rows,
                    'at_risk': at_risk }
        return action

    def make_cure(self, cards):
        player = self.players[self.active]
        cure_color = cards[0] // CITIES_PER_COLOR
        prev_avail, dispatch, origin, player_id = self.set_available(0)
        orig_cubes = self.cubes[player.get_position()][cure_color]
        orig_rows = copy(self.board.get_all_rows(player.get_position()))
        at_risk = copy(self.at_risk)

        player.make_cure(cards, self.cures, self.cubes, self.cubes_left, self.player_cards, self.board)
        medic_pos = -1
        for p in self.players:
            if p.get_role() == MEDIC:
                medic_pos = p.get_position()
                self.cubes_left[cure_color] += self.cubes[medic_pos][cure_color]
                self.cubes[medic_pos][cure_color] = 0
                self.risk(medic_pos)
                break
        if self.is_eradicated(cure_color):
            self.cures[cure_color] = ERADICATED
        self.phase += 1

        action = { 'act': 'cure',
                    'id': player.get_id(),
                    'color': cure_color,
                    'cards': [str(card) for card in cards],
                    'origin': str(player.get_position()),
                    'medic_pos': medic_pos,
                    'cubes': orig_cubes,
                    'rows': orig_rows,
                    'available': prev_avail,
                    'at_risk': at_risk }
        return action

    def give_card(self, recipient, card):
        giver = self.players[self.active]
        receiver = self.players[recipient]
        prev_avail, dispatch, origin, player_id = self.set_available(0)
        giver.give_card(card, receiver)
        self.phase += 1
        action = { 'act': 'give',
                    'card': str(card),
                    'giver': giver.get_id(),
                    'taker': receiver.get_id(),
                    'available': prev_avail }
        return action

    def take_card(self, giver, card):
        taker = self.players[self.active]
        source = self.players[giver]
        prev_avail, dispatch, origin, player_id = self.set_available(0)
        taker.take_card(card, source)
        self.phase += 1
        action = { 'act': 'take',
                    'card': str(card),
                    'taker': taker.get_id(),
                    'giver': source.get_id(),
                    'available': prev_avail }
        return action

# Event card handling
    def play_airlift(self, owner_index, new_pos):
        player = self.players[self.active]
        owner = self.players[owner_index]
        mover = self.players[self.selected]

        prev_avail, dispatch, origin, player_id = self.set_available(0)
        prev_hand = copy(player.hand)
        prev_take, prev_give, prev_hands = self.set_share()
        prev_build = player.can_build(origin, self.research_stations)
        prev_cure = player.can_cure(self.research_stations)
        orig_cubes = copy(self.cubes[new_pos])
        orig_rows = copy(self.board.rows[new_pos])
        at_risk = copy(self.at_risk)
        is_stored = AIRLIFT not in owner.hand
        action = { 'act': 'airlift',
                    'id': player.get_id(),
                    'owner': owner.get_id(),
                    'mover': mover.get_id(),
                    'is_stored': is_stored,
                    'origin': origin,
                    'destination': new_pos,
                    'cards': AIRLIFT,
                    'available': prev_avail,
                    'can_build': prev_build,
                    'can_cure': prev_cure,
                    'cubes': orig_cubes,
                    'rows': orig_rows,
                    'hand': prev_hand,
                    'team_hands': prev_hands,
                    'give': prev_give,
                    'take': prev_take,
                    'at_risk': at_risk }
        mover.move(new_pos, self.board, self.cures, self.cubes, self.cubes_left, self.quarantined)
        for c in COLORS:
            if self.is_eradicated(c):
                self.cures[c] = ERADICATED
        if not is_stored:
            owner.discard(AIRLIFT, self.player_cards)
        else:
            owner.play_event(self.player_cards)
        self.selected = self.active
        return action

    def play_gg(self, city, index, to_remove):
        player = self.players[self.active]
        owner = self.players[index]
        can_build = player.get_position() not in self.research_stations and (player.get_position() in player.hand or player.get_role() == OE)
        prev_avail, dispatch, origin, player_id = self.set_available(0)
        is_stored = GG not in owner.hand
        action = { 'act': "gg",
                   'origin': str(city),
                   'can_build': can_build,
                   'cards': str(GG),
                   'removed': str(to_remove),
                   'owner': owner.get_id(),
                   'card_data': CARDS[GG],
                   'available': prev_avail,
                   'is_stored': is_stored}
        if not is_stored:
            owner.discard(GG, self.player_cards)
        else:
            owner.play_event(self.player_cards)
        self.research_stations.append(city)
        if to_remove != -1:
            self.research_stations.remove(to_remove)
        return action


    def play_forecast(self, index, reordered):
        owner = self.players[index]
        self.infect_cards.deck = reordered + self.infect_cards.deck[6:]
        is_stored = FORECAST not in owner.hand
        if not is_stored:
            owner.discard(FORECAST, self.player_cards)
        else:
            owner.play_event(self.player_cards)
        return owner

    def play_rp(self, card, index):
        owner = self.players[index]
        self.infect_cards.remove_from_discard(card)
        self.infect_cards.add_to_graveyard(card)
        is_stored = RP not in owner.hand
        if not is_stored:
            owner.discard(RP, self.player_cards)
        else:
            owner.play_event(self.player_cards)

        action = { 'act': 'rp',
                    'owner': owner.get_id(),
                    'is_stored': is_stored,
                    'deleted': card }
        return action

    def play_oqn(self, index):
        owner = self.players[index]
        self.oqn = True
        is_stored = OQN not in owner.hand
        if not is_stored:
            owner.discard(OQN, self.player_cards)
        else:
            owner.play_event(self.player_cards)

        action = { 'act': 'oqn',
                    'is_stored': is_stored,
                    'owner': owner.get_id() }
        return action

    def store_on_cp(self, card):
        player = self.players[self.active]
        player.get_event_from_discard(card, self.player_cards)
        self.phase += 1
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
