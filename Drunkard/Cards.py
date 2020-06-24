from Card_game.CG_Card import CG_Card as CG_card

class Seniority:
    m = 9
    def __init__(self, i):
        self.content = i

    def __gt__(self, other):
        if self.content==0 and other.content==Seniority.m:
            return True
        else:
            return self.content>other.content


class Card(CG_card):
    suits = ['пик', 'крестей', 'червей', 'бубей']
    seniorities = list(Seniority(i) for i in range(Seniority.m))

    def __init__(self, suit, seniority):
        self.suit = suit
        self.seniority = seniority
        super().__init__('', '')

    def __gt__(self, other):
        if self.suit == other.suit and self.seniority>other.seniority:
            return True
        return False


full_deck = list(Card(suit, seniority) for suit in Card.suits for seniority in Card.seniorities)