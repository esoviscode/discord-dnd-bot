import random

from dnd_bot.logic.game.handler_kill_enemy import HandlerKillEnemy
from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.prototype.player import Player
from dnd_bot.logic.utils.exceptions import AttackException


class HandlerAttack:
    @staticmethod
    async def handle_attack(source: Creature, target: Creature, token) -> str:
        """
        handler for attacking enemy with main weapon
        return: message describing attack process which will be sent to users
        """

        game: Game = Multiverse.get_game(token)

        if target is None or not isinstance(target, Creature):
            raise AttackException("The target does not exist!")

        if source != game.active_creature:
            raise AttackException("You can't perform a move right now!")

        if source.equipment.right_hand:
            if source.action_points < source.equipment.right_hand.action_points:
                raise AttackException("You have an insufficient number of action points!")

            if isinstance(source, Player):
                attack_status_message = f'**{source.name}** has attacked **{target.name}** at ({target.x},{target.y})' \
                                        f'\n using *{source.equipment.right_hand.name}*!\n\n'
            else:
                attack_status_message = f'**{source.name}** has attacked **{target.name}**!\n\n'

            source.action_points -= source.equipment.right_hand.action_points
        # no weapon - fight with fists
        else:
            if source.action_points < 2:
                raise AttackException("You have an insufficient number of action points!")

            if isinstance(source, Player):
                attack_status_message = f'**{source.name}** has attacked **{target.name}** at ({target.x},{target.y})' \
                                        f'\n using fists!\n\n'
            else:
                attack_status_message = f'**{source.name}** has attacked **{target.name}**!\n\n'

            source.action_points -= 2

        # dodging an attack
        # the chance is (source dexterity)%
        if random.randint(0, 99) <= source.dexterity:  # evasion
            return attack_status_message + f'💨 **{target.name}** successfully dodged the attack!'

        # calculating damage
        # damage = main class attribute + damage from weapon
        if source.creature_class == 'Warrior':  # TODO this should be taken from an enum
            base_damage = source.strength
        elif source.creature_class == 'Mage':
            base_damage = source.intelligence
        elif source.creature_class == 'Ranger':
            base_damage = source.dexterity
        else:
            base_damage = 1

        weapon_damage = 0
        if source.equipment.right_hand:
            weapon_damage += random.randint(*source.equipment.right_hand.damage)

        target.hp -= (base_damage + weapon_damage)

        # death of the creature
        if target.hp <= 0:
            target_name = target.name
            game.delete_entity(target.id)

            HandlerKillEnemy.handle_kill_enemy(game, target)

            return attack_status_message[:-3] + f' for ' \
                                                f'**`{base_damage + weapon_damage}`**  damage!\n\n' + \
                                                f'> 💀 **{target_name}** has been defeated!'

        return attack_status_message[:-3] + f' for **`{base_damage + weapon_damage}`** damage!\n\n' + \
                                            f'> **{target.name}** has `{target.hp}` HP left!'
