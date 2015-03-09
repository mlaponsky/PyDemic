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
    def can_move(self, research_stations, board):
        return self.can_drive(board) + self.can_shuttle(research_stations) + self.can_fly_direct(board) + self.can_charter(research_stations, board)

    def can_drive(self, board):
        return board.get_neighbors(self.position)

    def can_shuttle(self, research_stations):
        shuttle = []
        if self.position in research_stations:
            shuttle = copy(research_stations)
            shuttle.remove(self.position)
        return shuttle

    def can_fly_direct(self, board):
        can_fly = copy(self.hand)
        neighbors = board.get_neighbors(self.position)
        if self.position in can_fly:
            can_fly.remove(self.position)
        for city in neighbors:
            if city in can_fly:
                can_fly.remove(city)
        return can_fly

    def can_charter(self, research_stations, board):
        can_charter = []
        neighbors = board.get_neighbors(self.position)
        if self.position in self.hand:
            can_charter = [ city for city in range(NUM_CITIES) ]
            can_charter.remove(self.position)
            for n in neighbors:
                can_charter.remove(n)
        return can_charter

    def move(self, new_pos, board, cures, cubes, cubes_left, quarantined):
        self.position = new_pos

    # Hand management
    def add_card(self, card):
        self.hand.append(card)
        self.hand.sort()

    def discard(self, card, deck):
        if card in self.hand:
            self.hand.remove(card)
            deck.add_to_discard(card)
            print(deck.discard)

    def has_card(self, card):
        return card in self.hand

    def add_card_from_hand(self, card):
        if self.has_card(card):
            return card
        return ""

    def can_take(self, card, source):
        if target.get_role() == RESEARCHER:
            return ( source.has_card(card) and self.position == source.get_position() )
        return (source.has_card(card) and self.position == source.get_position() and card == self.position)

    def can_give(self, card, target):
        return (self.has_card(card) and self.position == target.get_position() and card == self.position)

    def give_card(self, card, target):
        if card in self.hand:
            self.discard(card)
            target.add_card(card)

    def take_card(self, card, donor):
        if donor.has_card(card):
            donor.discard(card)
            self.add_card(card)

    # Treatment
    def treat(self, color, cures, cubes, cubes_left, board):
        if not cures[color]:
            cubes_left[color] += 1
            cubes[self.position][color] -= 1
        else:
            cubes_left[color] += cubes[self.position][color]
            cubes[self.position][color] = 0
        if cubes[self.position][color] == 0:
            board.delete_row(self.position, color)

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

    def make_cure(self, cards):
        for card in cards:
            self.hand.remove(card)

    # Research Stations
    def can_build(self, city, research_stations):
        return (self.position == city and city in self.hand and city not in research_stations)

    def build_station(self, city, research_stations, deck):
        self.discard(city, deck)
        research_stations.append(city)

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
        self.selected = self

    def select_player(self, selected):
        self.selected = selected

    def can_drive(self, board):
        if self.selected == self:
            return board.get_neighbors(self.position)
        else:
            return board.get_neighbors(self.selected.get_position())

    def can_shuttle(self, research_stations):
        shuttle = []
        if self.selected.get_position() in research_stations:
            shuttle = copy(research_stations)
            shuttle.remove(self.selected.get_position())
        return shuttle

    def can_fly_direct(self, board):
        can_fly = copy(self.hand)
        neighbors = board.get_neighbors(self.selected.get_position())
        if self.selected.get_position() in can_fly:
            can_fly.remove(self.position)
        for city in neighbors:
            if city in can_fly:
                can_fly.remove(city)
        return can_fly

    def can_charter(self, research_stations, board):
        can_charter = []
        if self.selected.get_position() in self.hand:
            can_charter = [ city for city in range(NUM_CITIES) ]
            can_charter.remove(self.selected.get_position())
            for n in board.get_neighbors(self.selected.get_position()):
                can_charter.remove(n)
        return can_charter

    def can_move(self, research_stations, board):
        return self.can_drive(board) + self.can_shuttle(research_stations) + self.can_fly_direct(board) + self.can_charter(research_stations, board)

    def move(self, new_pos, board, cures, cubes, cubes_left, quarantined):
        if self.selected == self:
            self.position = new_pos
        else:
            self.selected.move(new_pos, board, cures, cubes, quarantined)

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

    def move(self, new_pos, board, cures, cubes, cubes_left, quarantined):
        self.position = new_pos
        for color in COLORS:
            if cures[color]:
                cubes_left[color] += cubes[self.position][color]
                cubes[self.position][color] = 0
                board.delete_row(self.position, color)

    def treat(self, color, cures, cubes, cubes_left, board):
        if not cures[color]:
            cubes_left[color] += cubes[self.position][color]
            cubes[self.position][color] = 0
            board.get_row(self.position, color)

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

    def fly_from_station(self, destination, card, research_stations):
        if self.position in research_stations:
            self.discard(card)
            self.position = destination

    def can_charter(self, research_stations, board):
        can_charter = []
        cities_in_hand = False
        for card in self.hand:
            if card in range(NUM_CITIES):
                cities_in_hand = True;
                break;
        if self.position in self.hand or (self.position in research_stations and cities_in_hand):
            can_charter = [ city for city in range(NUM_CITIES) ]
            can_charter.remove(self.position)
            for n in board.get_neighbors(self.position):
                can_charter.remove(n)
        return can_charter

    def can_build(self, city, research_stations):
        return (self.position == city and city not in research_stations)

    def build_station(self, city, research_stations, deck):
        research_stations.append(city)

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

    def can_give(self, card, target):
        return (self.has_card(card) and self.position == target.get_position())

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
