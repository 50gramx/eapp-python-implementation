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
import logging

import phonenumbers
from ethos.elint.entities.generic_pb2 import TemporaryTokenDetails
from ethos.elint.services.product.identity.account.access_account_pb2 import ValidateAccountRequest
from ethos.elint.services.product.identity.account.access_account_pb2 import ValidateAccountResponse

from access.account.authentication import AccessAccountAuthentication
from support.database.account_services import is_existing_account_mobile
from support.helper_functions import get_random_string, gen_uuid, get_current_timestamp, send_otp, get_future_timestamp
from support.session.redis_service import set_kv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def validate_account_impl(request: ValidateAccountRequest, session_scope: str):
    logging.info("Starting ValidateAccount RPC")

    # get request params here
    logging.info(
        f"Received account_mobile_number: {request.account_mobile_number} at {request.requested_at}")

    # check account existence
    account_country_code = request.account_mobile_country_code if request.account_mobile_country_code \
        else "+" + str(phonenumbers.parse(request.account_mobile_number, "IN").country_code)

    logging.info(f"Using account_mobile_country_code: {account_country_code}")

    account_exists_with_mobile = is_existing_account_mobile(account_country_code,
                                                            request.account_mobile_number)

    # take action
    if account_exists_with_mobile:
        logging.info("Account exists with given mobile number. Proceeding to send OTP.")
        # send otp
        verification_code = get_random_string(4)
        code_token = gen_uuid()
        code_generated_at = get_current_timestamp()
        # send the code to mobile
        code_sent_at = send_otp(account_country_code, request.account_mobile_number, verification_code)
        # store the token details
        set_kv(code_token, verification_code)
        # create the code token details here
        verification_code_token_details = TemporaryTokenDetails(
            token=code_token,
            generated_at=code_generated_at,
            valid_till=get_future_timestamp(after_seconds=180)
        )

        # create response
        validate_account_response = ValidateAccountResponse(
            account_access_auth_details=AccessAccountAuthentication(
                session_scope=session_scope,
                account_mobile_country_code=request.account_mobile_country_code,
                account_mobile_number=request.account_mobile_number
            ).create_authentication_details(),
            account_exists=True,
            verification_code_token_details=verification_code_token_details,
            code_sent_at=code_sent_at,
            validate_account_done=True,
            validate_account_message="OTP Sent to the Mobile Number"
        )
        logging.info("OTP sent successfully.")
    else:
        logging.warning("Account does not exist with given mobile number.")
        validate_account_response = ValidateAccountResponse(
            account_exists=account_exists_with_mobile,
            validate_account_done=False,
            validate_account_message="Account doesn't exists. Please Create your Account."
        )

    logging.info("Finishing ValidateAccount RPC")
    return validate_account_response
