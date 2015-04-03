# -*- coding: utf-8 -*-

from .constants import *
from random import shuffle

class Deck:
    def __init__(self):
        self.deck = []
        self.discard = []
        self.graveyard = []

    def get_deck(self):
        return self.deck

    def get_discard(self):
        return self.discard

    def get_graveyard(self):
        return self.graveyard

    def draw_card(self, index):
        return self.deck.pop(index)

    def add_to_discard(self, name):
        self.discard.append(name)

    def add_to_graveyard(self, name):
        self.graveyard.append(name)

    def remove_from_discard(self, card):
        self.discard.remove(card)

    def shuffle_deck(self):
        shuffle(self.deck)

    def shuffle_discard(self):
        shuffle(self.discard)

class PlayerCards(Deck):
    def __init__(self, players, num_epidemics):
        super(PlayerCards, self).__init__()
        self.fill_deck()
        self.deal_start(players)
        self.set_deck(num_epidemics)

    def fill_deck(self):
        self.deck = [card for card in range(NUM_PLAYER_CARDS)]
        shuffle(self.deck)

    def deal_start(self, players):
        if len(players) == 2:
            hand_size = 4
        elif len(players) == 3:
            hand_size = 3
        else:
            hand_size = 2
        for i in range(hand_size):
            for player in players:
                player.add_card(self.deck.pop(0))

    def set_deck(self, num_epidemics):
        segment_size = len(self.deck) // num_epidemics
        extras = len(self.deck) % num_epidemics
        segments = []
        start = 0
        end = 0

        for i in range(num_epidemics):
            end = start + segment_size + (extras > 0)
            extras -= 1
            segment = self.deck[start:end]
            segment.append(EPIDEMIC)
            shuffle(segment)
            segments.append(segment)
            start = end

        new_deck = []
        for segment in segments:
            new_deck += segment
        self.deck = new_deck

class InfectCards(Deck):
    def __init__(self):
        super(InfectCards, self).__init__()
        self.fill_deck()

    def fill_deck(self):
        self.deck = [ card for card in range(NUM_CITIES) ]
        shuffle(self.deck)

    def recombine(self):
        shuffle(self.discard)
        self.deck = self.discard + self.deck
        self.discard = []
