import databaseConfig

connection = databaseConfig.database_connector()  # Should call this function before using the "connection" anywhere
# in the project. Hence called at start.
if connection:
    # Creating a cursor object
    cursor = connection.cursor()
    # SQL Queries should come here.

    cursor.close()
    connection.close()
