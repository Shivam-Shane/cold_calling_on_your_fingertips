from logger import logging
from database_connector import DatabaseConnector

class hc_dashboard_content():
    def __init__(self):
        pass

    def get_dashboard_content(self):
        cursor=None # Initialize cursor to None
        try:
            with DatabaseConnector() as conn:  # Ensure connection is open before use
                logging.info("Starting to fetch email content from the database.")
                cursor = conn.cursor()  # Create a cursor object

                query = "SELECT subject,recipients,company_name,created_at FROM dbo.sent_data_details ORDER BY created_at DESC;"
                cursor.execute(query)
                rows = cursor.fetchall()  # Fetch all rows

                # Get column names from the cursor description
                column_names = [column[0] for column in cursor.description]
                # Combine column names with their corresponding row values
                result = [dict(zip(column_names, row)) for row in rows]
                print(result,type(result)) #
                return result  # centric results
            
        except Exception as e:
            logging.error(f"Error occurred while fetching email content: {e}")
            raise e