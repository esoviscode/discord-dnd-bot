from enum import Enum


class Equipable(Enum):
    """ defines a type of an item - how it can be equipped"""
    NO = 0
    WEAPON = 1
    HELMET = 4
    CHEST = 5
    LEG_ARMOR = 6
    BOOTS = 7
    OFF_HAND = 8
    ACCESSORY = 9
