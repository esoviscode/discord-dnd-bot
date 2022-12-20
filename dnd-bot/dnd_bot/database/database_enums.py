from enum import Enum


class DatabaseEnums:
    class GameState(Enum):
        LOBBY = 'LOBBY'
        STARTING = 'STARTING'
        ACTIVE = 'ACTIVE'
        INACTIVE = 'INACTIVE'
        FINISHED = 'FINISHED'
