# -*- coding: utf-8 -*-

from constants import *

class Player:
    hand = set()

    def __init__(self, role):
        self.role = role
        self.position = ATL

    def get_role(self):
        return self.role

    def get_position(self):
        return self.position

    def move(self, new_pos, board, cures, cubes, quarantined):
        self.position = new_pos

    def get_card(self, card):
        self.hand.add(card)

    def discard(self, card):
        if card in self.hand:
            self.hand.remove(card)

    def treat(self, color, cures, cubes):
        if not cures[color]:
            cubes[self.position][color] -= 1
        else:
            cubes[self.position][color] = 0

    def can_cure(self, color):
        needed = 5
        count = 0
        for card in self.hand:
            count += card // CITIES_PER_COLOR == color
        return count >= needed

    def make_cure(self, cards):
        if cards.issubset(self.hand):
            self.hand = self.hand - cards

    def has_card(self, card):
        return card in self.hand

    def get_card_from_hand(self, card):
        if self.hasCard(card):
            return card
        return ""

# Role subclasses; contain special implementations of actions
class Medic(Player):
    def move(self, new_pos, board, cures, cubes, quarantined):
        self.position = new_pos
        for color in COLORS:
            if cures[color]:
                cubes[self.position][color] = 0

    def treat(self, cures, cubes):
        if not cures[color]:
            cubes[self.position][color] = 0

class QS(Player):
    def move(self, new_pos, board, cures, cubes, quarantined):
        self.position = new_pos
        quarantined = board.get_neighbors(self.position)
        quarantined.append(new_position)

class Reasearcher(Player):

class OE(Player):

class CP(Player):
    self.event = None
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
    def can_cure(self, color):
        needed = 4
        count = 0
        for card in self.hand:
            count += card // CITIES_PER_COLOR == color
        return count >= needed

class Dispatcher(Player):
