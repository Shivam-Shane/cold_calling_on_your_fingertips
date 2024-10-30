from logger import logging
from database_connector import DatabaseConnector

class custom_email_content():
    def __init__(self):
        pass
    
    def get_email_content(self):
        cursor=None # Initialize cursor to None
        try:
            with DatabaseConnector() as conn:  # Ensure connection is open before use
                logging.info("starting to fetch email content from the database.")
                cursor = conn.cursor()  # Create a cursor object

                query = "SELECT TOP 1 * FROM dbo.cold_calling_details ORDER BY last_updated DESC;"
                cursor.execute(query)
                rows = cursor.fetchall()  # Fetch all rows

                # Get column names from the cursor description
                column_names = [column[0] for column in cursor.description]
                
                # Combine column names with their corresponding row values
                result = [dict(zip(column_names, row)) for row in rows]
                return result  # Return the last updated row

        except Exception as e:
            logging.error(f"Error occurred while fetching email content: {e}")
            raise e
        finally:
            if cursor:  # Close the cursor only if it was successfully created
                cursor.close()
                logging.debug("Cursor closed.")
            logging.debug("Database connection closed.")

    def update_email_details(self, your_name, phone_no, github_link, linkedin_link, portfolio_link, resume_path):
        logging.info("Updating email details in database.")
        cursor=None  # Initialize cursor to None
        try:
            with DatabaseConnector() as conn:  # Ensure connection is open before use
                logging.info("starting to fetch email content from the database.")
                cursor = conn.cursor()  # Create a cursor object
            
                # Check if the old phone number exists
                check_query = "SELECT 1 FROM dbo.cold_calling_details WHERE phone_no = ?"
                cursor.execute(check_query, (phone_no,))
                result = cursor.fetchone()

                if result:
                    # If the phone number exists, delete the old entry
                    delete_query = "DELETE FROM dbo.cold_calling_details WHERE phone_no = ?"
                    cursor.execute(delete_query, (phone_no,))

                # Insert the new entry
                insert_query = """
                INSERT INTO dbo.cold_calling_details (your_name, phone_no, github_link, linkedin_link, portfolio_link, resume_path)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                cursor.execute(insert_query, (your_name, phone_no, github_link, linkedin_link, portfolio_link, resume_path))
                conn.commit()

                logging.info("Email details updated successfully in database.")
        except Exception as e:
            logging.error(f"Error occurred while updating email details: {e}")
            if cursor:  # Check if cursor was created before trying to rollback
                conn.rollback()  # Rollback in case of error
            raise  # Rethrow the exception to propagate it further
        finally:
            if cursor:  # Close the cursor only if it was successfully created
                cursor.close()  # Ensure cursor is closed
                logging.debug("Cursor closed.")
            logging.debug("Database connection closed.")