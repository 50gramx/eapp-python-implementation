import phonenumbers

from ethos.elint.entities.generic_pb2 import TemporaryTokenDetails
from ethos.elint.services.product.identity.account.create_account_pb2 import ValidateAccountWithMobileResponse, \
    VerificationAccountResponse, CaptureAccountMetaDetailsResponse
from ethos.elint.services.product.identity.account.create_account_pb2_grpc import CreateAccountServiceServicer
from models.account_connection_models import AccountConnections
from models.base_models import Account, AccountDevices
from services_caller.account_assistant_service_caller import create_account_assistant_caller
from services_caller.message_conversation_service_caller import setup_account_conversations_caller
from support.db_service import is_existing_account_mobile, add_new_account, get_our_galaxy, add_new_account_devices
from support.helper_functions import get_random_string, gen_uuid, get_current_timestamp, get_future_timestamp, send_otp, \
    format_timestamp_to_datetime
from support.redis_service import set_kv, get_kv
from support.session_manager import create_account_creation_auth_details, \
    update_persistent_session_last_requested_at, create_account_services_access_auth_details


class CreateAccountService(CreateAccountServiceServicer):
    def __init__(self):
        super(CreateAccountService, self).__init__()
        self.session_scope = self.__class__.__name__

    def ValidateAccountWithMobile(self, request, context):
        print("CreateAccountService:ValidateAccountWithMobile invoked.")
        # get request params here
        account_mobile_number = request.account_mobile_number
        requested_at = request.requested_at

        # check account existence
        account_country_code = "+" + str(phonenumbers.parse(account_mobile_number, "IN").country_code)
        account_exists_with_mobile = is_existing_account_mobile(account_country_code, account_mobile_number)

        # take action
        if not account_exists_with_mobile:
            # send otp
            verification_code = get_random_string(4)
            code_token = gen_uuid()
            code_generated_at = get_current_timestamp()
            # send the code to mobile
            country_code = "+91"
            code_sent_at = send_otp(country_code, account_mobile_number, verification_code)
            # store the token details
            set_kv(code_token, verification_code)
            # create the code token details here
            verification_code_token_details = TemporaryTokenDetails(
                token=code_token,
                generated_at=code_generated_at,
                valid_till=get_future_timestamp(after_seconds=180)
            )
            # create response
            validate_account_with_mobile_response = ValidateAccountWithMobileResponse(
                account_creation_auth_details=create_account_creation_auth_details(
                    account_mobile_number=account_mobile_number,
                    session_scope=self.session_scope
                ),
                account_exists_with_mobile=account_exists_with_mobile,
                verification_code_token_details=verification_code_token_details,
                code_sent_at=code_sent_at,
                validate_account_with_mobile_done=True,
                validate_account_with_mobile_message="OTP Sent to the Mobile Number"
            )
        else:
            validate_account_with_mobile_response = ValidateAccountWithMobileResponse(
                account_exists_with_mobile=account_exists_with_mobile,
                validate_account_with_mobile_done=False,
                validate_account_with_mobile_message="Account already exists. Please Access your Account."
            )
        return validate_account_with_mobile_response

    def VerificationAccount(self, request, context):
        print("CreateAccountService:VerificationAccount invoked.")
        # Get the request params here
        account_creation_auth_details = request.account_creation_auth_details
        resend_code = request.resend_code
        verification_code = request.verification_code
        verification_code_token_details = request.verification_code_token_details
        requested_at = request.requested_at

        # Update the session here
        update_persistent_session_last_requested_at(
            account_creation_auth_details.account_creation_session_token_details.session_token, requested_at)

        if not resend_code:
            # verify the code and return the status
            sent_verification_code = get_kv(verification_code_token_details.token)
            if verification_code == sent_verification_code:
                # verification successful
                verification_done = True
                verification_message = "Account successfully verified."
            else:
                # verification failed
                verification_done = False
                verification_message = "Verification failed. Please check the sent OTP and retry again."
        else:
            # resend the code and return the status
            new_verification_code = get_random_string(4)
            country_code = "+91"
            account_mobile_number = account_creation_auth_details.account_mobile_number
            code_sent_at = send_otp(country_code, account_mobile_number, new_verification_code)
            verification_done = False
            verification_message = "Code resent. Please verify to continue."
        verification_account_response = VerificationAccountResponse(
            verification_done=verification_done,
            verification_message=verification_message
        )
        return verification_account_response

    def CaptureAccountMetaDetails(self, request, context):
        print("CreateAccountService:CaptureAccountMetaDetails invoked.")
        # Get the request params here
        account_creation_auth_details = request.account_creation_auth_details
        account_first_name = request.account_first_name
        account_last_name = request.account_last_name
        account_birth_at = request.account_birth_at
        account_gender = request.account_gender
        requested_at = request.requested_at

        # update the session here
        update_persistent_session_last_requested_at(
            account_creation_auth_details.account_creation_session_token_details.session_token, requested_at)

        # create the account here
        account_analytics_id = gen_uuid()
        account_id = gen_uuid()
        account_country_code = "+91"
        account_galaxy_id = get_our_galaxy().galaxy_id
        account_mobile_number = account_creation_auth_details.account_mobile_number
        new_account = Account(
            account_analytics_id=account_analytics_id,
            account_id=account_id,
            account_country_code=account_country_code,
            account_mobile_number=account_mobile_number,
            account_first_name=account_first_name,
            account_last_name=account_last_name,
            account_galaxy_id=account_galaxy_id,
            account_gender=account_gender,
            account_birth_at=format_timestamp_to_datetime(account_birth_at),
            account_created_at=format_timestamp_to_datetime(requested_at),
            account_billing_active=False
        )
        # add the new account to db
        add_new_account(new_account)
        # add the new account device details
        new_account_devices = AccountDevices(
            account_id=account_id,
            account_device_os=request.account_device_details.account_device_os,
            account_device_token=request.account_device_details.device_token,
            account_device_token_accessed_at=format_timestamp_to_datetime(requested_at)
        )
        add_new_account_devices(new_account_devices)
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
        # create the response here
        capture_account_meta_details_response = CaptureAccountMetaDetailsResponse(
            account_service_access_auth_details=account_services_access_auth_details,
            account_creation_done=account_creation_done,
            account_creation_message=account_creation_message
        )
        # create account assistant
        # create_done, create_message, account_assistant_services_access_auth_details = create_account_assistant_caller(
        #     account_services_access_auth_details)
        # create account assistant connection

        return capture_account_meta_details_response
