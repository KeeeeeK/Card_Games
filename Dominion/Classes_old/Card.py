class Card:
    def __init__(self, price, name, when, description):
        # price принадлежит классу MoneySum
        self.price = price
    # В силу того, что к картам можно будет добавлять совойства, равенство карт производится именно по параметру name
        self.name = name
        self.when = when
        self.description = description
        # список действий, которые может сделать карта. Действия могут также делать и сокровища. Игра в какую-то фазу
        # зависит от типа карты.

    def w_act(self, game, player):
        for action in self.when.act:
            action(game, player)

    def w_buy(self, game, player):
        for action in self.when.buy:
            action(game, player)

    def w_gain(self, game, player):
        for action in self.when.gain:
            action(game, player)

    def w_take(self, game, player):
        for action in self.when.take:
            action(game, player)

    def w_drop(self, game, player):
        for action in self.when.drop:
            action(game, player)

    def w_throw(self, game, player):
        for action in self.when.throw:
            action(game, player)


class Money(Card):
    def __init__(self, price, name, when, description):
        super().__init__(price, name, when, description)

    # def act(self, *args):
    #     player.money += self.value
    #     player.hand.remove(self)
    #     player.discard.append(self)
    #     return True


class Action(Card):
    def __init__(self, price, name, when, description):
        super().__init__(price, name, when, description)

    # def act(self, player, *args):
    #     if player.actions != 0:
    #         player.actions -= 1
    #         if len(args)!=1:
    #             print('Большая ошибка с act_card')
    #         self.func(player, args[0])
    #         return True
    #     else:
    #         print("Не хватает действий!")
    #         return False


holding_type = 0
curse_type = 1


class WinCard(Card):
    def __init__(self, price, name, when, description, power, actable, type):
        super().__init__(price, name, when, description)
        self.actable = actable
        # Пхах, это не число, а функция, принимающая game и возвращающая число
        self.power = power
        self.type = type
