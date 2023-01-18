import copy
import json

from dnd_bot.logic.prototype.entities.hole import Hole
from dnd_bot.logic.prototype.entities.rock import Rock


class InitializeWorld:

    @staticmethod
    def load_entities(game, path):
        with open(path) as file:
            map_json = json.load(file)
            entities_json = map_json['map']['entities']

            # load entity types dict
            entity_types = map_json['entity_types']

            entities = []
            for y, row in enumerate(entities_json):
                entities_row = []
                for x, entity in enumerate(row):
                    if str(entity) not in entity_types.keys():
                        entities_row.append(None)

                    elif entity_types[str(entity)] == 'Rock':
                        entities_row.append(Rock(x=x, y=y))
                    elif entity_types[str(entity)] == 'Hole':
                        entities_row.append(Hole(x=x, y=y))
                entities.append(entities_row)

            game.entities = copy.deepcopy(entities)
