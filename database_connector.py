import pypyodbc as odbc  # type: ignore
from logger import logging
from utility import read_yaml

# Global variable to store the connection
_connection = None

def database_connector():
    global _connection
    if _connection is None:  # If no connection exists, create a new one
        try:
            config=read_yaml("config.yaml") # reading database connection details from config.yaml

            DRIVER_NAME=config.get("DRIVER_NAME") 
            SERVER_NAME=config.get("SERVER_NAME")
            DATABASE_NAME=config.get("DATABASE_NAME")
            USERNAME=config.get("USERNAME")
            PASSWORD=config.get("PASSWORD")
            # Creating the connection string using the provided details
            connection_string = f"""
            DRIVER={{{DRIVER_NAME}}};
            SERVER={SERVER_NAME};
            DATABASE={DATABASE_NAME};
            UID={USERNAME};
            PWD={PASSWORD};
            """
            logging.debug("Connection string: %s", connection_string)
            _connection = odbc.connect(connection_string)
            logging.info("Connection to database established successfully.")
        except odbc.Error as e:
            logging.error(f"Failed to connect to database: {e}")
            raise
    else:
        logging.info("Reusing the existing database connection.")
    return _connection
