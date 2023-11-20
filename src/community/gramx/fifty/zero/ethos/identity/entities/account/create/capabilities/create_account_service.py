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

from ethos.elint.entities.galaxy_pb2 import OpenGalaxyTierEnum
from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account.create_account_pb2 import ValidateAccountWithMobileResponse, \
    VerificationAccountResponse, CaptureAccountMetaDetailsResponse
from ethos.elint.services.product.identity.account.create_account_pb2_grpc import CreateAccountServiceServicer
from ethos.elint.services.product.identity.account.pay_in_account_pb2 import \
    ConfirmAccountOpenGalaxyPlayStoreSubscriptionRequest

from access.account.authentication import AccessAccountAuthentication
from access.account.services_authentication import AccessAccountServicesAuthentication
from application_context import ApplicationContext
from community.gramx.fifty.zero.ethos.conversations.services_caller.message_conversation_service_caller import \
    setup_account_conversations_caller
from community.gramx.fifty.zero.ethos.identity.models.account_connection_models import AccountConnections
from community.gramx.fifty.zero.ethos.identity.models.base_models import Account, AccountDevices
from community.gramx.fifty.zero.ethos.identity.services_caller.account_assistant_service_caller import \
    create_account_assistant_caller
from community.gramx.fifty.zero.ethos.identity.services_caller.account_service_caller import \
    validate_account_services_caller
from support.application.tracing import trace_rpc
from support.database.account_devices_services import check_existing_account_device, add_new_account_devices
from support.database.account_services import is_existing_account_mobile, add_new_account, activate_account_billing, \
    deactivate_account_billing
from support.database.galaxy_services import get_our_galaxy
from support.helper_functions import gen_uuid, format_timestamp_to_datetime, generate_verification_code_token, \
    verify_verification_code_token
from support.session_manager import update_persistent_session_last_requested_at


class CreateAccountService(CreateAccountServiceServicer):
    def __init__(self):
        super(CreateAccountService, self).__init__()
        self.session_scope = self.__class__.__name__

    @trace_rpc()
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
                account_creation_auth_details=AccessAccountAuthentication(
                    session_scope=self.session_scope,
                    account_mobile_country_code=request.account_mobile_country_code,
                    account_mobile_number=request.account_mobile_number,
                ).create_creation_authentication_details(),
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

    @trace_rpc()
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

    @trace_rpc()
    def CaptureAccountMetaDetails(self, request, context):
        logging.info("CreateAccountService:CaptureAccountMetaDetails invoked.")

        # update the session here
        update_persistent_session_last_requested_at(
            request.account_creation_auth_details.account_creation_session_token_details.session_token,
            request.requested_at)
        logging.info("Session updated.")

        # create the account here
        account_analytics_id = gen_uuid()
        account_id = gen_uuid()
        account_galaxy_id = get_our_galaxy().galaxy_id

        logging.info("Generated IDs.")

        # before adding account, check if the device is already registered
        if check_existing_account_device(account_device_token=request.account_device_details.device_token):
            logging.warning("Device already registered with another account.")
            return CaptureAccountMetaDetailsResponse(
                account_creation_done=False,
                account_creation_message="Your device is already registered with another account. Trying to sign in?"
            )

        logging.info("Device check passed.")

        new_account = Account(
            account_analytics_id=account_analytics_id, account_id=account_id,
            account_country_code=request.account_creation_auth_details.account_mobile_country_code,
            account_mobile_number=request.account_creation_auth_details.account_mobile_number,
            account_first_name=request.account_first_name, account_last_name=request.account_last_name,
            account_galaxy_id=account_galaxy_id, account_gender=request.account_gender,
            account_birth_at=format_timestamp_to_datetime(request.account_birth_at),
            account_created_at=format_timestamp_to_datetime(request.requested_at), account_billing_active=False)

        logging.info("Account created.")

        # add the new account to db
        add_new_account(new_account)

        logging.info("Account added to the database.")

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

        logging.info("Account device details added.")

        # setup account connections tables
        AccountConnections(account_id=account_id).setup_account_connections()
        logging.info("Account connections tables set up.")

        # create the response params here
        account_creation_done = True
        account_creation_message = "Account successfully created. Thanks."

        logging.info("Response params created.")

        # create account_service_access_auth_details
        account_services_access_auth_details = AccessAccountServicesAuthentication(
            session_scope=self.session_scope,
            account_id=account_id
        ).create_authentication_details()

        logging.info("Account service access auth details created.")

        # setup account conversation
        _, _ = setup_account_conversations_caller(access_auth_details=account_services_access_auth_details)

        logging.info("Account conversation set up.")

        # setup account pay_in
        _ = ApplicationContext.pay_in_account_service_stub().CreateAccountPayIn(account_services_access_auth_details)

        logging.info("Account pay-in set up.")

        # add account to free tier
        subscription_request = ConfirmAccountOpenGalaxyPlayStoreSubscriptionRequest(
            access_auth_details=account_services_access_auth_details,
            open_galaxy_tier_enum=OpenGalaxyTierEnum.FREE_TIER,
            google_play_purchase_token="",
        )
        _ = ApplicationContext.pay_in_account_service_stub().ConfirmAccountOpenGalaxyPlayStoreSubscription(
            subscription_request)

        logging.info("Account added to free tier.")

        # create the response here
        capture_account_meta_details_response = CaptureAccountMetaDetailsResponse(
            account_service_access_auth_details=account_services_access_auth_details,
            account_creation_done=account_creation_done,
            account_creation_message=account_creation_message
        )

        logging.info("Response created.")

        # create account assistant
        _, _, _ = create_account_assistant_caller(
            access_auth_details=account_services_access_auth_details,
            account_assistant_name=request.account_assistant_name
        )

        logging.info("Account assistant created.")

        return capture_account_meta_details_response

    @trace_rpc()
    def ActivateAccountBilling(self, request, context):
        logging.info("CreateAccountService:ActivateAccountBilling")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return response_meta
        else:
            billing_active = ApplicationContext.discover_account_service_stub().IsAccountBillingActive(
                request).meta_done
            if billing_active:
                return ResponseMeta(
                    meta_done=False, meta_message="Account billing is already active. This incident will be reported."
                )
            else:
                is_activated = activate_account_billing(account_id=request.account.account_id)
                if is_activated:
                    return ResponseMeta(
                        meta_done=True,
                        meta_message="Account billing status is active."
                    )
                else:
                    return ResponseMeta(
                        meta_done=False,
                        meta_message="Something went wrong on our end. Please contact the developer."
                    )

    @trace_rpc()
    def DeactivateAccountBilling(self, request, context):
        logging.info("CreateAccountService:DeactivateAccountBilling")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return response_meta
        else:
            billing_active = ApplicationContext.discover_account_service_stub().IsAccountBillingActive(
                request).meta_done
            if billing_active is False:
                return ResponseMeta(
                    meta_done=False, meta_message="Account billing is already inactive. This incident will be reported."
                )
            else:
                is_deactivated = deactivate_account_billing(account_id=request.account.account_id)
                if is_deactivated:
                    return ResponseMeta(
                        meta_done=True,
                        meta_message="Account billing status is inactive."
                    )
                else:
                    return ResponseMeta(
                        meta_done=False,
                        meta_message="Something went wrong on our end. Please contact the developer."
                    )
