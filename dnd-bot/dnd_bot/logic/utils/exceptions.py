class DiscordDndBotException(Exception):
    """
    primary exception class for this project
    """
    pass


# lobby exceptions
class LobbyException(DiscordDndBotException):
    """thrown when there is an issue or error during lobby phase"""
    pass


class CreateLobbyException(LobbyException):
    """thrown when there is an issue or error while creating a lobby"""
    pass


class JoinLobbyException(LobbyException):
    """thrown when there is an issue or error while joining a lobby"""
    pass


class OnReadyException(LobbyException):
    """thrown when there is an issue or error while a player is ready"""
    pass


class StartGameException(LobbyException):
    """thrown when there is an issue or error while starting game - beginning character creation"""
    pass


# character creation exceptions
class CharacterCreationException(DiscordDndBotException):
    """thrown when there is an issue or error during character creation phase"""
    pass


class StartCharacterCreationException(CharacterCreationException):
    """thrown when there is an issue or error while starting character creation"""
    pass


class CharacterCreationInterfaceException(CharacterCreationException):
    """thrown when there is an issue or error with the character creation user interface - messages, embeds etc"""
    pass


# game
class GameException(DiscordDndBotException):
    """thrown when there is an issue or error during game phase"""
    pass


class InitializeWorldException(GameException):
    """thrown when there is an issue or error during world initialization"""
    pass
