from sqlite3 import ProgrammingError

from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseGame:

    @staticmethod
    def add_game(token: str, id_host: int, game_state: str, campaign_name: str) -> int | None:
        """start game and add game to database
        :param token: lobby/game token (5 digit password)
        :param id_host: discord id of host
        :param game_state: string enum, initial value of added game is 'LOBBY'
        :param campaign_name: campaign  name
        :return:
            on success: game id, on failure: None
        """

        DatabaseConnection.cursor.execute(
            'INSERT INTO public."Game" (token, id_host, game_state, campaign_name) VALUES '
            '(%s, %s, %s, %s)',
            (token, id_host, game_state, campaign_name))
        DatabaseConnection.cursor.execute('SELECT LASTVAL()')

        try:
            game_id = DatabaseConnection.cursor.fetchone()[0]
        except ProgrammingError as err:
            print(f"db: error adding game {err}")
            return None

        DatabaseConnection.connection.commit()
        return game_id

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
        DatabaseConnection.cursor.execute('UPDATE public."Game" SET game_state = (%s) WHERE id_game = (%s)',
                                          (game_state, id_game))

        DatabaseConnection.connection.commit()

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
        game_id = DatabaseConnection.cursor.fetchone()
        DatabaseConnection.connection.commit()

        if not game_id:
            return None

        return game_id

    @staticmethod
    def get_game_token_from_id_game(id_game: int) -> str | None:
        """returns game token based on database game id, None if the query fails
        """
        DatabaseConnection.cursor.execute(f'SELECT token FROM public."Game" WHERE id_game = (%s)', (id_game,))
        game_token = DatabaseConnection.cursor.fetchone()
        DatabaseConnection.connection.commit()

        if not game_token:
            return None

        return game_token
