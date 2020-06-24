from Card_game.CG_Player import CG_Player as CG_Player
from Card_game.Containers import CG_Hand


class Player(CG_Player):
    empty_deck, lost = 1, 2
    def __init__(self, name, deck_and_discard):
        super().__init__(name, CG_Hand([]), deck_and_discard)
        self.deck = deck_and_discard.deck
        self.discard = deck_and_discard.discard

    def drop_card(self):
        if len(self.discard)==0 and len(self.deck)==0:
            return Player.lost
        if len(self.deck_and_discard.deck) == 0:
            return Player.empty_deck
        card = self.deck_and_discard.give()
        self.deck_and_discard.discard.add(card)
        return True
