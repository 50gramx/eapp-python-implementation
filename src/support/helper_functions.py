import os
import random
import string
import time
import uuid

from google.protobuf.timestamp_pb2 import Timestamp
from sendgrid import SendGridAPIClient, Mail
from twilio.rest import Client
from validate_email import validate_email

sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
twilio_account_sid = os.environ['SMS_API_ACCOUNT_SID']
twilio_auth_token = os.environ['SMS_API_AUTH_TOKEN']


def validate_email_dns(email_id: str, check_mx: bool = True, verify: bool = False) -> bool:
    validation = validate_email(email_id, check_mx=check_mx, verify=verify)
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


def get_random_string(length) -> (str, float):
    """
    Random string with the combination of lower and upper case
    :param length: length of the random string
    :return:  random string, generated_at time
    """
    return ''.join(random.choice(string.ascii_letters) for i in range(length)), time.time()


def get_random_digits(length) -> (str, float):
    """
        generates and retruns random digits of defined length
        :param length: length of the random digits
        :return:  random string, generated_at time
        """
    return ''.join(random.choice(string.digits) for i in range(length)), time.time()


def get_current_timestamp() -> Timestamp:
    curr_time = time.time()
    seconds = int(curr_time)
    nanos = int((curr_time - seconds) * 10 ** 9)
    return Timestamp(seconds=seconds, nanos=nanos)


def get_future_timestamp(after_seconds: int, after_minutes: int = 0, after_hours: int = 0) -> Timestamp:
    future_time = time.time() + after_seconds + (after_minutes * 60) + (after_hours * 3600)
    seconds = int(future_time)
    nanos = int((future_time - seconds) * 10 ** 9)
    return Timestamp(seconds=seconds, nanos=nanos)


def format_time2timestamp(time: float) -> Timestamp:
    """
    returns time in timestamp, by default the current timestamp
    :param time:
    :return: google.protobuf.Timestamp
    """
    seconds = int(time)
    nanos = int((time - seconds) * 10 ** 9)
    return Timestamp(seconds=seconds, nanos=nanos)


def gen_uuid() -> str:
    return str(uuid.uuid4())


def check_service_time_consumption(no_of_iter: int, service_func, service_func_params=None) -> float:
    """
    returns the average time taken for service call in milliseconds
    :param service_func_params:
    :param no_of_iter:
    :param service_func:
    :return:
    """
    if service_func_params is None:
        service_func_params = []
    total_time = []
    for i in range(no_of_iter):
        tic = time.time()
        if service_func_params is None:
            ps = service_func()
        else:
            ps = service_func(service_func_params)
        toc = time.time()
        total_time.append((toc - tic))
    tts = sum(total_time) / no_of_iter
    return tts * 1000


def send_otp(country_code, account_mobile_number, verification_code):
    # Download the helper library from https://www.twilio.com/docs/python/install
    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages.create(
        body=f"Hello Pathos! The OTP to access your account is {verification_code}. Thanks.",
        from_='+18182379146',
        to=f"{country_code}{account_mobile_number}"
    )
    return get_current_timestamp()
