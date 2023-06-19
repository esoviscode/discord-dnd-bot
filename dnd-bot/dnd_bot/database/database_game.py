from sqlite3 import ProgrammingError

from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseGame:

    @staticmethod
    def add_game(token: str = '', id_host: int = None, game_state: str = 'LOBBY', campaign_name: str = '',
                 active_creature: int = None) -> int | None:
        """start game and add game to database
        :param token: lobby/game token (5 digit password)
        :param id_host: discord id of host
        :param game_state: string enum, initial value of added game is 'LOBBY'
        :param campaign_name: campaign  name
        :param active_creature: active creature id
        :return:
            on success: game id, on failure: None
        """
        return DatabaseConnection.add_to_db('INSERT INTO public."Game" (token, id_host, game_state, campaign_name, active_creature)'
                                            'VALUES (%s, %s, %s, %s, %s)', (token, id_host, game_state, campaign_name, active_creature),
                                            "game")

    @staticmethod
    def start_game(id_game: int) -> None:
        """starts game
        :param id_game: database game id
        """
        DatabaseGame.update_game_state(id_game, 'ACTIVE')

    @staticmethod
    def update_game_state(id_game: int, game_state: str) -> None:
        """updates game state on the one provided
        """
        DatabaseConnection.update_object_in_db('UPDATE public."Game" SET game_state = (%s) WHERE id_game = (%s)',
                                               (game_state, id_game), "Game")

    @staticmethod
    def update_game_active_creature(id_game: int, active_creature: int) -> None:
        """updates active_creature id"""
        DatabaseConnection.update_object_in_db('UPDATE public."Game" SET active_creature = (%s) WHERE id_game = (%s)',
                                               (active_creature, id_game), "Game")

    @staticmethod
    def get_all_game_tokens():
        """returns all tokens currently existing in the database
        """
        DatabaseConnection.cursor.execute(f'SELECT token FROM public."Game"')
        tokens = DatabaseConnection.cursor.fetchall()
        DatabaseConnection.connection.commit()

        return [x[0] for x in tokens]

    @staticmethod
    def get_id_game_from_game_token(token: str) -> int | None:
        """returns database game id based on the token, None if the query fails
        """
        DatabaseConnection.cursor.execute(f'SELECT id_game FROM public."Game" WHERE token = (%s)', (token,))
        ret = DatabaseConnection.cursor.fetchone()
        DatabaseConnection.connection.commit()

        if ret is None:
            return None

        game_id = ret[0]

        return game_id

    @staticmethod
    def get_game_token_from_id_game(id_game: int) -> str | None:
        """returns game token based on database game id, None if the query fails
        """
        DatabaseConnection.cursor.execute(f'SELECT token FROM public."Game" WHERE id_game = (%s)', (id_game,))
        game_token = DatabaseConnection.cursor.fetchone()
        DatabaseConnection.connection.commit()

        if game_token is None:
            return None

        return game_token[0]

    @staticmethod
    def find_game_by_token(token: str) -> dict | None:
        """find game by token/password
        :param token: game token/password to find the game by
        :return: on success: dictionary containing game data - it's keys: 'id game' - database game id, 'token' - game token, 'id_host' -
        discord host id, 'id_campaign' - campaign id, 'game_state' - string enum, 'players' - list of players
        """

        DatabaseConnection.cursor.execute(f'SELECT * FROM public."Game" WHERE token = %s AND game_state != %s',
                                          (token, 'FINISHED'))
        game_tuple = DatabaseConnection.cursor.fetchone()

        if not game_tuple:
            return None

        DatabaseConnection.cursor.execute(f'SELECT * FROM public."User" WHERE id_game = {game_tuple[0]}')
        users_tuples = DatabaseConnection.cursor.fetchall()

        users = [{'id_user': user_tuple[0], 'id_game': user_tuple[1], 'discord_id': user_tuple[2]}
                 for user_tuple in users_tuples]

        return {'id_game': game_tuple[0], 'token': game_tuple[1], 'id_host': game_tuple[2],
                'game_state': game_tuple[3], 'campaign_name': game_tuple[4], 'players': users}

    @staticmethod
    def get_game(id_game: int) -> dict | None:
        query = f'SELECT *  FROM public."Game" WHERE id_game = (%s)'
        db_t = DatabaseConnection.get_object_from_db(query, (id_game,), "Game")
        return {'id_game': db_t[0], 'token': db_t[1], 'id_host': db_t[2], 'game_state': db_t[3],
                'campaign_name': db_t[4], 'active_creature': db_t[5]}
