import smtplib
from email.mime.text import MIMEText

from app.core.config import settings


def send_message(body: str, to: str, subject: str):
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = settings.SMTP_USER
    msg['To'] = to
    msg['Subject'] = subject

    server = smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT)
    server.login(settings.SMTP_USER, settings.SMTP_PASS)

    server.sendmail(settings.SMTP_USER, to, msg.as_string())

    server.quit()