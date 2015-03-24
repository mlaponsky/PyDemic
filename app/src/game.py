# -*- coding: utf-8 -*-

from .player import *
from .board import Board
from .deck import Deck, PlayerCards, InfectCards
from .constants import *
from random import shuffle

class Game:
    def __init__(self, roles, epidemics):
        self.lose = False
        self.phase = 0
        self.active_player = None

        self.num_outbreaks = 0
        self.num_epidemics = 0
        self.drawn_epidemics = 0

        self.num_players = 0
        self.players = []

        self.from_discard = []

        # cubes[city][color]
        self.cubes = { }
        for city in range(NUM_CITIES):
             self.cubes[city] = [0] * 4
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

        for role in roles:
            self.players.append(self.assign_player(role))

        self.player_cards = PlayerCards(self.players, self.num_epidemics)
        self.active = self.set_order()

        self.players[self.active].hand.append(ATL)

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

    def dispatcher_availability(self, player, available):
        dispatch = []
        for p in self.players:
            if player.selected != p and player.selected.get_position() != p.get_position():
                available.append(str(p.get_position()))
                dispatch.append(p.get_position())
        return dispatch

    def set_available(self, player):
        dispatch = []
        available = []
        player_id = player.get_id()
        if player_id == 'dispatcher':
            player_id = player.selected.get_id()
            origin = player.selected.get_position()
            dispatch = self.dispatcher_availability(player, available)
        else:
            player_id = player.get_id()
            origin = player.get_position()

        for city in player.can_move(self.research_stations, self.board):
            available.append(str(city))

        return available, dispatch, origin, player_id

    def set_share(self):
        can_give = {}
        can_take = {}
        player = self.players[self.active]
        team = self.players[self.active:] + self.players[:self.active]
        team_hands = []
        for p in team[1:]:
            can_take[p.get_id()] = []
            can_give[p.get_id()] = []
            team_hands.append(p.hand)
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

# Event card handling
    def play_airlift(self, player, target, new_pos):
        player.discard(AIRLIFT)
        self.player_cards.add_to_discard(AIRLIFT)
        target.move(new_pos)
        if target.get_role() == QS:
            self.quarantine_cities(target)

    def play_gov_grant(self, player, loc):
        self.research_stations.append(loc)
        player.discard(GG)

    def resolve_forecast(self, reorded):
        self.infect_cards.set_deck(self.infect_cards.get_deck()[:6])
        self.infect_cards.set_deck(reorded + self.infect_cards.get_deck())
        player.discard(FORECAST)

## End conditions
    # Win
    def isWin(self):
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
