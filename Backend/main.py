import databaseConfig

connection = databaseConfig.database_connector()
if connection:
    # Creating a cursor object
    cursor = connection.cursor()
    # SQL Queries should come here.

    cursor.close()
    connection.close()
