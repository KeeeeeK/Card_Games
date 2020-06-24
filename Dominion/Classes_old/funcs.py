from .Card import Action, Money, WinCard


# возвращает функцию, которая добавляет деньги и принимает на вход (game),
# def add_money(value):
#     return lambda game: game.player.add_money(value)


def add_power(power):
    return lambda game, player: power

def sort_allcards(allcards):
    # следует обратить внимание, что порядок карт в allcards задаёт пордок в руке
    actable, money, other = [], [], []
    for card in allcards:
        if isinstance(card, Money):
            money.append(card)
        elif isinstance(card, Action) or isinstance(card, WinCard) and card.actable is True:
            actable.append(card)
        else:
            other.append(card)
    return actable, money, other
