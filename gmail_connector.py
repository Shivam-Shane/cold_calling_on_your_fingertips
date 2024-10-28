import socket
import ssl
from logger import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from utility import read_yaml
import os

class GmailFetcher():
    def __init__(self):
        self.config = read_yaml("config.yaml")

    def email_sender(self, to_emails, subject, body, attachments):
        """
        Sends an email with optional attachments.

        :param to_emails: List of recipient email addresses.
        :param subject: Subject of the email.
        :param body: Body of the email, can contain HTML content.
        :param attachments: List of file paths to attach to the email.
        """
        try:
            # Prepare the email message
            msg = MIMEMultipart()
            SENDER_NAME_VALUE = self.config.get('SENDER_NAME')
            SENDER_EMAIL = self.config.get('SMTP_USERNAME')
            msg['From'] = f'{SENDER_NAME_VALUE} <{SENDER_EMAIL}>'
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))  # Use HTML content

            # Ensure attachments is a list, even if a single file is provided
            if attachments:
                if isinstance(attachments, str):
                    attachments = [attachments]

                # Attach files if provided
                for file_path in attachments:
                    if not os.path.isfile(file_path):
                        logging.warning(f"Attachment file not found: {file_path}")
                        continue
                    try:
                        # Open file in binary mode
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(attachment.read())

                        # Encode file in ASCII characters to send by email
                        encoders.encode_base64(part)

                        # Add header as key/value pair to the attachment part
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename={os.path.basename(file_path)}",
                        )

                        # Attach the file to the message
                        msg.attach(part)
                    except Exception as e:
                        logging.error(f"Error attaching file {file_path}: {str(e)}")
                        raise e

            # Send email using SMTP
            logging.debug(f"Connecting to SMTP server {self.config.get('SMTP_SERVER')}")
            with smtplib.SMTP(self.config["SMTP_SERVER"], self.config["SMTP_PORT"]) as server:
                server.starttls()
                server.login(self.config["SMTP_USERNAME"], self.config["SMTP_PASSWORD"])
                server.sendmail(self.config["SMTP_USERNAME"], to_emails, msg.as_string())
                logging.info(f"Email sent to {', '.join(to_emails)}")

        except (socket.gaierror, socket.timeout) as net_err:
            logging.error(f"Network issue while connecting to SMTP server: {str(net_err)}")
            raise net_err
        except ssl.SSLError as ssl_err:
            logging.error(f"SSL error while connecting to SMTP server: {str(ssl_err)}")
            raise ssl_err
        except smtplib.SMTPException as smtp_err:
            logging.error(f"SMTP error: {str(smtp_err)}")
            raise smtp_err
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
            raise e