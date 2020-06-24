from __future__ import annotations
from typing import List, Optional, Callable
from random import shuffle
from .CG_Card import CG_Card


class CG_Container:
    __slots__ = ('content',)
    """Контейнер карт"""

    def __init__(self, content: List[CG_Card]):
        self.content: List[CG_Card] = content

    def add(self, card: CG_Card) -> CG_Container:
        """ Добавляет карту в начало контейнера. """
        self.content.insert(0, card)
        return self

    def give(self, card: Optional[CG_Card] = None) -> Optional[CG_Card]:
        """ Удаляет 1 карту данного типа из контейнера. Если тип не указан, удаляется первая карта в контейнере
        Возвращает данную карту.
        В случае отсутствия такой карты возвращает None.
        """
        if card is None:
            if len(self.content) == 0:
                return None
            else:
                card = self.content[0]
        if card in self.content:
            self.content.remove(card)
            return card
        return None

    def shuffle(self) -> CG_Container:
        """ Перемешивает контейнер. """
        self.content = shuffle(self.content)
        return self

    def clean(self) -> List[CG_Card]:
        """ Опустошает контейнер. Возвращает список карт, которые были в контейнере. """
        self.content, content = [], self.content
        return content

    def __contains__(self, item: CG_Card):
        return item in self.content

    def __len__(self):
        return len(self.content)

    def __getitem__(self, item: int):
        return self.content[item]

    def __iter__(self):
        return iter(self.content)


class CG_Hand(CG_Container):
    __slots__ = ('size', 'sorting_func')

    def __init__(self, original_content: List[CG_Card], original_size: Optional[int] = None,
                 sorting_func: Optional[Callable] = None):
        super().__init__(original_content)
        self.size: int = original_size if original_size is not None else len(original_content)
        self.sorting_func: Callable = sorting_func if sorting_func is not None else lambda x, *args: x

    def sort(self) -> CG_Hand:
        """ Сортирует в соответсвии с self.sorting_func. Возвращает себя"""
        self.content = self.sorting_func(self.content)
        return self

    def add(self, card: CG_Card) -> CG_Hand:
        """ Добавляет карту и сортирует """
        super().add(card)
        self.sort()
        return self


class CG_Deck_and_Discard:
    __slots__ = ('deck', 'discard')

    def __init__(self, deck: CG_Container, discard: CG_Container):
        # нулевой считается верхняя карта в обоих контейнерах
        self.deck = deck
        self.discard = discard

    def _discard_to_deck(self):
        self.deck.content += self.discard.clean()
        self.deck.shuffle()

    def give(self) -> Optional[CG_Card]:
        """Возвращает None, если карт больше нет в обоих контейнерах"""
        if len(self.deck) == 0:
            if len(self.discard) == 0:
                return None
            self._discard_to_deck()
        return self.deck.give(self.deck[0])
