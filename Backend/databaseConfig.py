import csv
import os
import sys

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
        "database": "lb_2",
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
    global connection
    config.pop("raise_on_warnings")

    db_name = config.pop("database")
    connection = mysql.connector.connect(**config)  # No try catch block added since only error that reach here is
    # database doesn't exist.
    connection.cursor().execute(f'CREATE DATABASE {db_name}')
    connection.cursor().execute(f'USE {db_name}')  # Selecting the database for future operations.
    connection.cursor().close()
    print(f'Database Generated as "{db_name}".')
    # function below initialises tables.
    generate_tables_populate_data(connection)
    print("All the tables created and all initial data populated successfully.")
    return connection


def generate_tables_populate_data(dbconnection):
    # This function creates tables that should be in the database.
    def table_creator(table_name, columns):
        # SQL Queries should come here.
        try:
            dbconnection.cursor().execute(f"CREATE TABLE {table_name} ({columns});")
            print(f"Table {table_name} created successfully.")
        except mysql.connector.Error as errr:
            print(f"Table {table_name} creation failed!\nError: {errr}")
            sys.exit(1)

    table_files_list = os.listdir('dbInitialData')
    for file_name in table_files_list:
        if file_name.endswith('.csv'):  # Filters out non CSV files
            with open(f"dbInitialData/{file_name}", newline='') as csvfile:
                try:
                    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                    # Default EXCEL values provided for quote character and delimiter in csv.
                except csv.Error as err:
                    print(f"Error: {err}")
                first_line_list = next(
                    csvreader)  # First row of the csv file is the column names. This list will be later used after modification to get the column names to populate data.
                columns_with_type = ','.join(first_line_list)  # First row of the csv file is the column names.
                table_creator(file_name[0:-4],
                              columns_with_type)  # [0:-4]-Removes the .csv extension from the file name.

                # Preprocessing the first_line_list and converting it into a list of only "column names" without types.
                column_list = [string.split()[0] for string in first_line_list]
                # Populating the data into the table.
