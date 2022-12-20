import psycopg2

from psycopg2 import connect

class DatabaseConnection:

    def __init__(self):
        db_name = 'postgres'
        db_user = 'admin'
        db_password = 'admin'

        connection = connect(database=db_name, user=db_user, password=db_password, host='172.18.0.2')

        cur = connection.cursor()


        cur.execute('DROP TABLE test')
        cur.execute('CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);')

        cur.execute('INSERT INTO test (num, data) VALUES (%s, %s);', (123456, 'test_test'))
        cur.execute('INSERT INTO test (num, data) VALUES (%s, %s);', (145, 'second_record'))

        cur.execute('SELECT * FROM test;')
        print(cur.fetchall())

        connection.commit()

        cur.close()
        connection.close()




test = DatabaseConnection()
