from .Shop import *
from .Player import *
from random import shuffle

action_phase = 1
money_phase = 2
purchase_phase = 3


class Game:
    def __init__(self, names_of_players, main_types, quantities_of_main_types, basic_types, quantities_of_basic_types, start_deck):
        self.shop = Shop(main_types, quantities_of_main_types, basic_types, quantities_of_basic_types)
        self.names_of_players = shuffle(names_of_players)
        allcards = main_types+basic_types
        self.players = [Player(start_deck, allcards), Player(start_deck, allcards)]
        self.player = self.players[0]
        self.phase = action_phase
        self.trash = []
        # self.additional_turns = []

    def next_phase(self):
        if self.phase == action_phase:
            self.phase = money_phase
        elif self.phase == money_phase:
            self.phase = purchase_phase
        elif self.phase == purchase_phase:
            self.phase = action_phase

    def another_player(self):
        return self.players[(self.players.index(self.player) + 1) % 2]

    def next_turn(self):
        # метод сам вызывается, когда игрок заканчивает ход
        self.next_phase()
        self.player = self.another_player()
        self.player.start_turn(self)
