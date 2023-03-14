import psycopg2
from pytest_postgresql import factories


def load_database(**kwargs):
    db_connection = psycopg2.connect(**kwargs)
    with db_connection.cursor() as cur:
        query_create_tables = open('create_tables.sql')
        cur.execute(query_create_tables.read())
        query_populate_tables = open('populate_tables.sql')
        cur.execute(query_populate_tables.read())
        db_connection.commit()


def database_fixture(db_name):
    postgresql_in_docker = factories.postgresql_noproc(host='localhost', password='admin', user='admin',
                                                       load=[load_database], dbname=db_name)
    postgresql = factories.postgresql('postgresql_in_docker', dbname=db_name)

    return postgresql, postgresql_in_docker
