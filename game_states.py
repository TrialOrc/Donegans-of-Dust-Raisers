from enum import Enum


class GameStates(Enum):
    PLAYERS_TURN = 1
    MOVE = 2
    ENEMY_TURN = 3
    PLAYER_DEAD = 4
