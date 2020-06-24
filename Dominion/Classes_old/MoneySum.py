from functools import total_ordering


@total_ordering
class MoneySum:
    def __init__(self, coins, potion=0):
        # в этом формате указываются цены или money игрока
        self.coins = coins
        self.potion = potion

    def add_coins(self, coins):
        self.coins += coins

    def add_potion(self, potion):
        self.potion += potion

    def __add__(self, other):
        return MoneySum(self.coins + other.coins, self.potion + other.potion)

    def __iadd__(self, other):
        self.coins += other.coins
        self.potion += other.potion
        return self

    def __isub__(self, other):
        self.coins -= other.coins
        self.potion -= other.potion
        return self

    def __sub__(self, other):
        if self >= other:
            return MoneySum(self.coins - other.coins, self.potion - other.potion)
        else:
            return None

    def __eq__(self, other):
        return self.coins == other.coins and self.potion == other.potion

    def __ge__(self, other):
        return self.coins >= other.coins and self.potion >= other.potion
