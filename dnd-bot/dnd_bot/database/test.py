# debug
from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_enums import DatabaseEnums
from dnd_bot.database.database_interface import DatabaseInterface

DatabaseConnection.connection_establish()
DatabaseConnection.add_game(67, 'test', 123, 456, 'LOBBY')
DatabaseConnection.connection_close()
