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


class MovementException(GameException):
    """thrown where there is an issue or error during movement process during game"""
    pass


class AttackException(GameException):
    """thrown where there is an issue or error during attack process during game"""
    pass


class SkillException(GameException):
    """thrown where there is an issue or error during skill using process during game"""
    pass


class LootCorpseException(GameException):
    """ thrown when there is an error while looting the corpse"""
    pass


# messager exceptions

class MessagerException(DiscordDndBotException):
    """thrown when the discord communication module (messager) encounters an issue"""
    pass


class DMCreationException(MessagerException):
    """thrown when the bot cant create a dm with a user"""
    pass


