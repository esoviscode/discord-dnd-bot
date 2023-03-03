import os
from sqlite3 import ProgrammingError

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


