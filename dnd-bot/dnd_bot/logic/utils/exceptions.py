class DiscordDndBotException(Exception):
    pass


# lobby
class LobbyException(DiscordDndBotException):
    pass


class CreateLobbyException(LobbyException):
    pass


class JoinLobbyException(LobbyException):
    pass


class OnReadyException(LobbyException):
    pass


class StartGameException(LobbyException):
    pass


# character creation
class CharacterCreationException(DiscordDndBotException):
    pass


class StartCharacterCreationException(CharacterCreationException):
    pass


class CharacterCreationInterfaceException(CharacterCreationException):
    pass


# game
class GameException(DiscordDndBotException):
    pass


class InitializeWorldException(GameException):
    pass
