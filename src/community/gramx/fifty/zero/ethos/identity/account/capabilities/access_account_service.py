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

from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account.access_account_pb2 import VerifyAccountResponse, \
    ValidateAccountServicesResponse, ReAccountAccessTokenResponse
from ethos.elint.services.product.identity.account.access_account_pb2_grpc import AccessAccountServiceServicer
from opentracing import tags
from opentracing.propagation import Format

from access.account.services_authentication import AccessAccountServicesAuthentication
from community.gramx.fifty.zero.ethos.identity.account.capabilities.access_account_impl import validate_account_impl
from services_caller.account_service_caller import validate_account_services_caller
from support.application.tracing import init_tracer
from support.database.account_devices_services import update_account_devices
from support.database.account_services import get_account
from support.helper_functions import get_random_string, send_otp, format_timestamp_to_datetime
from support.redis_service import get_kv
from support.session_manager import update_persistent_session_last_requested_at, \
    is_persistent_session_valid

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class AccessAccountService(AccessAccountServiceServicer):
    def __init__(self):
        super(AccessAccountService, self).__init__()
        self.session_scope = self.__class__.__name__
        self.tracer = init_tracer('access-account-service')

    def __del__(self):
        self.tracer.close()

    def ValidateAccount(self, request, context):
        # Convert the metadata to a dictionary for opentracing.
        metadata_dict = dict(context.invocation_metadata())

        # Extract span context using the TEXT_MAP format.
        span_ctx = self.tracer.extract(Format.TEXT_MAP, metadata_dict)
        with self.tracer.start_active_span('ValidateAccount', child_of=span_ctx) as scope:
            # Add some tags
            scope.span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
            scope.span.set_tag(tags.PEER_SERVICE, 'unknown-service')  # or wherever the request is coming from
            scope.span.set_tag('account_mobile_number', request.account_mobile_number)

            logging.info("AccessAccountService:ValidateAccount")
            try:
                return validate_account_impl(request=request, session_scope=self.session_scope)
            except Exception as e:
                logging.error(f"An error occurred during ValidateAccount RPC: {e}")
                # You might also want to modify the response or set gRPC status to signal the error.

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
                # update account devices
                update_account_devices(
                    account_id=account.account_id,
                    account_device_os=request.account_device_details.account_device_os,
                    account_device_token=request.account_device_details.device_token,
                    account_device_token_accessed_at=format_timestamp_to_datetime(requested_at)
                )
                verify_account_response = VerifyAccountResponse(
                    account_service_access_auth_details=AccessAccountServicesAuthentication(
                        session_scope=self.session_scope,
                        account_id=account.account_id
                    ).create_authentication_details(),
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
            # TODO: Store the new verification code to cache
            code_sent_at = send_otp(
                country_code="+91",
                account_mobile_number=account_access_auth_details.account_mobile_number,
                verification_code=new_verification_code)
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
        if request.account.account_id is "":
            return ValidateAccountServicesResponse(
                account_service_access_validation_done=False,
                account_service_access_validation_message="Invalid Request. This action will be reported."
            )

        account_id = request.account.account_id
        # validate the account
        if get_account(account_id=account_id).account_id != account_id:
            # create the response here
            return ValidateAccountServicesResponse(
                account_service_access_validation_done=False,
                account_service_access_validation_message="Requesting account is not legit. This action will be reported."
            )
        else:
            # validate the session
            session_valid, session_valid_message = is_persistent_session_valid(
                request.account_services_access_session_token_details.session_token,
                account_id,
                self.session_scope
            )
            return ValidateAccountServicesResponse(
                account_service_access_validation_done=session_valid,
                account_service_access_validation_message=session_valid_message
            )

    def ReAccountAccessToken(self, request, context):
        logging.info("AccessAccountService:ReAccountAccessToken")
        validation_done, validation_message = validate_account_services_caller(
            request.account_service_access_auth_details)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            if validation_message == "Session has expired. Retrieve a new session.":
                return ReAccountAccessTokenResponse(
                    account_service_access_auth_details=AccessAccountServicesAuthentication(
                        session_scope=self.session_scope,
                        account_id=request.account_service_access_auth_details.account.account_id
                    ).create_authentication_details(),
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
