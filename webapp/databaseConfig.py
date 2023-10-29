import csv
import os
import sys
from colorama import init, Fore, Style
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash,check_password_hash

init(autoreset=True)
dotenv_path = os.path.join(os.path.dirname(__file__), 'dbInitialData', '.env')
load_dotenv(dotenv_path)


def get_db_config_data():
    _config = {
        "host": os.getenv("HOST") if os.getenv("HOST") else "localhost",
        "user": os.getenv("USER") if os.getenv("USER") else "root",
        "password": os.getenv("PASSWORD"),
        "database": os.getenv("DATABASE") if os.getenv("DATABASE") else "ecomdb",
        "raise_on_warnings": True
        # Throws an exception when there is an error with other provided parameters such as when database does not
        # exist.
    }
    return _config


def database_connector():
    # Defining the connection parameters in a config dictionary
    _config = get_db_config_data()

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
            sys.exit()


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

    def relationship_creator():
        try:
            with open('./webapp/dbInitialData/database_relations.sql', 'r') as sql_file:
                queries = sql_file.read().split('\n\n')
                # print(queries) # Uncomment for debugging.
            for query in queries:
                dbconnection.cursor().execute(query)
            print(Style.BRIGHT + Fore.LIGHTGREEN_EX + f"Table relationships created successfully.")
        except mysql.connector.Error as errr:
            print(Style.BRIGHT + Fore.RED + f"Table relationship creation failed!\nError: {errr}")
            sys.exit(1)
        except IOError as error:
            print(Style.BRIGHT + Fore.RED + f"Table relationship creation failed!\nError: {error}")
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
                    if password_column_index is not None and i == password_column_index:
                       csv_reader_row[i] = f'''"{generate_password_hash(csv_reader_row[i], method='pbkdf2:sha256')}"'''
                    else:
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

    table_files_list = os.listdir('./webapp/dbInitialData')
    for file_name in table_files_list:
        if file_name.endswith('.csv'):  # Filters out non CSV files
            with open(f"./webapp/dbInitialData/{file_name}", newline='') as csvfile:
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
                # Find the index of the password column
                #
                #
                #
                password_column_index = next((i for i, col in enumerate(column_list) if col.lower() == 'password'), None)
                # Populating the data into the table.
                data_populater()
    relationship_creator()
    dbconnection.commit()
    dbconnection.cursor().close()
