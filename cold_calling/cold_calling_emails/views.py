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
from gmail_content_decomission import mail_content_handler
from gmail_preview_content import preview_mail
from database_connector import database_connector
from customize_email_content import custom_email_content
from utility import update_yaml,read_yaml

get_email_details_object=custom_email_content()

def index(request):
    return render(request, 'index.html')

def preview_email(request):
    if request.method == 'POST':
        recipient_name=request.POST['recipient_name']
        mail_subject = request.POST['subject']
        recipients = request.POST['recipients']
        company_name = request.POST['company_name']
        company_work_related = request.POST['summary']
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


        email_content=preview_mail(recipient_name,company_name, company_work_related)
        # Pass data to preview template
        context = {
            'subject': mail_subject,
            'recipients': recipients,
            'email_content': email_content,
            'recipient_name': recipient_name,  # Pass this to the context
            'company_name': company_name,
            'summary': company_work_related,
            'resume_path': resume_path,  # Pass the file path to the template

        }
        return render(request, 'preview.html', context)

def send_email(request):
    if request.method == 'POST':
        logging.info("Sending email")
        subject = request.POST['subject']
        recipients = request.POST['recipients'].split(',')
        recipient_name=request.POST['recipient_name']        
        company_name = request.POST['company_name']
        company_work_related = request.POST['summary']
        # Get the resume path from the session
        resume_path = request.session.get('resume_path')
        logging.info(f"Retrieved Resume path from session: {resume_path}")

        body=mail_content_handler(recipient_name, company_name, company_work_related)

        GM=GmailFetcher()
        GM.email_sender(recipients,subject, body,attachments=resume_path)
        # Save the email details in the database
        try:
            connection = database_connector()
            cursor = connection.cursor()

            # Insert the email details into the database
            insert_query = """
            INSERT INTO dbo.sent_data_details (subject, recipients, recipient_name, company_name, company_work_related, body, resume_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (subject, ', '.join(recipients), recipient_name, company_name, company_work_related, body, resume_path))
            connection.commit()
            logging.info("Email details saved to database.")
        except odbc.Error as e:
            logging.error("Error saving to database: %s", e)
        finally:
            cursor.close()
            connection.close()
        return redirect('index')

def customize_email(request):
    if request.method == 'POST':
        your_name = request.POST['your_name']
        phone_no = request.POST['phone_no']
        github_link = request.POST['github_link']        
        linkedin_link = request.POST['linkedin_link']
        portfolio_link = request.POST['portfolio_link']
        # Get the resume path from the session
        resume_path = request.session.get('resume_path')

        # Update the email details
        get_email_details_object.update_email_details(your_name, phone_no, github_link, linkedin_link, portfolio_link, resume_path)
        
        # Redirect to the same view after saving to refresh the data
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
            update_yaml('config.yaml',
                        {'SENDER_NAME': SENDER_NAME, 
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
        config=read_yaml('config.yaml')
        SENDER_NAME = config['SENDER_NAME']
        SMTP_USERNAME = config['SMTP_USERNAME']
        SMTP_PASSWORD = config['SMTP_PASSWORD']        
        DRIVER_NAME = config['DRIVER_NAME']
        SERVER_NAME = config['SERVER_NAME']
        DATABASE_NAME = config['DATABASE_NAME']
        USERNAME = config['USERNAME']
        PASSWORD = config['PASSWORD']
        context = {'SENDER_NAME': SENDER_NAME, 
                     'SMTP_USERNAME': SMTP_USERNAME,
                       'SMTP_PASSWORD': SMTP_PASSWORD, 
                       'DRIVER_NAME': DRIVER_NAME,
                        'SERVER_NAME': SERVER_NAME, 
                       'DATABASE_NAME': DATABASE_NAME, 
                       'USERNAME': USERNAME, 
                       'PASSWORD': PASSWORD}
        

    # Render the template with the context
    return render(request, 'secrets.html', context)