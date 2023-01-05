from psycopg2 import connect
from dnd_bot.database.database_connection import DatabaseConnection

"""
Python script to initialize tables

    It is meant to be used when starting a fresh development environment
    This assumes the tables don't exist
"""

db_address, db_name, db_user, db_password, db_port = DatabaseConnection.__connection_get_authentication__()

print(
    f'DB table initialization: attempting connection to {db_name} database at {db_address}:{db_port} {db_user}:{db_password}')

connection = connect(database=db_name, user=db_user, password=db_password,
                     host=db_address, port=db_port)
cursor = connection.cursor()

print(f'DB table initialization: successfully connected')

cursor.execute(
    f'CREATE TABLE public."Game"(id_game serial NOT NULL,token character varying,id_host bigint,id_campaign bigint,game_state character varying,PRIMARY KEY (id_game),CONSTRAINT game_state_enum CHECK (game_state in (%s, %s, %s, %s, %s)));',
    ('LOBBY', 'STARTING', 'ACTIVE', 'INACTIVE', 'FINISHED'))
cursor.execute(f'ALTER TABLE IF EXISTS public."Game" OWNER to admin;')

cursor.execute(
    f'CREATE TABLE public."User"(id_user serial NOT NULL,id_game serial,discord_id bigint,PRIMARY KEY (id_user),FOREIGN KEY (id_game) REFERENCES public."Game" (id_game) MATCH SIMPLE ON UPDATE CASCADE ON DELETE CASCADE);'
)
cursor.execute(f'ALTER TABLE IF EXISTS public."User" OWNER to admin;')

connection.commit()

cursor.close()
connection.close()
