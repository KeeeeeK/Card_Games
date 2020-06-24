from typing import List
from .Containers import CG_Hand, CG_Deck_and_Discard
from .CG_Card import CG_Card


class CG_Player:
    __slots__ = ('name', 'hand', 'deck_and_discard', 'deck', 'discard')

    def __init__(self, name: str, hand: CG_Hand, deck_and_discard: CG_Deck_and_Discard):
        self.name = name
        self.hand = hand
        self.deck_and_discard = deck_and_discard
        # следующие два поля введены чисто для удобства
        self.deck = deck_and_discard.deck
        self.discard = deck_and_discard.discard

    def take_card(self) -> bool:
        """Возвращает False, если карт в колоде и сбросе нет. Иначе True."""
        card = self.deck_and_discard.give()
        if card is None:
            return False
        self.hand.add(card)
        return True

    def drop(self, card: CG_Card) -> None:
        """Сбрасывает данную карту в сброс"""
        self.discard.add(card)

    def __str__(self):
        return self.name
