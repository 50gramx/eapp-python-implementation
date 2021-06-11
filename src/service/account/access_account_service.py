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

from ethos.elint.entities.generic_pb2 import TemporaryTokenDetails, ResponseMeta
from ethos.elint.services.product.identity.account.access_account_pb2 import ValidateAccountResponse, \
    VerifyAccountResponse, ValidateAccountServicesResponse, ReAccountAccessTokenResponse
from ethos.elint.services.product.identity.account.access_account_pb2_grpc import AccessAccountServiceServicer
from services_caller.account_service_caller import validate_account_services_caller
from support.db_service import is_existing_account_mobile, get_account, update_account_devices
from support.helper_functions import get_random_string, gen_uuid, get_current_timestamp, send_otp, get_future_timestamp, \
    format_timestamp_to_datetime
from support.redis_service import set_kv, get_kv
from support.session_manager import create_account_access_auth_details, update_persistent_session_last_requested_at, \
    is_persistent_session_valid, create_account_services_access_auth_details


class AccessAccountService(AccessAccountServiceServicer):
    def __init__(self):
        super(AccessAccountService, self).__init__()
        self.session_scope = self.__class__.__name__

    def ValidateAccount(self, request, context):
        logging.info("AccessAccountService:ValidateAccount")
        # get request params here
        account_mobile_number = request.account_mobile_number
        requested_at = request.requested_at

        # check account existence
        account_country_code = "+" + str(phonenumbers.parse(account_mobile_number, "IN").country_code)
        account_exists_with_mobile = is_existing_account_mobile(account_country_code, account_mobile_number)

        # take action
        if account_exists_with_mobile:
            # send otp
            verification_code = get_random_string(4)
            code_token = gen_uuid()
            code_generated_at = get_current_timestamp()
            # send the code to mobile
            code_sent_at = send_otp(account_country_code, account_mobile_number, verification_code)
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
                account_access_auth_details=create_account_access_auth_details(
                    account_mobile_number=account_mobile_number,
                    session_scope=self.session_scope
                ),
                account_exists=account_exists_with_mobile,
                verification_code_token_details=verification_code_token_details,
                code_sent_at=code_sent_at,
                validate_account_done=True,
                validate_account_message="OTP Sent to the Mobile Number"
            )
        else:
            validate_account_response = ValidateAccountResponse(
                account_exists=account_exists_with_mobile,
                validate_account_done=False,
                validate_account_message="Account doesn't exists. Please Create your Account."
            )
        return validate_account_response

    def VerifyAccount(self, request, context):
        logging.info("AccessAccountService:VerifyAccount invoked.")
        # get the request params here
        account_access_auth_details = request.account_access_auth_details
        resend_code = request.resend_code
        verification_code_token_details = request.verification_code_token_details
        verification_code = request.verification_code
        requested_at = request.requested_at

        # update the session here
        update_persistent_session_last_requested_at(
            account_access_auth_details.account_access_auth_session_token_details.session_token, requested_at)

        if not resend_code:
            # verify the code and return the status
            sent_verification_code = get_kv(verification_code_token_details.token)
            if verification_code == sent_verification_code:
                # verification successful
                verification_done = True
                verification_message = "Account successfully verified."
                # access account id
                account = get_account(account_mobile_number=account_access_auth_details.account_mobile_number)
                account_service_access_auth_details = create_account_services_access_auth_details(
                    account_id=account.account_id, session_scope=self.session_scope)
                # update account devices
                update_account_devices(
                    account_id=account.account_id,
                    account_device_os=request.account_device_details.account_device_os,
                    account_device_token=request.account_device_details.device_token,
                    account_device_token_accessed_at=format_timestamp_to_datetime(requested_at)
                )
                verify_account_response = VerifyAccountResponse(
                    account_service_access_auth_details=account_service_access_auth_details,
                    verification_done=verification_done,
                    verification_message=verification_message
                )
            else:
                # verification failed
                verification_done = False
                verification_message = "Verification failed. Please check the sent OTP and retry again."
                verify_account_response = VerifyAccountResponse(
                    verification_done=verification_done,
                    verification_message=verification_message
                )
        else:
            # resend the code and return the status
            new_verification_code = get_random_string(4)
            country_code = "+91"
            account_mobile_number = account_access_auth_details.account_mobile_number
            code_sent_at = send_otp(country_code, account_mobile_number, new_verification_code)
            # create the response here
            verification_done = False
            verification_message = "Code resent. Please verify to continue."
            verify_account_response = VerifyAccountResponse(
                verification_done=verification_done,
                verification_message=verification_message
            )
        return verify_account_response

    def ValidateAccountServices(self, request, context):
        logging.info("AccessAccountService:ValidateAccountServices invoked.")
        # validate request params
        if request.account.account_id is None:
            return ValidateAccountServicesResponse(
                account_service_access_validation_done=False,
                account_service_access_validation_message="Invalid Request. This action will be reported."
            )

        account = request.account
        account_services_access_session_token_details = request.account_services_access_session_token_details
        requested_at = request.requested_at

        # validate the account
        if get_account(account_id=account.account_id).account_id != account.account_id:
            account_service_access_validation_done = False
            account_service_access_validation_message = "Requesting account is not legit. This action will be reported."
            # create the response here
            validate_account_service_response = ValidateAccountServicesResponse(
                account_service_access_validation_done=account_service_access_validation_done,
                account_service_access_validation_message=account_service_access_validation_message
            )
            return validate_account_service_response
        else:
            # validate the session
            session_valid, session_valid_message = is_persistent_session_valid(
                account_services_access_session_token_details.session_token,
                account.account_id,
                self.session_scope
            )
            validate_account_service_response = ValidateAccountServicesResponse(
                account_service_access_validation_done=session_valid,
                account_service_access_validation_message=session_valid_message
            )
            return validate_account_service_response

    def ReAccountAccessToken(self, request, context):
        logging.info("AccessAccountService:ReAccountAccessToken")
        validation_done, validation_message = validate_account_services_caller(
            request.account_service_access_auth_details)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            if validation_message == "Session has expired. Retrieve a new session.":
                # create a new account services access auth details
                new_access_auth_details = create_account_services_access_auth_details(
                    account_id=request.account_service_access_auth_details.account.account_id,
                    session_scope=self.session_scope)
                return ReAccountAccessTokenResponse(
                    account_service_access_auth_details=new_access_auth_details,
                    response_meta=ResponseMeta(meta_done=True, meta_message="New Session retrieved."))
            else:
                # Not authorised access, do not create one
                return ReAccountAccessTokenResponse(
                    account_service_access_auth_details=request.account_service_access_auth_details,
                    response_meta=meta)
        else:
            # Session is valid, no need to create one
            return ReAccountAccessTokenResponse(
                account_service_access_auth_details=request.account_service_access_auth_details,
                response_meta=ResponseMeta(meta_done=True, meta_message="Session is already valid."))
