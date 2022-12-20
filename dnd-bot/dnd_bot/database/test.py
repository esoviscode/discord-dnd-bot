# debug
from dnd_bot.database.database_connection import DatabaseConnection

DatabaseConnection.connection_establish()

game = DatabaseConnection.find_game_by_token('7777')
print(game)

DatabaseConnection.connection_close()
