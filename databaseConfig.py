import csv
import os
import sys
from colorama import init, Fore, Style
import mysql.connector
from mysql.connector import errorcode

init(autoreset=True)import csv
import os
import sys
from colorama import init, Fore, Style
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

init(autoreset=True)

# Load environment variables from the .env file
load_dotenv("dbInitialData/.env")


def database_connector():
    # Defining the connection parameters in a config dictionary
    _config = {
        "host": os.getenv("HOST") if os.getenv("HOST") else "localhost",
        "user": os.getenv("USER") if os.getenv("USER") else "root",
        "password": os.getenv("PASSWORD"),
        "database": os.getenv("DATABASE") if os.getenv("DATABASE") else "ecomdb",
        "raise_on_warnings": True
        # Throws an exception when there is an error with other provided parameters such as when database does not
        # exist.
    }

    try:
        connection = mysql.connector.connect(**_config)
        print(Style.BRIGHT + Fore.GREEN + f'Successfully Connected to the MYSQL Database "{_config["database"]}".')
        connection.close()
        return _config
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print(Style.BRIGHT + Fore.YELLOW + "Database not Found! Generating the initial database")
            generate_database(_config)
            return _config
        else:
            print(Style.BRIGHT + Fore.RED + f"Database Server Connection Failed!\nError: {err}")
            sys.exit(1)


def generate_database(config):
    config.pop("raise_on_warnings")
    db_name = config.pop("database")
    connection = mysql.connector.connect(**config)  # No try catch block added since only error that reach here is
    # database doesn't exist.
    connection.cursor().execute(f'CREATE DATABASE {db_name}')
    connection.cursor().execute(f'USE {db_name}')  # Selecting the database for future operations.
    connection.cursor().close()
    print(Style.BRIGHT + Fore.GREEN + f'Database Generated as "{db_name}".')
    # function below initialises tables.
    generate_tables_populate_data(connection)
    print(Style.BRIGHT + Fore.GREEN + "All the tables created and all initial data populated successfully.")
    return


def generate_tables_populate_data(dbconnection):
    # This function creates tables that should be in the database.
    def table_creator(table_name, columns):
        # SQL Queries should come here.
        try:
            dbconnection.cursor().execute(f"CREATE TABLE {table_name} ({columns});")
            dbconnection.cursor().close()
            print(Style.BRIGHT + Fore.LIGHTGREEN_EX + f"Table '{table_name}' created successfully.")
        except mysql.connector.Error as errr:
            print(f"CREATE TABLE {table_name} ({columns});")
            print(Style.BRIGHT + Fore.RED + f"Table '{table_name}' creation failed!\nError: {errr}")
            sys.exit(1)

    def data_populater():

        def row_sanitizer(csv_reader_row):
            for i in range(len(csv_reader_row)):
                try:  # Had to use a try catch block to check whether string contains a float.
                    if csv_reader_row[i] == 'NULL':  # Adding support for NULL values in fields such as integers.
                        continue
                    float(csv_reader_row[i].replace(" ", ""))  # If the cell is a float (or an integer), it will not
                    # raise an exception. Instead, will jump to the next for loop iteration
                except ValueError:
                    csv_reader_row[i] = f'''"{csv_reader_row[i]}"'''
            return csv_reader_row

        for row in csvreader:
            try:
                dbconnection.cursor().execute(
                    f"INSERT INTO {file_name[0:-4]} ({','.join(column_list)}) VALUES ({','.join(row_sanitizer(row))})")
                print(Style.BRIGHT + Fore.BLUE + f"Record '{row[0]}...'Inserted in to '{file_name}' table")
            except mysql.connector.Error as errr:
                print(Style.BRIGHT + Fore.RED + f"Error: {errr}")
                sys.exit(1)
        print('\n')

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
                    csvreader)  # First row of the csv file is the column names. This list will be later used after
                # modification to get the column names to populate data.
                columns_with_type = ','.join(first_line_list)  # First row of the csv file is the column names.
                table_creator(file_name[0:-4],
                              columns_with_type)  # [0:-4]-Removes the .csv extension from the file name.

                # Preprocessing the first_line_list and converting it into a list of only "column names" without types.
                column_list = [string.split()[0] for string in first_line_list]
                # Populating the data into the table.
                data_populater()

            dbconnection.commit()
        dbconnection.cursor().close()



