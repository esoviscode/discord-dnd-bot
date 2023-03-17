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

        if source.action_points <= 0:
            return False, 'You\'re out of action points!'

        if isinstance(source, Player):
            attack_status_message = f'**{source.name}** has attacked **{target.name}**' \
                                    f' using a *{source.equipment.right_hand.name}*!\n\n'
        else:
            attack_status_message = f'**{source.name}** has attacked **{target.name}**!\n\n'

        # TODO handle evasion more properly
        if random.choice([0, 1, 2, 3]) == 3:  # evasion
            return True, attack_status_message + f'💨 **{target.name}** successfully dodged the attack!'

        damage = 0
        if source.creature_class == 'Warrior':  # TODO this should be taken from an enum
            damage = source.strength
        if source.creature_class == 'Mage':
            damage = source.intelligence
        if source.creature_class == 'Ranger':
            damage = source.dexterity

        if source.equipment.right_hand:
            damage += random.randint(*source.equipment.right_hand.damage)

        target.hp -= damage
        source.action_points -= source.equipment.right_hand.action_points

        if target.hp <= 0:
            target_name = target.name
            game.delete_entity(target.id)
            return True, attack_status_message[:-3] + f' for  `{damage}`  damage!\n\n' + f'💀 {target_name} has been defeated!'

        return True, attack_status_message[:-3] + f' for `{damage}` damage!\n\n' + \
                                                  f'**{target.name}** has `{target.hp}` HP left!'
