import pypyodbc as odbc  # type: ignore
from logger import logging
import os
from dotenv import load_dotenv
class DatabaseConnector:
    """
    It maintains a single instance of the database connection across the application
    """
    _connection = None #private class-level, indicating that no connection has been established yet
    load_dotenv()
    @classmethod
    def _connect(cls):    #cls: Refers to the class itself, allowing access to class variables and methods
        if cls._connection is None : #connection already exists cls._connection, 
            try:
                DRIVER_NAME = os.getenv("DRIVER_NAME")
                SERVER_NAME = os.getenv("SERVER_NAME")
                DATABASE_NAME = os.getenv("DATABASE_NAME")
                DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
                DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

                connection_string = f"""
                DRIVER={DRIVER_NAME};
                SERVER={SERVER_NAME};
                DATABASE={DATABASE_NAME};
                UID={DATABASE_USERNAME};
                PWD={DATABASE_PASSWORD};
                """
                cls._connection = odbc.connect(connection_string)
                logging.info("Database connection established.")
            except odbc.Error as e:
                logging.error(f"Failed to connect to database: {e}")
                raise
        return cls._connection

    def __enter__(self):
        """This method is part of the context management protocol,
          allowing the use of the with statement. It calls the _connect()
            method to establish and return the database connection when entering the context."""
        return self._connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """This method is also part of the context management protocol and is executed
          when exiting the with block.
          In this implementation, it does nothing (indicated by the pass statement), 
          leaving the connection open across instances"""
        pass  # Leave the connection open across instances

    @classmethod
    def close(cls):
        if cls._connection:
            cls._connection.close()
            cls._connection = None
            logging.info("Database connection closed.")
