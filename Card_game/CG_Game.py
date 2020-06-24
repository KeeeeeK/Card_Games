from typing import List, Optional
from .CG_Player import CG_Player
from .CG_Phase import CG_Phase


# action_phase = 1
# money_phase = 2
# purchase_phase = 3


class CG_Game:
    def __init__(self, player_1: CG_Player, player_2: CG_Player, phases: Optional[List[CG_Phase]] = None):
        self.players: List[CG_Player] = [player_1, player_2]
        self.active_player: CG_Player = player_1
        self.phases: List[CG_Phase] = phases if phases is not None else [CG_Phase()]
        self.phase: CG_Phase = self.phases[0]

    def info_next_phase(self) -> CG_Phase:
        next_phase = (self.phases.index(self.phase) + 1).__mod__(len(self.phases))
        return self.phases[next_phase]

    def next_phase(self) -> None:
        self.phase = self.info_next_phase()

    def another_player(self, player: Optional[CG_Player] = None):
        if player is None:
            player = self.active_player
        return self.players[(self.players.index(player) + 1).__mod__(2)]

    def next_turn(self) -> None:
        self.phase = self.phases[0]
        self.active_player = self.another_player()
