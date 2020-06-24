from random import shuffle
from .Hand import Hand
from .Game import action_phase, money_phase, purchase_phase
from .MoneySum import MoneySum

start_actions = 1
start_purchases = 1
start_money = MoneySum(0)
hand_size = 5


class Player:
    def __init__(self, start_deck, allcards):
        # сам по себе игрок в начале игры сидит без карт. а потому уже добирает их
        self.hand = Hand(allcards, hand_size)
        self.deck = start_deck
        self.play_zone = []
        self.discard = []
        self.actions = start_actions
        self.purchase = start_purchases
        self.money = start_money

        # увы, некоторые карты могут изменять данный параметр
        # списки действий, которые необходимо сделать
        self.in_the_beginning = []
        # self.in_action_phase = []
        # self.in_money_phase = []
        # self.in_purchase_phase = []
        self.in_the_end = []

    def start_turn(self, game):
        # метод сам вызывается, когда игра передаёт ход
        while len(self.in_the_beginning) != 0:
            self.in_the_beginning.pop(0)(game)

    def _ending(self, game):
        while len(self.in_the_end) != 0:
            self.in_the_end.pop(0)(game)

    def end_turn(self, game):
        while not self.hand.is_empty():
            card = (self.hand.content[0] + self.hand.content[1] + self.hand.content[2])[0]
            self.drop_from_hand(card, game)
        while len(self.play_zone) != 0:
            card = self.play_zone[0]
            self.drop_from_play_zone(card, game)
        self._ending(game)
        for i in range(self.hand.size):
            self.take(game)
        game.next_turn()

    def play(self, card, game):
        # суть проста: проверяем, что сыграть можно. потом вычитаем действие, кладём в игровую зону и играем карту
        if self.hand.include(card):
            if game.phase == action_phase:
                if card in self.hand.content[0]:
                    if self.actions != 0:
                        # Неужели что-то можно всё же сыграть??
                        self.actions -= 1
                        card = self.hand.give(card)
                        self.play_zone.append(card)
                        card.w_act(game, self)
                    else:
                        print('Не хватает действий')
                else:
                    print('Нельзя играть в эту фазу')
            elif game.phase == money_phase:
                if card in self.hand.content[1]:
                    card = self.hand.give(card)
                    self.play_zone.append(card)
                    card.w_act(game, self)
                else:
                    print('Нельзя играть в эту фазу')

            else:
                print('Сейчас нельзя играть карты')
        else:
            print('Карты нет в руке')

    def buy(self, card, game):
        if game.phase != purchase_phase:
            print('Нельзя сейчас купить')
            return
        if self.purchase == 0:
            print('Не хватает покупок')
            return
        if card.price > self.money:
            print('Не хватает денег')
            return
        card = game.shop.give_card(card)
        if card is None:
            return
        self.money -= card.price
        self.purchase -= 1
        game.shop.when_buy_slot(card, game, self)
        card.w_buy(game, self)

    def gain(self, card, game):
        # Получается, что ничего вообще не может помешать игроку получить карту.
        card.w_gain(game, self)

    def drop_from_hand(self, card, game):
        card = self.hand.give(card)
        if card is None:
            # карты нет в руке и give уже сообщил об этом
            return
        self.discard.append(card)
        card.w_drop(game, self)

    def drop_from_play_zone(self, card, game):
        if card in self.play_zone:
            self.play_zone.remove(card)
            self.discard.append(card)
            card.w_drop(game, self)
        else:
            print('этой карты нет в игровой зоне')

    def take(self, game):
        if len(self.deck) != 0:
            card = self.deck.pop(0)
            self.hand.add(card)
            card.w_take(game, self)
        else:
            if len(self.discard) != 0:
                # мешаем сброс в колоду
                self.deck = self.discard
                shuffle(self.deck)
                self.discard = []
                self.take(game)
            else:
                print('сброс и колода пусты')

    def throw(self, container, card, game):
        # container - откуда выкинуть карту
        if container == self.hand:
            card = self.hand.give(card)
            if card is None:
                # карты нет в руки и гив уже сообщил об этом
                return
            game.trash.append(card)
            card.w_throw(game, self)
        elif container == self.deck:
            if card in self.deck:
                self.deck.remove(card)
                game.trash.append(card)
                card.w_throw(game, self)
            else:
                print('Карты нет в колоде')
        elif container == self.discard:
            if card in self.discard:
                self.discard.remove(card)
                game.trash.append(card)
                card.w_throw(game, self)
            else:
                print('Карты нет в сбросе')
        else:
            print('Контейнер, из которого пытаются выкинуть карту, не принадлежит игроку')

    def look_through(self, num):
        return self.deck[:num]
