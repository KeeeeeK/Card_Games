from .Card import Action, WinCard, Money
from .funcs import sort_allcards


# Следующий список очень важен.

class Hand:
    def __init__(self, allcards, size):
        self.sort = sort_allcards(allcards)  # 0-actions, 1-money, 2-not actable cards
        self.content = [[], [], []]
        self.size = size

    def add(self, card):
        for i in range(3):
            if card in self.sort[i]:
                self.content[i].append(card)
                sorted(self.content[i], key=lambda x: self.sort[i].index(x))
                return
        else:
            raise Exception("такой карты не должно существовать")

    def give(self, card):
        for i in range(3):
            if card in self.content[i]:
                self.content.remove(card)
                return card
        print("данной карты нет в руке")
        return None

    def include(self, card):
        for i in range(3):
            if card in self.content[i]:
                return True
        return False

    def is_empty(self):
        if len(self.content[0]) == len(self.content[1]) == len(self.content[2]) == 0:
            return True
        else:
            return False
