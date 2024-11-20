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

from ethos.elint.services.product.identity.account.access_account_pb2 import (
    VerifyAccountRequest,
    VerifyAccountResponse,
)

from access.account.services_authentication import AccessAccountServicesAuthentication
from support.database.account_devices_services import update_account_devices
from support.database.account_services import get_account
from support.helper_functions import (
    format_timestamp_to_datetime,
    get_random_string,
    send_otp,
)
from support.session.redis_service import get_kv
from support.session_manager import update_persistent_session_last_requested_at


def verify_account_impl(request: VerifyAccountRequest, session_scope: str):
    # get the request params here
    account_access_auth_details = request.account_access_auth_details
    resend_code = request.resend_code
    verification_code_token_details = request.verification_code_token_details
    verification_code = request.verification_code
    requested_at = request.requested_at

    # update the session here
    update_persistent_session_last_requested_at(
        account_access_auth_details.account_access_auth_session_token_details.session_token,
        requested_at,
    )

    if not resend_code:
        # verify the code and return the status
        sent_verification_code = get_kv(verification_code_token_details.token)
        if verification_code == sent_verification_code:
            # verification successful
            verification_done = True
            verification_message = "Account successfully verified."
            # access account id
            account = get_account(
                account_mobile_number=account_access_auth_details.account_mobile_number
            )
            # update account devices
            update_account_devices(
                account_id=account.account_id,
                account_device_os=request.account_device_details.account_device_os,
                account_device_token=request.account_device_details.device_token,
                account_device_token_accessed_at=format_timestamp_to_datetime(
                    requested_at
                ),
            )
            verify_account_response = VerifyAccountResponse(
                account_service_access_auth_details=AccessAccountServicesAuthentication(
                    session_scope=session_scope, account_id=account.account_id
                ).create_authentication_details(),
                verification_done=verification_done,
                verification_message=verification_message,
            )
        else:
            # verification failed
            verification_done = False
            verification_message = (
                "Verification failed. Please check the sent OTP and retry again."
            )
            verify_account_response = VerifyAccountResponse(
                verification_done=verification_done,
                verification_message=verification_message,
            )
    else:
        # resend the code and return the status
        new_verification_code = get_random_string(4)
        # TODO: Store the new verification code to cache
        code_sent_at = send_otp(
            country_code="+91",
            account_mobile_number=account_access_auth_details.account_mobile_number,
            verification_code=new_verification_code,
        )
        # create the response here
        verification_done = False
        verification_message = "Code resent. Please verify to continue."
        verify_account_response = VerifyAccountResponse(
            verification_done=verification_done,
            verification_message=verification_message,
        )
    return verify_account_response
