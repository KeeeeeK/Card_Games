from .Card import Action, Money, WinCard, holding_type
from .Slot import Slot
from copy import deepcopy as copy  # каждой карте на самом деле достаточно ссылки на её тип


class Shop:
    def __init__(self, main_types, quantities_of_main_types, basic_types, quantities_of_basic_types):
        if len(main_types) != len(quantities_of_main_types):
            raise Exception("Неверная инициализация")
        self.slots = [Slot(main_types[i], quantities_of_main_types[i]) for i in range(len(main_types))]
        self.basic_types = basic_types
        self.slots += [Slot(basic_types[i], quantities_of_basic_types[i]) for i in range(len(basic_types))]
        # Если создать изначально 0 Поместий, то оно не будет влиять на игру.
        # Если было 0 Реконструкций, то оно тоже не будет влиять.
        self.end_game = False
        self.ended_main_types = 0

    def when_buy_slot(self, card, game, player):
        slot = self._find_slot(card)
        if slot is None:
            print('нет такого слота')
        for action in slot.when_buy:
            action(game, player)

    # функция может быть не выполнена!
    def _find_slot(self, type):
        for slot in self.slots:
            if slot.type == type:
                return slot
        return None

    # функция может быть не выполнена!
    def give_card(self, type):
        slot = self._find_slot(type)
        if slot is None:
            print("Данная карта не представлена в магазине!")
            return None
        if slot.quantity != 0:
            slot.quantity -= 1
            if slot.quantity == 0:
                if type in self.basic_types and isinstance(type, WinCard) and type.type == holding_type:
                    self.end_game = True
                elif (type not in self.basic_types) or isinstance(type, WinCard) and type.type != holding_type:
                    self.ended_main_types += 1
                    if self.ended_main_types >= 3:
                        self.end_game = True
            return type
        else:
            print("Данная карта закончилось в магазине!")
            return None

    # # функция может быть не выполнена! Нужно сделать wbuy  слота и wbuy карты
    # def buy_card(self, type, game, player):
    #     card = self.give_card(type)
    #     if card is not None:
    #         type.w_buy(game)
