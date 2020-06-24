from __future__ import annotations
from typing import Callable, Dict, List, Union, Optional
from functools import reduce
from Card_game.CG_Player import CG_Player
from Card_game.CG_Card import CG_Card
from Card_game.CG_Game import CG_Game
from Card_game.Containers import CG_Hand, CG_Deck_and_Discard, CG_Container
from Card_game.CG_Phase import CG_Phase
from Card_game.CG_Resources import CG_Resources

Hand = CG_Hand
Deck_and_Discard = CG_Deck_and_Discard
Container = CG_Container
Resources = CG_Resources

Resources.coins_index = 0
Resources.indexes = [Resources.coins_index]


def default_ability(gives: Dict[int, Callable[[Card, Game, Player], Union[bool, int]]]):
    def ability(card: Card, game: Game, player: Player):
        return game.active_player == player and card in player.hand and \
               ((game.phase == Game.action_phase and Card.action in gives and player.actions > 0) or
                (game.phase == Game.treasure_phase and Card.treasure in gives))

    return ability


class Card(CG_Card):
    __slots__ = ('price', 'able', 'gives')

    action = 1
    treasure = 2
    victory = 3
    curse = 4
    attack = 5
    reaction = 6

    """ :arg gives - словарь, в котором ключи - индексы (action, treasure, ...), значения - соответствующие функции.
        Функции принимают на вход саму карту, игру и обладателя карты (или инициатора её розыгрыша)
        :arg ability - проверяет, можно ли сыграть данную карту данному игроку. Можно передать None, тогда
        преобразует его в default_ability(gives)
        Тип карты определяется наличием соответсвующего индекса в словаре.
        1) action - возвращает правильность отработки функции.(В силу зависимости от выбора игрока может быть не чистой)
        2) treasure - возвращает правильность отработки. После отработки меняет ресурсы игрока
        3) victory - возвращает количество очков, приносимое игроку этой картой
        4) curse - тоже возвращает количество очков, приносимое игроку этой картой с учётом знака
        5) attack - возвращает правильность отработки функции
        6) reaction - возвращает правильность отработки функции."""

    def __init__(self, name: str, description: str, price: Resources,
                 gives: Dict[int, Callable[[Card, Game, Player], Union[bool, int]]],
                 ability: Optional[Callable[[Card, Game, Player], bool]] = None):
        super().__init__(name, description)
        self.price: Resources = price
        self.gives: Dict[int, Callable[[Card, Game, Player], Union[bool, int]]] = gives
        self.able: Callable[[Card, Game, Player], bool] = ability if ability is not None else default_ability(gives)

    def type_is(self, index: int) -> bool:
        return index in self.gives

    def gives_points(self, game, player):
        """Возвращает сколько очков приносит карта игроку.
         Учитывает то, что карта может быть одновременно curse и victory"""
        return sum({self.gives.get(index, default=(lambda _game_, _player: 0))(game, player) for index in
                    [Card.victory, Card.curse]})


class Shop:
    def __init__(self, cards_to_quantities: Dict[Card, int]):
        self.content: Dict[Card, Container] = \
            {card: Container([card] * quantity) for card, quantity in cards_to_quantities.items()}

    def give(self, card: Card) -> Optional[Card]:
        """ Возвращает карту полученного и типа.
        В случае отсутствия такой карты возвращает None.
        None возвращается и если 'карта была в магазине, но закончилась', и если 'её никогда не было в магазине'"""
        if card not in self.content:
            return None
        return self.content[card].give()

    def add(self, card: Card) -> Optional[Shop]:
        """Возвращает None в случае, если такой карты ранее не было в магазине. Иначе возвращает себя"""
        slot = self.content.get(card)
        if slot is None:
            return None
        slot.add(card)
        return self

    def _lst_quantities(self, cards: List[Card]):
        return list(len(self.content[card]) for card in cards)

    def end_game(self) -> bool:
        """Игра заканчивается, если 'закончились поместья, герцогства или провинции' или 'закончились 3 и более карт'"""
        return self._lst_quantities(list(self.content.keys())).count(0) >= 3 or 0 in self._lst_quantities(
            list(filter(lambda card: card.name in {'Поместье', 'Герцогство', 'Провинция'}, self.content)))

    def enough_to_buy(self, resources: CG_Resources) -> List[Card]:
        return list(filter(lambda card: resources >= card.price and len(self.content[card]) != 0, self.content))


class Game(CG_Game):
    __slots__ = ('shop', 'trash')

    action_phase = CG_Phase(1)
    treasure_phase = CG_Phase(2)
    purchase_phase = CG_Phase(3)
    phases = [action_phase, treasure_phase, purchase_phase]

    def __init__(self, player_1: Player, player_2: Player, shop: Shop):
        super().__init__(player_1, player_2, Game.phases)
        self.shop: Shop = shop
        self.trash: Container = Container([])


