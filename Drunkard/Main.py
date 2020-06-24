from random import sample
from Card_game.Containers import CG_Container, CG_Deck_and_Discard
from Drunkard.Player import Player
from Drunkard.Cards import full_deck
from Drunkard.Game import Game

nones, w1, w2, fr = 0, 0, 0, 0
lst_1, lst_2, lst_fr = [], [], []
for n in range(100):
    if n.__mod__(100)==0:
        print(n)
    half_deck = sample(full_deck, int(len(full_deck)/2))
    another_half = list(set(full_deck)-set(half_deck))
    player1 = Player('Булат', CG_Deck_and_Discard(CG_Container(half_deck), CG_Container([])))
    player2 = Player('Tагир', CG_Deck_and_Discard(CG_Container(another_half), CG_Container([])))
    game = Game(player1, player2)
    winner = None
    i = 0
    while winner is None and i<10000:
        # print('new_turn', i)
        # print('Булат: ', len(player1.deck), len(player1.discard))
        # print('Тагир: ', len(player2.deck), len(player2.discard))
        i+=1
        winner = game.next_turn()
    if winner is None:
        nones+=1
    elif winner==player1:
        w1+=1
        lst_1.append(i)
    elif winner==player2:
        w2+=1
        lst_2.append(i)
    elif winner.name=='Дружба':
        fr+=1
        lst_fr.append(i)
print(nones, w1, w2, fr)
# print(lst_1)
# print(lst_2)
# print(lst_fr)
# 495 4333 4499 673
# 514 4318 4512 656