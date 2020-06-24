from Dominion.All_Classes import *
from typing import Tuple

GIVES_TYPE = Callable[[Card, Game, Player], bool]


def merger(*funcs: GIVES_TYPE) -> GIVES_TYPE:
    def ret_func(card: Card, game: Game, player: Player):
        for func in funcs:
            if func(card, game, player) is False:
                return False
        return True

    return ret_func


def plus_actions(num_actions: int) -> GIVES_TYPE:
    def ret_func(card: Card, game: Game, player: Player) -> bool:
        nonlocal num_actions
        player.actions += num_actions
        return True

    return ret_func


def plus_cards(num_cards: int):
    def ret_func(card: Card, game: Game, player: Player) -> bool:
        nonlocal num_cards
        for i in range(num_cards):
            if player.take_card() is False:
                return False
        return True

    return ret_func


def add_to_play_zone(card: Card, game: Game, player: Player) -> bool:
    if card not in player.hand:
        return False
    player.play_zone.add(player.hand.give(card))
    return True


def choose_card_from_hand(card: Card, game: Game, player: Player) -> Tuple[Card, Game]:
    return player.presenter.choose_cards(player.hand.content, 1, 1)[0], game


def drop_cards_to_trash_from_hand(cards_min: int, cards_max: int):
    def ret_func(card: Card, game: Game, player: Player) -> bool:
        if len(player.hand) == 0:
            return False
        game.trash.add(player.hand.give(player.presenter.choose_cards(player.hand.content, 1, 1)[0]))
        return True

    return ret_func


village = Card('Деревня', 'todo', Resources([3]),
               {Card.action: merger(plus_actions(2), plus_cards(1), add_to_play_zone)})

reconstruction = Card('Реконструкция', 'todo', Resources([4]),
                      {Card.action: merger(add_to_play_zone, drop_cards_to_trash_from_hand(1, 1))})
