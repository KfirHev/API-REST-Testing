import os
import logging
import inspect
from logging.handlers import RotatingFileHandler
import jaydebeapi
import pytest


@pytest.mark.usefixtures('setup_browser')
class BaseClass:
    """Base class for web and database-related utilities in the test framework."""

    # --- Logger Setup ---
    @staticmethod
    def get_logger() -> logging.Logger:
        """Sets up and returns a logger instance for the test framework."""
        # Use the calling function's name as the logger's name
        logger_name = inspect.stack()[1][3]
        logger = logging.getLogger(logger_name)

        # Clear existing handlers to avoid duplicate logs
        if logger.hasHandlers():
            logger.handlers.clear()

        # Create 'Logs' directory if it doesn't exist
        os.makedirs('Logs', exist_ok=True)

        # Set up rotating file handler for log rotation
        file_handler = RotatingFileHandler(
            'Logs/logfile.log', maxBytes=10 * 1024 * 1024, backupCount=5
        )
        formatter = logging.Formatter('%(asctime)s :%(levelname)s : %(name)s : %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)
        return logger

    # --- Database Utilities ---
    HOST = "localhost"
    PORT = 9001
    DATABASE_NAME = "parabank"
    JDBC_URL = f"jdbc:hsqldb:hsql://{HOST}:{PORT}/{DATABASE_NAME}"
    JDBC_DRIVER = "org.hsqldb.jdbc.JDBCDriver"
    JDBC_DRIVER_PATH = "libs/hsqldb.jar"  # Path to the JAR inside the 'libs' folder
    USERNAME = "SA"  # Default user for HSQLDB
    PASSWORD = ""  # Default password for HSQLDB (empty by default)

    ACCOUNT_ID_LIST = []
    BASE_ACCOUNT_ID = None
    CUSTOMER_ID = None

    @classmethod
    def execute_db_query(cls, query):
        """
        Executes a SQL query on the database and retrieves the results.

        Args:
            query (str): The SQL query to execute.

        Returns:
            list: A list of results retrieved from the database based on the query.

        Raises:
            jaydebeapi.DatabaseError: If a database error occurs during query execution.
            Exception: If an unexpected error occurs during query execution.

        Notes:
            This method is intended to run any SQL query and is not limited to specific data retrievals.
            Ensure the query is valid for the database schema to avoid errors.
        """
        conn = None
        cursor = None
        log = cls.get_logger()

        try:
            # Establish the database connection
            conn = jaydebeapi.connect(
                cls.JDBC_DRIVER, cls.JDBC_URL,
                [cls.USERNAME, cls.PASSWORD],
                cls.JDBC_DRIVER_PATH
            )
            cursor = conn.cursor()

            # Execute the query and fetch all results
            cursor.execute(query)
            query_response = cursor.fetchall()

            log.info(f"DB query {query} results: {query_response}")
            return query_response

        except jaydebeapi.DatabaseError as e:
            log.error(f"Database error during query execution: {query}. Error: {e}")
            raise  # Re-raise the error after logging

        except Exception as e:
            log.error(f"Unexpected error during query execution: {query}. Error: {e}")
            raise  # Re-raise the error after logging

        finally:
            # Ensure resources are closed to avoid memory leaks
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    @classmethod
    def initialize_account_and_customer_ids(cls):
        """Initializes class attributes ACCOUNT_ID_LIST, BASE_ACCOUNT_ID, and CUSTOMER_ID."""
        log = cls.get_logger()  # Obtain a logger instance

        try:
            # Query to retrieve all account IDs greater than 13400
            account_id_query = "SELECT ID FROM PUBLIC.ACCOUNT WHERE ID > 13400"
            cls.ACCOUNT_ID_LIST = cls.execute_db_query(account_id_query)
            cls.BASE_ACCOUNT_ID = cls.ACCOUNT_ID_LIST[0][0]

            # Query to retrieve customer ID associated with BASE_ACCOUNT_ID
            customer_id_query = f"SELECT CUSTOMER_ID FROM PUBLIC.ACCOUNT WHERE ID = {cls.BASE_ACCOUNT_ID}"
            cls.CUSTOMER_ID = cls.execute_db_query(customer_id_query)
            log.info("Account and customer IDs initialized successfully.")
        except Exception as e:
            # Log the exception but don't raise it, to prevent test failures
            log.warning(
                f"Failed to initialize account and customer IDs. "
                f"Proceeding without these values. Error: {e}"
            )


# Initialize the account and customer IDs at class level
BaseClass.initialize_account_and_customer_ids()
print(f"**** This is the account ID full list :{BaseClass.ACCOUNT_ID_LIST}****")
