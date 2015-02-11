# -*- coding: utf-8 -*-

import constants
from random import shuffle

class Deck:
    def __init__(self):
        self.deck = []
        self.discard = []
        self.graveyard = []

    def add_to_deck(self, name):
        self.deck.append(name)

    def add_to_discard(self, name):
        self.discard.append(name)

    def add_to_graveyard(self, name):
        self.graveyard.append(name)

    def draw_card(self, index):
        card = self.deck[index]
        self.deck.remove(card)
        return card

    def remove_from_discard(self, card):
        self.discard.remove[card]

    def shuffl_deck(self):
        shuffle(self.deck)

    def shuffle_discard(self):
        shuffle(self.discard)

    def recombine_decks(self):
        shuffle(self.discard)
        self.deck = self.discard + self.deck
        self.discard = []

    def get_deck(self):
        return self.deck

    def set_deck(self, deck):
        self.deck = deck

    def get_size(self):
        return len(self.deck)
