import os
import sys
# Adding the project root directory to the PYTHONPATH for imports from upper level
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_path)

# setting PYTHONPATH so it can access the module outside of CWD
from logger import logging
from django.conf import settings
import pypyodbc as odbc
from django.contrib import messages
from django.shortcuts import render, redirect
from gmail_connector import GmailFetcher
from gmail_preview_content import preview_mail
from database_connector import DatabaseConnector
from customize_email_content import custom_email_content
from hc_dashboard_content_fetcher import hc_dashboard_content
from utility import update_env
from datetime import datetime

get_email_details_object=custom_email_content()
hc_content_object=hc_dashboard_content()
GM=GmailFetcher()

def index(request):
    logging.debug("Rendeding main page of site")
    return render(request, 'index.html')

def preview_email(request):
    logging.debug("Rendering preview page of email")
    if request.method == 'POST':
        recipient_name=request.POST['recipient_name']
        mail_subject = request.POST['subject']
        recipients = request.POST['recipients']
        company_name = request.POST['company_name']
        job_post_url = request.POST['job_post_url']
        
        # Check if a resume was uploaded
        resume_path = None

        if 'resume' in request.FILES:
            resume = request.FILES['resume']
            logging.info(f"Uploading resume {resume} at location {settings.MEDIA_ROOT}")
            resume_path = os.path.join(settings.MEDIA_ROOT, resume.name)
            with open(resume_path, 'wb+') as destination:
                for chunk in resume.chunks():
                    destination.write(chunk)

        else:
            # Use the existing resume path from the session if no new resume is uploaded
            logging.info("No new resume uploaded, using existing resume path if available")
            resume_path = request.session.get('resume_path')
            if not resume_path:
                logging.error("No resume path found in session.")
                
    
        if 'resume' in request.FILES or resume_path:
            request.session['resume_path'] = resume_path

        email_content=preview_mail(recipient_name,company_name,job_post_url,resume_path)
        request.session['body']=email_content
        # Pass data to preview template
        context = {
            'subject': mail_subject,
            'recipients': recipients,
            'email_content': email_content,
            'recipient_name': recipient_name,  # Pass this to the context
            'company_name': company_name,
            'resume_path': resume_path,  # Pass the file path to the template

        }
        logging.debug("Ending preview page of email")
        return render(request, 'preview.html', context)

def send_email(request):
    if request.method == 'POST':
        try: 
            logging.debug(f"Sending email, Sent mail button called")
            subject = request.POST['subject']
            recipients = request.POST['recipients'].split(',')
            recipient_name=request.POST['recipient_name']        
            company_name = request.POST['company_name']
            
            # Get the resume path from the session
            resume_path = request.session.get('resume_path')
            logging.info(f"Retrieved Resume path from session: {resume_path}")
            if resume_path==None:
                messages.error(request, f'No resume found in session please upload one.! ')
                logging.debug("No resume found in session, returning to home page.")
                return redirect('index')
            body=request.session.get('body')

            GM.email_sender(recipients,subject, body,attachments=resume_path)
            messages.success(request, f'Mail Sent successfully! at {datetime.now()}')
            # Save the email details in the database
            try:
                cursor=None # Initialize cursor to None
                with DatabaseConnector() as conn:
                    cursor = conn.cursor()

                    # Insert the email details into the database
                    insert_query = """
                    INSERT INTO dbo.sent_data_details (subject, recipients, recipient_name, company_name,  body, resume_path)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """
                    cursor.execute(insert_query, (subject, ', '.join(recipients), recipient_name, company_name,  body, resume_path))
                    conn.commit()
                    logging.info("Email details saved to database.")
            except odbc.Error as e:
                logging.error("Error saving to database: %s", e)
                messages.error(request, f'An error occurred while saving to database: {str(e)}')
                if cursor:  # Check if cursor was created before trying to rollback
                    conn.rollback()  # Rollback in case of error
                raise  # Rethrow the exception to propagate it further
            finally:
                if cursor:  # Close the cursor only if it was successfully created
                    cursor.close()  # Ensure cursor is closed
                logging.debug("Cursor closed.")
            logging.debug("Send mail closed.")

        except Exception as e:
            logging.error("Error sending mail: %s", e)
            messages.error(request, f'An error occurred while sending mail: {str(e)}')
            return redirect('index')
        
        return redirect('index')

