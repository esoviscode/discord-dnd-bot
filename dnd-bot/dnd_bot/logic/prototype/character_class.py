from abc import ABC, abstractmethod


class CharacterClass(ABC):
    """Abstract interface defining methods which must be overriden by classes defining particular character classes"""

    @staticmethod
    @abstractmethod
    def emoji():
        pass

    @staticmethod
    @abstractmethod
    def base_hp():
        pass

    @staticmethod
    @abstractmethod
    def base_strength():
        pass

    @staticmethod
    @abstractmethod
    def base_dexterity():
        pass

    @staticmethod
    @abstractmethod
    def base_intelligence():
        pass

    @staticmethod
    @abstractmethod
    def base_charisma():
        pass

    @staticmethod
    @abstractmethod
    def base_perception():
        pass

    @staticmethod
    @abstractmethod
    def base_action_points():
        pass

    @staticmethod
    @abstractmethod
    def base_initiative():
        pass
