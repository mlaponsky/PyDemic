# -*- coding: utf-8 -*-

import constants

class Player:
    hand = set()

    def __init__(self, role):
        self.role = role
        self.position = constants.ATL

        numActions = constants.MAX_ACTIONS
    def get_role(self):
        return self.role

    def get_position(self):
        return self.position

    def perform_action(self):
        if self.numActions != 0:
            self.numActions -= 1

    def move(self, newPos):
        self.position = newPos

    def reset_actions(self):
        self.actions = constants.MAX_ACTIONS

    def get_card(self, card):
        self.hand.add(card)

    def discard(self, card):
        if card in self.hand:
            self.hand.remove(card)

    def can_cure(self, color):
        needed = 4 if self.role == constants.SCIENTIST else 5
        count = 0
        for card in self.hand:
            count += card // 12 == color
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
