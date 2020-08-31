import datetime
import os
import random
import string

from sendgrid import SendGridAPIClient, Mail
from validate_email import validate_email

sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')


def validate_email_dns(email_id: str) -> bool:
    validation = validate_email(email_id, verify=True)
    if validation is False or validation is None:
        return False
    else:
        return True


def mail(from_email: str, to_email: str, subject: str, html_content: str) -> bool:
    if validate_email(from_email) and validate_email(to_email):
        if len(subject) < 200:
            message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content
            )
    try:
        client = SendGridAPIClient(sendgrid_api_key)
        client.send(message)
        return True
    except Exception as e:
        return False


def get_random_string(length):
    """
    Random string with the combination of lower and upper case
    :param length: length of the random string
    :return:  random string, generated_at time
    """
    return ''.join(random.choice(string.ascii_letters) for i in range(length)), datetime.datetime.now()
