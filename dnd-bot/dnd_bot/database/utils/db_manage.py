import requests as requests
from psycopg2 import connect
from dnd_bot.database.database_connection import DatabaseConnection

"""
Python script to initialize tables

    It is meant to be used when starting a fresh development environment
    This assumes the tables don't exist
"""

db_address, db_name, db_user, db_password, db_port = DatabaseConnection.__connection_get_authentication__()

print(f'DB: attempting connection to {db_name} database at {db_address}:{db_port}')

connection = connect(database=db_name, user=db_user, password=db_password[-1],
                     host=db_address, port=db_port)
cursor = connection.cursor()

print('DB: successfully connected')

choice = input("Do you want to CREATE, CLEAR, or DROP the tables? ")

if choice == "CREATE":
    queries = requests.get("https://raw.githubusercontent.com/esoviscode/database/main/scripts/create_tables.sql")\
        .content.decode("UTF8")
    cursor.execute(queries)
    print('Tables created.')

elif choice == "CLEAR":
    queries = requests.get("https://raw.githubusercontent.com/esoviscode/database/main/scripts/clear_tables.sql")\
        .content.decode("UTF8")
    cursor.execute(queries)
    print('Tables cleared.')

elif choice == "DROP":
    queries = requests.get("https://raw.githubusercontent.com/esoviscode/database/main/scripts/drop_tables.sql")\
        .content.decode("UTF8")
    cursor.execute(queries)
    print('Tables deleted.')

else:
    print('Aborting...')

connection.commit()
cursor.close()
connection.close()
