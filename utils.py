from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

from os import environ


def send_mail(body):
    smtp = SMTP('imap.gmail.com', 587)
    smtp.starttls()
    try:
        smtp.login(environ.get('IMAP_USER'), environ.get('IMAP_PASSWD'))
        message = MIMEMultipart()
        message['From'] = environ.get('IMAP_USER')
        message['To'] = environ.get('IMAP_USER')
        message['Subject'] = r'Bot: futabus-notification'
        message.attach(MIMEText(body, 'plain'))
        smtp.sendmail(environ.get('IMAP_USER'), environ.get('IMAP_USER'), message.as_string())
    finally:
        smtp.quit()
