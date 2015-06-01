# -*- coding: utf-8 -*-

from .constants import *
from .deck import *
from copy import copy
from .board import *

class Player:
    def __init__(self, role):
        self.role = role
        self.position = ATL
        self.hand = []
        self.color = ROLES[role]['color']
        self.title = ROLES[role]['title_img']
        self.piece = ROLES[role]['piece_img']

    # Getter functions
    def get_role(self):
        return self.role

    def get_title(self):
        return self.title

    def get_id(self):
        return self.id

    def get_position(self):
        return self.position

    # Movement
    def can_move(self, hand, research_stations, board):
        return self.can_drive(board) + self.can_shuttle(research_stations) + self.can_fly_direct(hand, board) + self.can_charter(hand, board)

    def can_drive(self, board):
        return board.get_neighbors(self.position)

    def can_shuttle(self, research_stations):
        shuttle = []
        if self.position in research_stations:
            shuttle = copy(research_stations)
            shuttle.remove(self.position)
        return shuttle

    def can_fly_direct(self, hand, board):
        can_fly = copy(hand)
        for card in range(48, 53):
            if card in can_fly:
                can_fly.remove(card)
        neighbors = board.get_neighbors(self.position)
        if self.position in can_fly:
            can_fly.remove(self.position)
        for city in neighbors:
            if city in can_fly:
                can_fly.remove(city)
        return can_fly

    def can_charter(self, hand, board):
        can_charter = []
        neighbors = board.get_neighbors(self.position)
        if self.position in hand:
            can_charter = [ city for city in range(NUM_CITIES) ]
            can_charter.remove(self.position)
            for n in neighbors:
                if n in can_charter:
                    can_charter.remove(n)
        return can_charter

    def move(self, new_pos, board, cures, cubes, cubes_left, quarantined):
        self.position = new_pos

    # Hand management
    def add_card(self, card):
        self.hand.append(card)

    def discard(self, card, deck):
        if card in self.hand:
            self.hand.remove(card)
            deck.add_to_discard(card)

    def has_card(self, card):
        return card in self.hand

    def add_card_from_hand(self, card):
        if self.has_card(card):
            return card
        return ""

    def can_take(self, card, source):
        if source.get_role() == RESEARCHER:
            return ( source.has_card(card) and self.position == source.get_position() and card//CITIES_PER_COLOR != EVENT)
        return (source.has_card(card) and self.position == source.get_position() and card == self.position and card//CITIES_PER_COLOR != EVENT)

    def can_give(self, card, target):
        return (self.has_card(card) and self.position == target.get_position() and card == self.position and card//CITIES_PER_COLOR != EVENT and self.role != target.get_role())

    def give_card(self, card, target):
        if card in self.hand:
            self.hand.remove(card)
            target.add_card(card)

    def take_card(self, card, donor):
        if donor.has_card(card):
            donor.hand.remove(card)
            self.add_card(card)

    # Treatment
    def treat(self, color, cures, cubes, cubes_left, board):
        if not cures[color]:
            cubes_left[color] += 1
            cubes[self.position][color] -= 1
        else:
            cubes_left[color] += cubes[self.position][color]
            cubes[self.position][color] = 0
        if all(cubes[self.position][color] == 0 for color in COLORS):
            board.delete_rows(self.position)

    # Cure
    def can_cure(self, research_stations):
        if self.position not in research_stations:
            return False
        else:
            needed = 5
            count = 0
            hand_colors = [ card // CITIES_PER_COLOR for card in self.hand ]
            for color in COLORS:
                if hand_colors.count(color) > count:
                    count = hand_colors.count(color)
            return count >= needed

    def get_cure_cards(self):
        needed = 5 if self.role != SCIENTIST else 4
        cure_color = -1
        hand_colors = [ card // CITIES_PER_COLOR for card in self.hand ]
        for color in COLORS:
            if hand_colors.count(color) >= needed:
                cure_color = color
        cards = [ card for card in self.hand if card // CITIES_PER_COLOR == cure_color ]
        return cards

    def make_cure(self, cards, cures, cubes, cubes_left, deck, board):
        cure_color = cards[0] // CITIES_PER_COLOR
        for card in cards:
            self.discard(card, deck)
        cures[cure_color] = CURED


    # Research Stations
    def can_build(self, city, research_stations):
        return (self.position == city and city in self.hand and city not in research_stations)

    def build_station(self, city, discard, research_stations, deck):
        if discard != -1 and discard in self.hand:
            self.discard(discard, deck)
        research_stations.append(city)

    def select(self, selected):
        self.selected = selected
        if self.selected.get_role() == OE:
            self.selected.has_stationed = True

# Role subclasses; contain special implementations of actions
class ContingencyPlanner(Player):
    def __init__(self):
        role = CP
        self.role = role
        self.id = 'cp'
        self.event = None
        self.position = ATL
        self.hand = []
        self.color = ROLES[role]['color']
        self.title = ROLES[role]['title_img']
        self.piece = ROLES[role]['piece_img']
        self.selected = self

    def can_get_event(self):
        return self.event == None

    def get_event_from_discard(self, card, deck):
        if card in deck.get_discard() and self.can_get_event():
            deck.remove_from_discard(card)
            self.event = card

    def play_event(self, deck):
        card = self.event
        self.event = None
        deck.add_to_graveyard(card)

    def build_station(self, city, discard, research_stations, deck):
        if discard != -1 and discard in self.hand:
            self.discard(discard, deck)
        else:
            self.play_event(deck)
        research_stations.append(city)

class Dispatcher(Player):
    def __init__(self):
        super(Player, self).__init__()
        role = DISPATCHER
        self.role = role
        self.id = 'dispatcher'
        self.position = ATL
        self.hand = []
        self.color = ROLES[role]['color']
        self.title = ROLES[role]['title_img']
        self.piece = ROLES[role]['piece_img']

    # def can_drive(self, selected_id, board):
    #     if self.selected == self:
    #         return board.get_neighbors(self.position)
    #     else:
    #         return board.get_neighbors(self.selected.get_position())
    #
    # def can_shuttle(self, research_stations):
    #     shuttle = []
    #     if self.selected.get_position() in research_stations:
    #         shuttle = copy(research_stations)
    #         shuttle.remove(self.selected.get_position())
    #     return shuttle
    #
    # def can_fly_direct(self, board):
    #     can_fly = copy(self.hand)
    #     neighbors = board.get_neighbors(self.selected.get_position())
    #     if self.selected.get_position() in can_fly:
    #         can_fly.remove(self.selected.position)
    #     for city in neighbors:
    #         if city in can_fly:
    #             can_fly.remove(city)
    #     return can_fly
    #
    # def can_charter(self, research_stations, board):
    #     can_charter = []
    #     if self.selected.get_position() in self.hand:
    #         can_charter = [ city for city in range(NUM_CITIES) ]
    #         can_charter.remove(self.selected.get_position())
    #         for n in board.get_neighbors(self.selected.get_position()):
    #             if n in can_charter:
    #                 can_charter.remove(n)
    #     return can_charter

class Medic(Player):
    def __init__(self):
        role = MEDIC
        self.role = role
        self.id = 'medic'
        self.position = ATL
        self.hand = []
        self.color = ROLES[role]['color']
        self.title = ROLES[role]['title_img']
        self.piece = ROLES[role]['piece_img']
        self.selected = self

    def move(self, new_pos, board, cures, cubes, cubes_left, quarantined):
        if self.selected == self:
            self.position = new_pos
            for color in COLORS:
                if cures[color] > LIVE:
                    cubes_left[color] += cubes[self.position][color]
                    cubes[self.position][color] = 0
                    if all(cubes[self.position][c] == 0 for c in COLORS):
                        board.delete_rows(self.position)
        else:
            self.selected.move(new_pos, board, cures, cubes, cubes_left, quarantined)

    def treat(self, color, cures, cubes, cubes_left, board):
        cubes_left[color] += cubes[self.position][color]
        cubes[self.position][color] = 0
        if all(cubes[self.position][color] == 0 for color in COLORS):
            board.delete_rows(self.position)

    def make_cure(self, cards, cures, cubes, cubes_left, deck, board):
        cure_color = cards[0] // CITIES_PER_COLOR
        for card in cards:
            self.discard(card, deck)
        cures[cure_color] = CURED
        cubes_left[cure_color] += cubes[self.position][cure_color]
        cubes[self.position][cure_color] = 0
        if all(cubes[self.position][c] == 0 for c in COLORS):
            board.delete_rows(self.position)

class OperationsExpert(Player):
    def __init__(self):
        role = OE
        self.role = role
        self.id = 'oe'
        self.position = ATL
        self.hand = []
        self.color = ROLES[role]['color']
        self.title = ROLES[role]['title_img']
        self.piece = ROLES[role]['piece_img']
        self.selected = self
        self.has_stationed = False

    def fly_from_station(self, destination, card, research_stations):
        if self.position in research_stations:
            self.discard(card)
            self.position = destination
            self.has_stationed = True

    def can_station_fly(self, research_stations, board):
        can_station = []
        cities_in_hand = False

        for card in self.hand:
            if card in range(NUM_CITIES):
                cities_in_hand = True;
                break;

        if self.position in research_stations and not self.has_stationed:
            can_station = [ city for city in range(NUM_CITIES) ]
            can_station.remove(self.position)
            for n in board.get_neighbors(self.position):
                if n in can_station:
                    can_station.remove(n)
        return can_station

    def can_move(self, hand, research_stations, board):
        available = self.can_drive(board) + self.can_shuttle(research_stations) + self.can_fly_direct(hand, board) + self.can_charter(hand, board)
        if not self.has_stationed:
            return available + self.can_station_fly(research_stations, board)
        return available

    def can_build(self, city, research_stations):
        return (self.position == city and city not in research_stations)

    def build_station(self, city, discard, research_stations, deck):
        research_stations.append(city)
        if discard == GG:
            self.discard(discard, deck)

class QuarantineSpecialist(Player):
    def __init__(self, quarantined, neighbors):
        role = QS
        self.role = role
        self.id = 'qs'
        self.position = ATL
        self.hand = []
        self.color = ROLES[role]['color']
        self.title = ROLES[role]['title_img']
        self.piece = ROLES[role]['piece_img']
        self.selected = self
        for city in neighbors:
            quarantined.append(city)
        quarantined.append(self.position)

    def move(self, new_pos, board, cures, cubes, cubes_left, quarantined):
        self.position = new_pos
        del quarantined[:]
        for city in board.get_neighbors(self.position):
            quarantined.append(city)
        quarantined.append(new_pos)

class Researcher(Player):
    def __init__(self):
        super(Player, self).__init__()
        role = RESEARCHER
        self.role = role
        self.id = 'researcher'
        self.position = ATL
        self.hand = []
        self.color = ROLES[role]['color']
        self.title = ROLES[role]['title_img']
        self.piece = ROLES[role]['piece_img']
        self.selected = self

    def can_give(self, card, target):
        return (self.has_card(card) and self.position == target.get_position() and self.role != target.get_role())

class Scientist(Player):
    def __init__(self):
        super(Player, self).__init__()
        role = SCIENTIST
        self.role = role
        self.id = 'scientist'
        self.position = ATL
        self.hand = []
        self.color = ROLES[role]['color']
        self.title = ROLES[role]['title_img']
        self.piece = ROLES[role]['piece_img']
        self.selected = self

    def can_cure(self, research_stations):
        needed = 4
        count = 0
        if self.position not in research_stations:
            return False
        hand_colors = [ card // CITIES_PER_COLOR for card in self.hand ]
        for color in COLORS:
            if hand_colors.count(color) > count:
                count = hand_colors.count(color)
        return count >= needed
