from __future__ import annotations
from functools import total_ordering, reduce
from typing import List, Optional, Dict


@total_ordering
class CG_Resources:
    """ В этом формате указываются цены или ресурсы игрока. """
    # Это поле необходимо исправить под себя при импортировании. Здесь представлен лишь примерный вариант реализации
    # coins_index = 0
    # potion_index = 1
    # indexes = [coins_index, potion_index]
    indexes: List[int] = []

    def __init__(self, resources: Optional[List[int]] = None):
        if resources is None:
            resources = [0] * len(CG_Resources.indexes)
        if len(resources) != len(CG_Resources.indexes):
            print("Неправильно указана цена")
        self.content: Dict[int, int] = dict(zip(CG_Resources.indexes, resources))

    def amount(self, index) -> int:
        return self.content[index]

    def set_0(self) -> None:
        self.content = dict.fromkeys(CG_Resources.indexes, 0)
        return None

    def __add__(self, other: CG_Resources) -> CG_Resources:
        result_content = [self.amount(index) + other.amount(index) for index in CG_Resources.indexes]
        return CG_Resources(result_content)

    def __iadd__(self, other) -> CG_Resources:
        self.content = (self + other).content
        return self

    def __sub__(self, other) -> CG_Resources:
        result_content = [self.amount(index) - other.amount(index) for index in CG_Resources.indexes]
        return CG_Resources(result_content)

    def __isub__(self, other) -> CG_Resources:
        self.content = (self - other).content
        return self

    def __eq__(self, other) -> bool:
        return self.content == other.cotent

    def __ge__(self, other) -> bool:
        return reduce(lambda result, index: result and self.amount(index) >= other.amount(index),
                      CG_Resources.indexes, True)
