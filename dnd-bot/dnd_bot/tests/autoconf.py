import psycopg2
from pytest_postgresql import factories

from dnd_bot.database.database_connection import DatabaseConnection


def load_database(**kwargs):
    db_connection = psycopg2.connect(**kwargs)
    with db_connection.cursor() as cur:
        query = open('create_tables.sql')
        cur.execute(query.read())
        db_connection.commit()


def database_fixture(db_name):
    postgresql_in_docker = factories.postgresql_noproc(host='172.20.0.2', password='admin', user='admin',
                                                       load=[load_database], dbname=db_name)
    postgresql = factories.postgresql('postgresql_in_docker', dbname=db_name)

    return postgresql, postgresql_in_docker
