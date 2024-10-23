from logger import logging
from database_connector import database_connector

class custom_email_content():
    def __init__(self):
        self.connection=database_connector()

    def get_email_content(self):
        try:
            cursor = self.connection.cursor() # Create a cursor object
            query="SELECT TOP 1 * FROM dbo.cold_calling_details ORDER BY last_updated DESC;"
            cursor.execute(query)

            rows=cursor.fetchall() # fetch all rows 
            # Get column names from the cursor description
            column_names = [column[0] for column in cursor.description]
            
            # Combine column names with their corresponding row values
            result = [dict(zip(column_names, row)) for row in rows]
            # return the last updated row
            return result


        except Exception as e:
            logging.error(f"Error occurred while fetching email content: {e}")
            raise Exception

    def update_email_details(self, your_name, phone_no, github_link, linkedin_link, portfolio_link, resume_path):
        try:
            cursor = self.connection.cursor()

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
            self.connection.commit()

            logging.info("Email details updated successfully.")
        except Exception as e:
            logging.error(f"Error occurred while updating email details: {e}")
            self.connection.rollback()  # Rollback in case of error
            raise e
        finally:
            cursor.close()
 