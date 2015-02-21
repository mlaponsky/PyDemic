# -*- coding: utf-8 -*-

from player import Player
from board import Board
from deck import Deck, PlayerCards, InfectCards
from constants import *
from random import shuffle

class Game:
    phase = 0

    num_outbreaks = 0
    num_epidemics = 0
    drawn_epidemics = 0

    num_players = 0
    players = []

    from_discard = []

    research_stations = []
    cubes_left = [NUM_CUBES] * 4
    cures = [False] * 4
    eradicated = [False] * 4
    quarantined = []

    def __init__(self, roles, epidemics):
        self.board = Board()
        self.num_epidemics = epidemics
        self.num_players = len(roles)
        self.research_stations.append(ATL)

        for i in range(self.num_players):
            self.players.append(Player(roles[i]))

        self.player_cards = PlayerCards(self.players, self.num_epidemics)
        self.infect_cards = InfectCards()

        # cubes[city][color]
        self.cubes = [ [0] * 4 for x in range(NUM_CITIES) ]

        # outbreaks[color][cities]
        self.outbreaks = []

    ## Manage game phase
    def get_phase(self):
        return self.phase

    def set_phase(self, phase):
        self.phase = phase

    ## The procedures for adding cubes.
    '''
    The below function is a generic cube adding function. It takes the color and number of cubes to be added, and the city to infect. This function is implemented in all situations in which a city would be infected. A normal infect city action will just call the function directly with numCubes = 1. The other cube-adding scenarios are outbreak and epidemic. Notice the recursive coupling between infect and outbreak below, and infect will call outbreak when it would go over the cube limit, and outbreaks will infect, potentially chaining into other outbreaks. The outbreak function handles all conditions for outbreaks, and tracks outbreaks that have already occurred on a turn so as not to repeat. The function to reset the outbreak array is called after each epidemic AND each infect stage.
    '''
    def draw_infect_card(self):
        card = self.infect_cards.draw_dard(0)
        self.infect_cards.add_to_discard(card)
        return card

    def infect(self, city, color, num_cubes):
        if city not in self.quarantined or not self.eradicated[color]:
            if self.cubes[city][color] + num_cubes <= MAX_CUBES:
                self.cubes[city][color] += num_cubes
                self.cubes_left[color] -= num_cubes
            else:
                self.cubes[city][color] = MAX_CUBES
                self.cubes_left[color] -= MAX_CUBES - num_cubes
                self.outbreak(city, color)

    def outbreak(self, city, color):
        self.execute_outbreak(city, color):
        self.reset_outbreaks()

    def execute_outbreak(self, city, color):
        if city not in self.outbreaks[color] or
                or city not in self.quarantined
                or city not self.eradicated[color]:
            self.num_outbreaks += 1
            self.outbreaks[color].append(city)
            neighbors = self.board.get_neighbors(city)
            for n in neighbors:
                self.infect(n, color, 1)

    def resetOutbreaks(self):
        self.outbreaks = []

    def epidemic(self):
        self.num_epidemics += 1
        card = self.infect_cards.draw_card(-1)
        print(card)
        self.infect_cards.add_to_discard(card)
        self.infect(card, card // CITIES_PER_COLOR, MAX_CUBES)
        self.infect_cards.recombine_decks()

## Special Role handlers
    # This function automates the Jesus ability for the medic with a cure.
    # This will be paired with any movement by the medic.
    def medic_with_cure(self, player):
        city = player.get_position()
        for color in range(len(self.cures)):
            if self.cures[color]:
                self.cubes_left[color] += self.cubes[city][color]
                self.cubes[city][color] = 0

    # Handles quarantine of cities. Called at the end of every turn, or when an AIRLIFT is played.
    def quarantine_cities(self, player):
        self.quarantined = []
        city = player.get_position()
        self.quarantined.append(city)
        for n in self.board.get_neighbors(city):
            self.quarantined.append(n)

    # Handles the special action of the CP.
    def contingency(self, player, card):
        self.player_deck.remove_from_discard[card]
        player.get_card(card)
        self.from_discard.append[card]

    # Called every time the CP plays an Event card
    def play_contingency_event(self, player, card):
        player.discard(card)
        if card in self.from_discard:
            self.player_cards.add_to_graveyard(card)
        else:
            self.player_cards.add_to_discard(card)

    # The general function for removing cubes. Accounts for the medic case.
    def remove_cubes(self, city, player, color):
        if player == MEDIC:
            self.cubes_left[color] += self.cubes[city][color]
            self.cubes[city][color] = 0
        else:
            if not self.cures[color]:
                self.cubes_left[color] += 1
                self.cubes[city][color] -= 1
            else:
                self.cubes_left[color] += self.cubes[city][color]
                self.cubes[city][color] = 0
        self.actions[player] -= 1

    # Handles all functions relating to research stations.
    def check_num_stations(self):
        return len(self.research_stations)

    def remove_station(self, city):
        self.research_stations.remove(city)

    # Handles OE special ability.
    def build_station(self, city, player):
        if player.get_role() != OE:
            player.discard(city)
        if player.get_position() == city:
            self.research_stations.append(city)

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
        return self.cubes_left[color] - added < 0

    def is_outbreak_lose(self):
        return self.num_outbreaks >= MAX_OUTBREAKS

    def is_card_lose(self):
        return self.player_cards.getSize() < 2
