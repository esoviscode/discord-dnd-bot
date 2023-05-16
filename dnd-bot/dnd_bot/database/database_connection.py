import os
from sqlite3 import ProgrammingError
from typing import List

from psycopg2 import connect


class DatabaseConnection:
    connection = None
    cursor = None

    @staticmethod
    def connection_establish():
        """ establishes connection with the database using the provided ip address, credentials and port
        """
        db_address, db_name, db_user, db_passwords, db_port = DatabaseConnection.__connection_get_authentication__()

        print(f'db: attempting connection to {db_name} database at {db_address}:{db_port}')

        DatabaseConnection.connection = connect(database=db_name, user=db_user, password=db_passwords.pop(),
                                                host=db_address, port=db_port)

        # erase password in memory upon using it
        db_passwords.clear()

        DatabaseConnection.cursor = DatabaseConnection.connection.cursor()
        print(f'db: successfully connected')

    @staticmethod
    def __connection_get_authentication__():
        """extracts database credentials and others from environment variables passed to the app
        """
        passwords = []
        address = os.getenv('DB_ADDRESS')
        name = os.getenv('DB_NAME')
        user = os.getenv('DB_USER')
        passwords.append(os.getenv('DB_PASSWORD'))
        port = os.getenv('DB_PORT')

        if not user:
            user = 'admin'
        if passwords[0] is None:
            passwords.append('admin')
        if not port:
            port = 5432

        return address, name, user, passwords, port

    @staticmethod
    def connection_close():
        """closes connection to the database
        """
        DatabaseConnection.cursor.close()
        DatabaseConnection.connection.close()

    @staticmethod
    def execute_query(query: str):
        """deprecated - executes query as a string
        """
        DatabaseConnection.cursor.execute(query)
        DatabaseConnection.connection.commit()

    @staticmethod
    def add_to_db(query: str = "", parameters: tuple = None, element_name: str = "element") -> int | None:
        """
        adds an element to the database and return its id
        :param query: the SQL query to be executed
        :param parameters: the parameters to be passed to the query
        :param element_name: the name of the element being added, for more informative errors
        :return: the id of the added element if successful, or None if an error occurred.
        """
        DatabaseConnection.cursor.execute(query, parameters)
        DatabaseConnection.cursor.execute('SELECT LASTVAL()')

        try:
            id = DatabaseConnection.cursor.fetchone()[0]
        except ProgrammingError as err:
            print(f"db: error adding {element_name} {err}")
            return None

        DatabaseConnection.connection.commit()
        return id

    @staticmethod
    def add_multiple_to_db(queries: List[str], parameters_list: List[tuple]) -> List[int]:
        """
        add multiple elements to the database in bulk and return a list of their ids (in the order that the element
        were provided). This method is faster than adding elements individually
        :param queries: list of queries to be executed
        :param parameters_list: list of parameter tuples, where each corresponds to a query in 'queries'
        :return: list of ids of the added elements
        """
        ids = []

        for query, parameters in list(zip(queries, parameters_list)):
            DatabaseConnection.cursor.execute(query, parameters)
            DatabaseConnection.cursor.execute('SELECT LASTVAL()')

            try:
                id = DatabaseConnection.cursor.fetchone()[0]
                ids.append(id)
            except ProgrammingError as err:
                print(f"db: error adding element {err}")

        DatabaseConnection.connection.commit()
        return ids

    @staticmethod
    def get_object_from_db(query: str = '', parameters: tuple = None, element_name: str = '') -> tuple | None:
        DatabaseConnection.cursor.execute(query, parameters)
        obj = DatabaseConnection.cursor.fetchone()

        if not obj:
            print(f"db: error getting {element_name}")
            return None

        DatabaseConnection.connection.commit()
        return obj

    @staticmethod
    def get_multiple_objects_from_db(query: str = '', parameters: tuple = None, element_name: str = '') -> list | None:
        """returns list of tuples representing a db object"""
        DatabaseConnection.cursor.execute(query, parameters)
        objs = DatabaseConnection.cursor.fetchall()

        if not objs:
            print(f"db: error getting multiple {element_name}")
            return None

        DatabaseConnection.connection.commit()
        return objs

    @staticmethod
    def update_object_in_db(query: str = '', parameters: tuple = None, element_name: str = '') -> None:
        try:
            DatabaseConnection.cursor.execute(query, parameters)
        except ProgrammingError as err:
            print(f'db: error updating {element_name} {err}')

        DatabaseConnection.connection.commit()
