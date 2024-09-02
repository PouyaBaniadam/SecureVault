import sqlite3
from database.queries import Queries


class DatabaseUtils:
    def __init__(self, db_name):
        """
        Initialize the DatabaseUtils class.

        :param db_name: The name of the SQLite database file. Defaults to 'password_manager.db'.
        """
        self.db_name = db_name
        self.connection = None

    def connect(self):
        """
        Establish a connection to the SQLite database.
        """

        try:
            self.connection = sqlite3.connect(self.db_name)
            print(f"Connected to database: {self.db_name}")

        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def execute_query(self, query, params=(), fetch_one=False, fetch_all=False):
        """
        Execute a given SQL query with optional parameters.

        :param query: The SQL query to execute.
        :param params: A tuple of parameters to bind to the query.
        :param fetch_one: If True, fetch one record.
        :param fetch_all: If True, fetch all records.
        :return: Query result if fetching data, otherwise None.
        """

        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute(query, params)

                if fetch_one:
                    return cursor.fetchone()
                if fetch_all:
                    return cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Error executing query: {e}")

            return None

    def create_table(self, query):
        """
        Create a table in the database based on the provided SQL query.

        :param query: The SQL query to create a table.
        """

        self.execute_query(query)
        print("Table creation query executed.")

    def table_exists(self, table_name):
        """
        Check if a table exists in the database.

        :param table_name: The name of the table to check.
        :return: True if the table exists, False otherwise.
        """

        result = self.execute_query(Queries.does_table_exist, (table_name,), fetch_one=True)
        return result is not None

    def load_sql_to_dict(self):
        """
        Load all data from the 'passwords' table into a dictionary.

        :return: A dictionary containing all password records.
        """

        rows = self.execute_query(Queries.read_all_data_from_passwords, fetch_all=True)

        if rows:
            data_dict = {row[0]: {'label': row[1], 'password_hash': row[2], 'created_at': row[3]} for row in rows}
            return data_dict
        else:
            print("No data found.")
            return {}

    def close(self):
        """
        Close the connection to the SQLite database.
        """

        if self.connection:
            self.connection.close()
            print("Database connection closed.")
        else:
            print("Connection was already closed or never established.")
