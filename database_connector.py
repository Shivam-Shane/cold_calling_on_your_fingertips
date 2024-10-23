import pypyodbc as odbc # type: ignore
from logger import logging
DRIVER_NAME = "ODBC Driver 17 for SQL Server"
SERVER_NAME = r"LAPTOP-UG5R2KF5\SQLEXPRESS"
DATABASE_NAME = "cold_calling_emails"
USERNAME = "cold_calling"  # Replace with the SQL Server username you created
PASSWORD = "cold@1234"  # Replace with the corresponding password

connection_string = f"""
DRIVER={{{DRIVER_NAME}}};
SERVER={SERVER_NAME};
DATABASE={DATABASE_NAME};
UID={USERNAME};
PWD={PASSWORD};
"""
def database_connector():
    try:
        connection = odbc.connect(connection_string)
        logging.info("connection to database connected successfully")
        return connection
    except odbc.Error as e:
        print("Error:", e)


if __name__=="__main__":
    database_connector()