def database_connector():
    # Defining the connection parameters in a config dictionary
    _config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "EcomDB",
        "raise_on_warnings": True
        # Throws an exception when there is an error with other provided parameters such as when database does not
        # exist.
    }

    # _config["host"] = input(Style.BRIGHT + Fore.MAGENTA+"Enter your MySQL Hostname (default: localhost): ")
    # _config["user"] = input(Style.BRIGHT + Fore.MAGENTA+"Enter your MySQL Username (default: root): ")
    _config["password"] = input(Style.BRIGHT + Fore.MAGENTA + "Enter your MySQL Password: ")
    # _config["database"] = input(Style.BRIGHT + Fore.MAGENTA+"Enter the name of the MySQL Database: ")

    # Creating a connection to the MySQL server
    try:
        connection = mysql.connector.connect(**_config)
        print(Style.BRIGHT + Fore.GREEN + f'Successfully Connected to the MYSQL Database "{_config["database"]}".')
        connection.close()
        return _config
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print(Style.BRIGHT + Fore.YELLOW + "Database not Found! Generating the initial database")
            generate_database(_config)
            return _config
        else:
            print(Style.BRIGHT + Fore.RED + f"Database Server Connection Failed!\nError: {err}")
            return 0


def generate_database(config):
    config.pop("raise_on_warnings")
    db_name = config.pop("database")
    connection = mysql.connector.connect(**config)  # No try catch block added since only error that reach here is
    # database doesn't exist.
    connection.cursor().execute(f'CREATE DATABASE {db_name}')
    connection.cursor().execute(f'USE {db_name}')  # Selecting the database for future operations.
    connection.cursor().close()
    print(Style.BRIGHT + Fore.GREEN + f'Database Generated as "{db_name}".')
    # function below initialises tables.
    generate_tables_populate_data(connection)
    print(Style.BRIGHT + Fore.GREEN + "All the tables created and all initial data populated successfully.")
    return


def generate_tables_populate_data(dbconnection):
    # This function creates tables that should be in the database.
    def table_creator(table_name, columns):
        # SQL Queries should come here.
        try:
            dbconnection.cursor().execute(f"CREATE TABLE {table_name} ({columns});")
            dbconnection.cursor().close()
            print(Style.BRIGHT + Fore.LIGHTGREEN_EX + f"Table '{table_name}' created successfully.")
        except mysql.connector.Error as errr:
            print(f"CREATE TABLE {table_name} ({columns});")
            print(Style.BRIGHT + Fore.RED + f"Table '{table_name}' creation failed!\nError: {errr}")
            sys.exit(1)

    def data_populater():

        def row_sanitizer(csv_reader_row):
            for i in range(len(csv_reader_row)):
                try:  # Had to use a try catch block to check whether string contains a float.
                    if csv_reader_row[i] == 'NULL':  # Adding support for NULL values in fields such as integers.
                        continue
                    float(csv_reader_row[i].replace(" ", ""))  # If the cell is a float (or an integer), it will not
                    # raise an exception. Instead, will jump to the next for loop iteration
                except ValueError:
                    csv_reader_row[i] = f'''"{csv_reader_row[i]}"'''
            return csv_reader_row

        for row in csvreader:
            try:
                dbconnection.cursor().execute(
                    f"INSERT INTO {file_name[0:-4]} ({','.join(column_list)}) VALUES ({','.join(row_sanitizer(row))})")
                print(Style.BRIGHT + Fore.BLUE + f"Record '{row[0]}...'Inserted in to '{file_name}' table")
            except mysql.connector.Error as errr:
                print(Style.BRIGHT + Fore.RED + f"Error: {errr}")
                sys.exit(1)
        print('\n')

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
                    csvreader)  # First row of the csv file is the column names. This list will be later used after
                # modification to get the column names to populate data.
                columns_with_type = ','.join(first_line_list)  # First row of the csv file is the column names.
                table_creator(file_name[0:-4],
                              columns_with_type)  # [0:-4]-Removes the .csv extension from the file name.

                # Preprocessing the first_line_list and converting it into a list of only "column names" without types.
                column_list = [string.split()[0] for string in first_line_list]
                # Populating the data into the table.
                data_populater()

            dbconnection.commit()
        dbconnection.cursor().close()