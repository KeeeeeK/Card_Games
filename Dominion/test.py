from Dominion.cards import *
from copy import deepcopy
none_card = Card('none', 'none', Resources([0]), {}, None)

test_card = reconstruction
hand = Hand([none_card]*3+[village]+[test_card])


deck_and_discard = Deck_and_Discard(Container([none_card]*5), Container([]))
player1 = Player('Булат', hand, deck_and_discard)
player2 = Player('Аня', deepcopy(hand), deepcopy(deck_and_discard))
shop = Shop({none_card: 10})
game = Game(player1, player2, shop)
player: Player = game.active_player


print(f'actions={player.actions}, len(hand)={len(player.hand)}, len(play_zone)={len(player.play_zone)}')
print(f'able={test_card.able(test_card, game, player)}, result={player.play_action(game, test_card)}')
print(f'actions={player.actions}, len(hand)={len(player.hand)}, len(play_zone)={len(player.play_zone)}')
for i, card in enumerate(player.hand):
    print(f'{i + 1}: {card.name}; ', end='')
