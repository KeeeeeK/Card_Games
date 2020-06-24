from Card_game.CG_Game import CG_Game as CG_Game
from Drunkard.Player import Player
from Card_game.Containers import CG_Container, CG_Deck_and_Discard

class Game(CG_Game):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)

    def next_turn(self):
        if (len(self.players[0].deck)==0) and(len(self.players[1].deck)==0):
            return Player('Дружба', CG_Deck_and_Discard(CG_Container([]), CG_Container([])))
        for player in self.players:
            result = player.drop_card()
            if result == Player.lost:
                return self.another_player(player)

        win = None
        if self.players[0].discard[0]>self.players[1].discard[0]:
            win = self.players[0]
        elif self.players[1].discard[0]>self.players[0].discard[0]:
            win = self.players[1]

        if win is None:
            return None
        else:
            win.deck.content = win.discard.content+self.another_player(win).discard.content+win.deck.content
            self.another_player(win).discard.clean()
            win.discard.clean()
        return None
