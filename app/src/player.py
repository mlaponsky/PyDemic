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

    def get_role(self):
        return self.role

    def get_title(self):
        return self.title

    def get_id(self):
        return self.id

    def get_position(self):
        return self.position

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

    def move(self, new_pos, board, cures, cubes, quarantined):
        self.position = new_pos

    def get_card(self, card):
        self.hand.append(card)
        self.hand.sort()

    def discard(self, card):
        if card in self.hand:
            self.hand.remove(card)

    def treat(self, color, cures, cubes):
        if not cures[color]:
            cubes[self.position][color] -= 1
        else:
            cubes[self.position][color] = 0

    def can_cure(self, color, research_stations):
        if self.position not in research_stations:
            return False
        else:
            needed = 5
            count = 0
            for card in self.hand:
                count += card // CITIES_PER_COLOR == color
            return count >= needed

    def make_cure(self, cards):
        for card in cards:
            self.hand.remove(card)

    def has_card(self, card):
        return card in self.hand

    def get_card_from_hand(self, card):
        if self.hasCard(card):
            return card
        return ""

    def build_station(self, city, research_stations):
        if self.position == city \
          and len(research_stations) < MAX_STATIONS \
          and city in self.hand:
                self.discard(card)
                research_stations.append(city)

    def can_share(self, card, target):
        return (card in self.hand or card in target.hand) and self.position == target.get_position() and card == self.position

    def give_card(self, card, target):
        if card in self.hand:
            self.discard(card)
            target.get_card(card)

    def take_card(self, card, donor):
        if donor.has_card(card):
            donor.discard(card)
            self.get_card(card)

# Role subclasses; contain special implementations of actions
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

    def move(self, new_pos, board, cures, cubes, quarantined):
        self.position = new_pos
        for color in COLORS:
            if cures[color]:
                cubes[self.position // 12][color] = 0

    def treat(self, cures, cubes):
        if not cures[color]:
            cubes[self.position][color] = 0

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

    def move(self, new_pos, board, cures, cubes, quarantined):
        self.position = new_pos
        del quarantined[:]
        for city in board.get_neighbors(self.position):
            quarantined.append(city)
        quarantined.append(new_pos)

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

    def build_station(self, city, research_stations):
        if self.position == city and len(research_stations) < MAX_STATIONS:
            research_stations.append(city)

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

    def can_cure(self, color):
        needed = 4
        count = 0
        for card in self.hand:
            count += card // CITIES_PER_COLOR == color
        return count >= needed

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

    def move(self, new_pos, board, cures, cubes, quarantined):
        if self.selected == self:
            self.position = new_pos
        else:
            self.selected.move(new_pos, board, cures, cubes, quarantined)

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

    def can_share(self, card, target):
        if card in self.hand and self.position == target.get_position():
            return True
        else:
            return card in target.hand and card == self.position and self.position == taarget.position()
