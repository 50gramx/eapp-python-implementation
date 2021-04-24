#   /*************************************************************************
#   *
#   * AMIT KUMAR KHETAN CONFIDENTIAL
#   * __________________
#   *
#   *  [2017] - [2021] Amit Kumar Khetan
#   *  All Rights Reserved.
#   *
#   * NOTICE:  All information contained herein is, and remains
#   * the property of Amit Kumar Khetan and its suppliers,
#   * if any.  The intellectual and technical concepts contained
#   * herein are proprietary to Amit Kumar Khetan
#   * and its suppliers and may be covered by U.S. and Foreign Patents,
#   * patents in process, and are protected by trade secret or copyright law.
#   * Dissemination of this information or reproduction of this material
#   * is strictly forbidden unless prior written permission is obtained
#   * from Amit Kumar Khetan.
#   */

import os
import random
import string
import time
import uuid
from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp
from sendgrid import SendGridAPIClient, Mail
from twilio.rest import Client
from validate_email import validate_email

from ethos.elint.entities.generic_pb2 import TemporaryTokenDetails
from support.redis_service import set_kv, get_kv

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


def get_random_string(length) -> str:
    """
    Random string with the combination of lower and upper case
    :param length: length of the random string
    :return:  random string, generated_at time
    """
    return ''.join(random.choice(string.digits) for i in range(length))


def get_random_digits(length) -> (str, float):
    """
        generates and retruns random digits of defined length
        :param length: length of the random digits
        :return:  random string, generated_at time
        """
    return ''.join(random.choice(string.digits) for i in range(length)), time.time()


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


def send_otp(country_code, account_mobile_number, verification_code) -> Timestamp:
    # Download the helper library from https://www.twilio.com/docs/python/install
    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages.create(
        body=f"50GRAMX: Your security code is: {verification_code}. "
             f"It expires in 10 minutes. Don't share this code with anyone.",
        from_='+18182379146',
        to=f"{country_code}{account_mobile_number}"
    )
    print(verification_code)
    return get_current_timestamp()


# --------------------------------------
# Timestamps Helpers
# --------------------------------------

def get_current_timestamp() -> Timestamp:
    ts = Timestamp()
    ts.GetCurrentTime()
    return ts


def format_timestamp_to_datetime(timestamp: Timestamp) -> datetime:
    return timestamp.ToDatetime()


def format_timestamp_to_iso_string(timestamp: Timestamp) -> str:
    return timestamp.ToJsonString()


def format_datetime_to_timestamp(timestamp: datetime) -> Timestamp:
    timestamp_obj = Timestamp()
    timestamp_obj.FromDatetime(timestamp)
    return timestamp_obj


def format_iso_string_to_timestamp(timestamp: str) -> Timestamp:
    ts = Timestamp()
    ts.FromJsonString(timestamp)
    return ts


def format_datetime_to_iso_string(timestamp: datetime) -> str:
    return format_timestamp_to_iso_string(format_datetime_to_timestamp(timestamp))


def format_iso_string_to_datetime(timestamp: str) -> datetime:
    return format_timestamp_to_datetime(format_iso_string_to_timestamp(timestamp))


def get_future_timestamp(after_seconds: int, after_minutes: int = 0, after_hours: int = 0) -> Timestamp:
    ts = get_current_timestamp()
    future_seconds = ts.seconds + after_seconds + (after_minutes * 60) + (after_hours * 3600)
    return Timestamp(seconds=future_seconds, nanos=ts.nanos)


# --------------------------------------
# Generic Helpers
# --------------------------------------

def gen_uuid() -> str:
    return str(uuid.uuid4()).upper()


# --------------------------------------
# Phone Numbers
# --------------------------------------
def generate_verification_code_token(account_mobile_country_code: str, account_mobile_number: str,
                                     code_token: str = None) -> (
        TemporaryTokenDetails, Timestamp):
    verification_code = get_random_string(4)
    if code_token is None:
        code_token = gen_uuid()
    code_sent_at = send_otp(account_mobile_country_code, account_mobile_number, verification_code)
    set_kv(code_token, verification_code)
    verification_code_token_details = TemporaryTokenDetails(
        token=code_token,
        generated_at=get_current_timestamp(),
        valid_till=get_future_timestamp(after_seconds=180)
    )
    return verification_code_token_details, code_sent_at


def verify_verification_code_token(token: str, verification_code: str) -> bool:
    sent_verification_code = get_kv(token)
    if verification_code == sent_verification_code:
        return True
    else:
        return False
