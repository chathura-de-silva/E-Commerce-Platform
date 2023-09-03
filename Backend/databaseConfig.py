import mysql.connector


def database_connector():
    # Defining the connection parameters in a config dictionary
    _config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "lab_2",
        "raise_on_warnings" : True  #Thows an exception when there is an error with other provided parameters.
    }

    # config["host"] = input("Enter your MySQL Hostname (default: localhost): ")
    # config["user"] = input("Enter your MySQL Username (default: root): ")
    _config["password"] = input("Enter your MySQL Password: ")
    # config["database"] = input("Enter the name of the MySQL Database: ")

    # Creating a connection to the MySQL server
    try:
        connection = mysql.connector.connect(**_config)
        print("Successfully Connected to the MYSQL Database")
        return connection
    except mysql.connector.Error as err:
        print(f"Database Server Connection Failed!\nError: {err}")
        return 0