def customize_email(request):
    if request.method == 'POST':
        try:
            logging.debug("Updating email details")
            your_name = request.POST['your_name']
            phone_no = request.POST['phone_no']
            github_link = request.POST['github_link']        
            linkedin_link = request.POST['linkedin_link']
            portfolio_link = request.POST['portfolio_link']
            # Get the resume path from the session
            resume_path = request.session.get('resume_path')
 
            if not your_name and not phone_no:
                messages.error(request, "Name and Phone No can't be empty!")
            else:
                if your_name=="None" or phone_no=="None":
                    messages.error(request, "Name Or Phone can't be None!")
                else:
                    # Update the email details
                    get_email_details_object.update_email_details(your_name, phone_no, github_link, linkedin_link, portfolio_link, resume_path)
                    messages.success(request, 'Details updated successfully!')
                    # Redirect to the same view after saving to refresh the data
                    return redirect('customize_email')
        except Exception as e:
            logging.error(f"Error occurred while updating email details: {e}")
            messages.error(request, "Failed to update email details.")
            return redirect('customize_email')

    # If not POST, fetch the current details
    result = get_email_details_object.get_email_content()
    logging.info(f"Retrieved email details: {result}")
    if not result:
        logging.info("No email details found in the database.")
        context = {
            "your_name": "None",
            "phone_no": "None",
            "github_link": "None",
            "linkedin_link": "None",
            "portfolio_link": "None",
            "resume_path": "None",
            "last_updated": "None"
        }
    else:
        # Prepare the context with the latest data
        context = {
            "your_name": result[0]['your_name'],
            "phone_no": result[0]['phone_no'],
            "github_link": result[0]['github_link'],
            "linkedin_link": result[0]['linkedin_link'],
            "portfolio_link": result[0]['portfolio_link'],
            "resume_path": result[0]['resume_path'],
            "last_updated": result[0]['last_updated']
        }

    # Render the template with the context
    return render(request, 'customize_email.html', context)
def mask_sensitive(value, show_chars=4):
    """Mask sensitive data, showing only last few characters"""
    if not value:
        return ""
    return "*" * (len(value) - show_chars) + value[-show_chars:]

def customize_secrets(request):
    if request.method == 'POST':
        try:
            SENDER_NAME = request.POST['SENDER_NAME']
            SMTP_USERNAME = request.POST['SMTP_USERNAME']
            SMTP_PASSWORD = request.POST['SMTP_PASSWORD']        
            DRIVER_NAME = request.POST['DRIVER_NAME']
            SERVER_NAME = request.POST['SERVER_NAME']
            DATABASE_NAME = request.POST['DATABASE_NAME']
            USERNAME = request.POST['USERNAME']
            PASSWORD = request.POST['PASSWORD']  
            # Update the secrets details
            update_env({'SENDER_NAME': SENDER_NAME, 
                        'SMTP_USERNAME': SMTP_USERNAME,
                        'SMTP_PASSWORD': SMTP_PASSWORD, 
                        'DRIVER_NAME': DRIVER_NAME,
                        'SERVER_NAME': SERVER_NAME, 
                        'DATABASE_NAME': DATABASE_NAME, 
                        'USERNAME': USERNAME, 
                        'PASSWORD': PASSWORD})
            # Redirect to the same view after saving to refresh the data
            messages.success(request, 'Secrets updated successfully!')

            return redirect('customize_secrets')
        except Exception as e:
            logging.error("Error updating secrets: %s", e)
            messages.error(request, f'An error occurred while updating the secrets: {str(e)}')
        return redirect('customize_secrets')


    else:
        # Prepare the context for secrets
        
        SENDER_NAME = os.getenv('SENDER_NAME')
        SMTP_USERNAME = os.getenv('SMTP_USERNAME')
        SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')        
        DRIVER_NAME = os.getenv('DRIVER_NAME')
        SERVER_NAME = os.getenv('SERVER_NAME')
        DATABASE_NAME = os.getenv('DATABASE_NAME')
        DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
        DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
        # Mask sensitive data before sending to the frontend
        SMTP_PASSWORD=mask_sensitive(SMTP_PASSWORD,show_chars=2)
        DATABASE_PASSWORD=mask_sensitive(DATABASE_PASSWORD)
        context = {'SENDER_NAME': SENDER_NAME, 
                     'SMTP_USERNAME': SMTP_USERNAME,
                       'SMTP_PASSWORD': SMTP_PASSWORD, 
                       'DRIVER_NAME': DRIVER_NAME,
                        'SERVER_NAME': SERVER_NAME, 
                       'DATABASE_NAME': DATABASE_NAME, 
                       'USERNAME': DATABASE_USERNAME, 
                       'PASSWORD': DATABASE_PASSWORD}
        

    # Render the template with the context
    return render(request, 'secrets.html', context)

def hc_dashboard(request):
    logging.debug("Rendering mailed details page")
    # Fetch the mailed data from the database
    result = hc_content_object.get_dashboard_content()
    logging.debug(f"Retrieved mailed data: {result}")
    context = {
        "mailed_data": result
    }
    # Render the template with the context
    return render(request, 'hc_dashboard.html', context)

def faq(request):
    return render(request, 'FAQ.html')