class Slot:
    def __init__(self, type, quantity):
        self.type = type
        self.quantity = quantity
        # список функций принимающих game, player
        self.when_buy = []

    def add_when_buy(self, when_buy):
        self.when_buy.append(when_buy)
