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

from application_context import ApplicationContext
from ethos.elint.services.product.identity.account.create_account_pb2 import ValidateAccountWithMobileResponse, \
    VerificationAccountResponse, CaptureAccountMetaDetailsResponse
from ethos.elint.services.product.identity.account.create_account_pb2_grpc import CreateAccountServiceServicer
from models.account_connection_models import AccountConnections
from models.base_models import Account, AccountDevices
from services_caller.account_assistant_service_caller import create_account_assistant_caller
from services_caller.message_conversation_service_caller import setup_account_conversations_caller
from support.db_service import is_existing_account_mobile, add_new_account, get_our_galaxy, add_new_account_devices
from support.helper_functions import gen_uuid, format_timestamp_to_datetime, generate_verification_code_token, \
    verify_verification_code_token
from support.session_manager import create_account_creation_auth_details, \
    update_persistent_session_last_requested_at, create_account_services_access_auth_details


class CreateAccountService(CreateAccountServiceServicer):
    def __init__(self):
        super(CreateAccountService, self).__init__()
        self.session_scope = self.__class__.__name__

    def ValidateAccountWithMobile(self, request, context):
        logging.info("CreateAccountService:ValidateAccountWithMobile invoked.")
        account_exists_with_mobile = is_existing_account_mobile(
            request.account_mobile_country_code,
            request.account_mobile_number
        )
        if not account_exists_with_mobile:
            verification_code_token_details, code_sent_at = generate_verification_code_token(
                account_mobile_country_code=request.account_mobile_country_code,
                account_mobile_number=request.account_mobile_number)
            return ValidateAccountWithMobileResponse(
                account_creation_auth_details=create_account_creation_auth_details(
                    account_mobile_country_code=request.account_mobile_country_code,
                    account_mobile_number=request.account_mobile_number,
                    session_scope=self.session_scope
                ),
                account_exists_with_mobile=account_exists_with_mobile,
                verification_code_token_details=verification_code_token_details, code_sent_at=code_sent_at,
                validate_account_with_mobile_done=True,
                validate_account_with_mobile_message="OTP Sent to the Mobile Number"
            )
        else:
            return ValidateAccountWithMobileResponse(
                account_exists_with_mobile=account_exists_with_mobile,
                validate_account_with_mobile_done=False,
                validate_account_with_mobile_message="Account already exists. Please Access your Account."
            )

    def VerificationAccount(self, request, context):
        logging.info("CreateAccountService:VerificationAccount invoked.")
        update_persistent_session_last_requested_at(
            request.account_creation_auth_details.account_creation_session_token_details.session_token,
            request.requested_at)
        if not request.resend_code:
            if verify_verification_code_token(token=request.verification_code_token_details.token,
                                              verification_code=request.verification_code):
                return VerificationAccountResponse(
                    verification_done=True,
                    verification_message="Account successfully verified.")
            else:
                return VerificationAccountResponse(
                    verification_done=False,
                    verification_message="Verification failed. Please check the sent OTP and retry again.")
        else:
            _, _ = generate_verification_code_token(
                account_mobile_country_code=request.account_creation_auth_details.account_mobile_country_code,
                account_mobile_number=request.account_creation_auth_details.account_mobile_number,
                code_token=request.verification_code_token_details.token)
            return VerificationAccountResponse(
                verification_done=False,
                verification_message="Code resent. Please verify to continue.")

    def CaptureAccountMetaDetails(self, request, context):
        logging.info("CreateAccountService:CaptureAccountMetaDetails invoked.")

        # update the session here
        update_persistent_session_last_requested_at(
            request.account_creation_auth_details.account_creation_session_token_details.session_token,
            request.requested_at)

        # create the account here
        account_analytics_id = gen_uuid()
        account_id = gen_uuid()
        account_galaxy_id = get_our_galaxy().galaxy_id
        new_account = Account(
            account_analytics_id=account_analytics_id, account_id=account_id,
            account_country_code=request.account_creation_auth_details.account_mobile_country_code,
            account_mobile_number=request.account_creation_auth_details.account_mobile_number,
            account_first_name=request.account_first_name, account_last_name=request.account_last_name,
            account_galaxy_id=account_galaxy_id, account_gender=request.account_gender,
            account_birth_at=format_timestamp_to_datetime(request.account_birth_at),
            account_created_at=format_timestamp_to_datetime(request.requested_at), account_billing_active=False)
        # add the new account device details
        try:
            new_account_devices = AccountDevices(
                account_id=account_id,
                account_device_os=request.account_device_details.account_device_os,
                account_device_token=request.account_device_details.device_token,
                account_device_token_accessed_at=format_timestamp_to_datetime(request.requested_at)
            )
            add_new_account_devices(new_account_devices)
        except Exception as e:
            logging.warning(f"CreateAccountService:CaptureAccountMetaDetails:DeviceException: {e}")
            return CaptureAccountMetaDetailsResponse(
                account_creation_done=False,
                account_creation_message="Your device is already registered with another account. Trying to sign in?"
            )
        # add the new account to db
        add_new_account(new_account)
        # setup account connections tables
        AccountConnections(account_id=account_id).setup_account_connections()
        # create the response params here
        account_creation_done = True
        account_creation_message = "Account successfully created. Thanks."
        # create account_service_access_auth_details
        account_services_access_auth_details = create_account_services_access_auth_details(
            account_id=account_id,
            session_scope=self.session_scope
        )
        # setup account conversation
        _, _ = setup_account_conversations_caller(access_auth_details=account_services_access_auth_details)
        # setup account pay_in
        _ = ApplicationContext.pay_in_account_service_stub().CreateAccountPayIn(account_services_access_auth_details)
        # create the response here
        capture_account_meta_details_response = CaptureAccountMetaDetailsResponse(
            account_service_access_auth_details=account_services_access_auth_details,
            account_creation_done=account_creation_done,
            account_creation_message=account_creation_message
        )
        # create account assistant
        _, _, _ = create_account_assistant_caller(
            access_auth_details=account_services_access_auth_details,
            account_assistant_name=request.account_assistant_name
        )
        return capture_account_meta_details_response
