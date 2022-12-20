import psycopg2

from psycopg2 import connect


class DatabaseConnection:
    connection = None
    cursor = None

    @staticmethod
    def connection_establish():
        db_name = 'postgres'
        db_user = 'admin'
        db_password = 'admin'

        DatabaseConnection.connection = connect(database=db_name, user=db_user, password=db_password, host='172.18.0.2')

        DatabaseConnection.cursor = DatabaseConnection.connection.cursor()

    @staticmethod
    def connection_close():
        DatabaseConnection.cursor.close()
        DatabaseConnection.connection.close()


test = DatabaseConnection()