class Player(CG_Player):
    __slots__ = ('actions', 'resources', 'purchases', 'play_zone', 'presenter')

    def __init__(self, name: str, hand: CG_Hand, deck_and_discard: CG_Deck_and_Discard):
        super().__init__(name, hand, deck_and_discard)
        self.actions: int = 1
        self.resources: CG_Resources = CG_Resources()
        self.purchases: int = 1
        self.play_zone: Container = Container([])
        self.presenter: Presenter = Presenter(self)

    def able_to_play(self, game: Game) -> List[Card]:
        """Возвращает список карт в руке, которые можно разыграть"""
        return list(filter(lambda card: card.able(game, self), self.hand))

    def all_cards(self) -> List[Card]:
        return self.hand.content + self.deck.content + self.discard.content

    def points(self, game: Game) -> int:
        """Возвращает текущее суммарное количество победных очков"""
        return reduce(lambda points, card: points + card.gives_points(game, self),
                      filter(lambda card: card.type_is(Card.victory) or card.type_is(Card.curse), self.all_cards()), 0)

    def able_to_buy(self, game: Game, card: Card) -> bool:
        """Возвращает False если 'не хватает ресурсов на покупку' или 'карта не представлена в магазине' или
        'сейчас игрок не имеет возможности покупать карты'."""
        return card in game.shop.enough_to_buy(self.resources) and \
               game.active_player == self and game.phase == Game.purchase_phase

    def buy(self, game: Game, card: Card) -> bool:
        """Возвращает тот же результат, что и able_to_buy"""
        if self.able_to_buy(game, card) is False:
            return False
        self.resources -= card.price
        self.discard.add(game.shop.give(card))
        return True

    def play_action(self, game: Game, card: Card) -> bool:
        """Возвращает False, если карту невозможно разыграть"""
        if card.able(card, game, self) is False:
            return False
        self.actions -= 1
        # self.play_zone.add(self.hand.give(card)) -- это делает gives
        card.gives[Card.action](card, game, self)
        return True

    def play_treasure(self, game: Game, card: Card) -> bool:
        """Возвращает False, если карту невозможно разыграть"""
        if card.able(card, game, self) is False:
            return False
        self.play_zone.add(self.hand.give(card))
        self.resources += card.gives[Card.treasure](game, self)
        return True

    def start_turn(self, game: Game) -> bool:
        """False если сейчас не ход игрока.
        Игрок выполняет действия в начале хода: ..."""
        if game.active_player != self:
            return False
        ...
        return True

    def end_turn(self, game: Game) -> bool:
        """False если сейчас не ход игрока.
        Игрок выполняет действия в конце хода: очистака игровой зоны, _set_default"""
        if game.active_player != self:
            return False
        self._set_default()
        # сделано это на дальнейший случай расширений в стиле 'когда карта попадает в сброс, ...'
        for card in self.play_zone.clean():
            self.discard.add(card)
        return True

    def _set_default(self) -> None:
        """Устанавливает параметры actions, resources, purchases на уровень,
        который обычно бывает в конце каждого хода"""
        self.actions, self.purchases = 1, 1
        self.resources -= self.resources
        return None

    def choose_cards(self, container: Container, filter_func: Callable[[Card], bool], n: int) -> List[Card]:
        """Игрок должен выбрать n карт из container"""
        ...


class Presenter:
    def __init__(self, player: Player):
        self.player: Player = player

    def choose_cards(self, assortment: List[Card], num_cards_min: int, num_cards_max: int) -> List[Card]:
        """Взывает к игроку-пользоавтелю, принимает на вход
        :arg assortment -- контейнер из которого будет произведён выбор
        :arg num_cards_min -- минимум количества карт, которые необходимо выбрать
        :arg num_cards_max -- максимум количества карт, которые необходимо выбрать"""
        if len(assortment) <= num_cards_min:
            return assortment
        print(f'Выберите от {num_cards_min} до {num_cards_max} карт из:')
        for i, card in enumerate(assortment):
            print(f'{i + 1}) {card.name}')
        num_cards: str = input()
        try:
            num_cards: List[int] = list(map(int, num_cards.split()))
        except ValueError:
            print('Карты под номерами 1, 5 надо выбирать так: "1 5" или "5 1". Лишние символы недопустимы.'
                  'Запускаю выбор заново.')
            return self.choose_cards(assortment, num_cards_min, num_cards_max)
        if not (num_cards_min <= len(num_cards) <= num_cards_max):
            print('Вы ввели слишком много или слишком мало номеров карт. Запускаю выбор заново')
            return self.choose_cards(assortment, num_cards_min, num_cards_max)
        try:
            return [assortment[i - 1] for i in num_cards]
        except IndexError:
            print('Нет карты с одним из номеров. Запускаю выбор заново')
            return self.choose_cards(assortment, num_cards_min, num_cards_max)
