import mysql.connector
from mysql.connector import errorcode

# Declaring the global connection object.
connection = None


def database_connector():
    # Defining the connection parameters in a config dictionary
    global connection
    _config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "lab_2",
        "raise_on_warnings": True
        # Throws an exception when there is an error with other provided parameters such as when database does not
        # exist.
    }

    # _config["host"] = input("Enter your MySQL Hostname (default: localhost): ")
    # _config["user"] = input("Enter your MySQL Username (default: root): ")
    _config["password"] = input("Enter your MySQL Password: ")
    # _config["database"] = input("Enter the name of the MySQL Database: ")

    # Creating a connection to the MySQL server
    try:
        connection = mysql.connector.connect(**_config)
        print(f'Successfully Connected to the MYSQL Database "{_config["database"]}".')
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not Found! Generating the initial database")
            return generate_database(_config)
        else:
            print(f"Database Server Connection Failed!\nError: {err}")
            return 0


def generate_database(config):
    config.pop("raise_on_warnings")
    db_name = config.pop("database")
    connection = mysql.connector.connect(**config)  # No try catch block added since only error that reach here is
    # database doesn't exist.
    connection.cursor().execute(f'CREATE DATABASE {db_name}')
    print(f'Database Generated as "{db_name}".')
    # SQL Queries should
    # come here to create
    # the tables.
    print("Tables created successfully.")
    # Then comes the code for  populate the initial data from CSV files.
    print("Initial data populated successfully.")
    return connection
