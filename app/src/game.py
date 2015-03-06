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
        self.cures = [1] * 4
        self.research_stations = []
        self.quarantined = []

        self.board = Board()
        self.num_epidemics = epidemics
        self.num_players = len(roles)
        self.research_stations.append(ATL)
        self.infect_cards = InfectCards()
        for i in reversed(range(9)):
            city = self.draw_infect_card()
            self.infect(city, city//CITIES_PER_COLOR, i//3 + 1)

        for role in roles:
            self.players.append(self.assign_player(role))

        self.player_cards = PlayerCards(self.players, self.num_epidemics)
        self.active = self.set_order()

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

    ## The procedures for adding cubes.
    '''
    The below function is a generic cube adding function. It takes the color and number of cubes to be added, and the city to infect. This function is implemented in all situations in which a city would be infected. A normal infect city action will just call the function directly with numCubes = 1. The other cube-adding scenarios are outbreak and epidemic. Notice the recursive coupling between infect and outbreak below, and infect will call outbreak when it would go over the cube limit, and outbreaks will infect, potentially chaining into other outbreaks. The outbreak function handles all conditions for outbreaks, and tracks outbreaks that have already occurred on a turn so as not to repeat. The function to reset the outbreak array is called after each epidemic AND each infect stage.
    '''
    def draw_infect_card(self):
        card = self.infect_cards.draw_card(0)
        self.infect_cards.add_to_discard(card)
        return card

    def infect(self, city, color, num_cubes):
        if city not in self.quarantined or not self.eradicated[color]:
            if self.cubes[city][color] == 0:
                self.board.set_row(city, color)
            if self.cubes[city][color] + num_cubes <= MAX_CUBES:
                self.cubes[city][color] += num_cubes
                self.cubes_left[color] -= num_cubes
            else:
                self.cubes[city][color] = MAX_CUBES
                self.cubes_left[color] -= MAX_CUBES - num_cubes
                self.outbreak(city, color)

    def execute_outbreak(self, city, color, outbreaks):
        if city not in outbreaks \
                or city not in self.quarantined \
                or not self.eradicated[color]:
            self.num_outbreaks += 1
            outbreaks.append(city)
            neighbors = self.board.get_neighbors(city)
            for n in neighbors:
                self.infect(n, color, 1)

    def outbreak(self, city, color):
        outbreaks = []
        self.execute_outbreak(city, color, outbreaks)
        self.reset_outbreaks(outbreaks)

    def reset_outbreaks(self, outbreaks):
        outbreaks = []

    def epidemic(self):
        self.num_epidemics += 1
        card = self.infect_cards.draw_card(-1)
        self.infect_cards.add_to_discard(card)
        self.infect(card, card // CITIES_PER_COLOR, MAX_CUBES)
        self.infect_cards.recombine_decks()

    # Handles all functions relating to research stations.
    def check_num_stations(self):
        return len(self.research_stations)

    def remove_station(self, city):
        self.research_stations.remove(city)

    # Handles OE special ability.

    # Handles RESEARCHER ability in trade check.
    def can_share(self, city, owner, target):
        same_city = owner.get_position() == target.get_position()
        right_city = (city == owner.get_position()
                                or owner.get_role() == RESEARCHER)
        return same_city and right_city

    def share(self, city, owner, target):
        if self.can_share(city, owner, target):
            owner.discard(city)
            target.get_card(city)

    def can_move(self, player, city):
        if player.get_position() in self.research_stations and city in self.research_stations:
            return True
        else:
            return city in self.board.get_neighbors(player.getPosition())

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
