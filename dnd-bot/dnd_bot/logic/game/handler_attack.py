import random

from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.prototype.player import Player


class HandlerAttack:
    @staticmethod
    async def handle_attack(source: Creature, target: Creature, token) -> (bool, str):
        """
        handler for attacking enemy with main weapon
        """

        game: Game = Multiverse.get_game(token)

        if target is None or not isinstance(target, Creature):
            return False, 'The target does not exist!'

        if source != game.active_creature:
            return False, 'You can\'t perform a move right now!'

        if source.action_points < source.equipment.right_hand.action_points:
            return False, 'You have an insufficient number of action points!'

        if isinstance(source, Player):
            attack_status_message = f'**{source.name}** has attacked **{target.name}** at ({target.x},{target.y})\n' \
                                    f' using a *{source.equipment.right_hand.name}*!\n\n'
        else:
            attack_status_message = f'**{source.name}** has attacked **{target.name}**!\n\n'

        source.action_points -= source.equipment.right_hand.action_points

        # dodging an attack
        # the chance is (source dexterity)%
        if random.randint(0, 99) <= source.dexterity:  # evasion
            return True, attack_status_message + f'💨 **{target.name}** successfully dodged the attack!'

        # calculating damage
        # damage = main class attribute + damage from weapon
        base_damage = 0
        if source.creature_class == 'Warrior':  # TODO this should be taken from an enum
            base_damage = source.strength
        if source.creature_class == 'Mage':
            base_damage = source.intelligence
        if source.creature_class == 'Ranger':
            base_damage = source.dexterity

        weapon_damage = 0
        if source.equipment.right_hand:
            weapon_damage += random.randint(*source.equipment.right_hand.damage)

        target.hp -= (base_damage + weapon_damage)

        if target.hp <= 0:
            target_name = target.name
            game.delete_entity(target.id)
            return True, attack_status_message[:-3] + f' for ' \
                                                      f'**`{base_damage + weapon_damage}`**  damage!\n\n' + \
                                                      f'> 💀 **{target_name}** has been defeated!'

        return True, attack_status_message[:-3] + f' for **`{base_damage + weapon_damage}`** damage!\n\n' + \
                                                  f'> **{target.name}** has `{target.hp}` HP left!'
