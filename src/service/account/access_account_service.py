from ethos.elint.entities.generic_pb2 import TemporaryTokenDetails
from ethos.elint.services.product.identity.account.access_account_pb2 import ValidateAccountResponse, \
    VerifyAccountResponse
from ethos.elint.services.product.identity.account.access_account_pb2_grpc import AccessAccountServiceServicer
from support.db_service import is_existing_account_mobile, get_account
from support.helper_functions import get_random_string, gen_uuid, get_current_timestamp, send_otp, get_future_timestamp
from support.redis_service import set_kv, get_kv
from support.session_manager import create_account_access_auth_details, update_persistent_session_last_requested_at, \
    create_account_service_access_auth_details


class AccessAccountService(AccessAccountServiceServicer):
    def __init__(self):
        super(AccessAccountService, self).__init__()
        self.session_scope = self.__class__.__name__

    def ValidateAccount(self, request, context):
        # get request params here
        account_mobile_number = request.account_mobile_number
        requested_at = request.requested_at

        # check account existence
        account_exists_with_mobile = is_existing_account_mobile(account_mobile_number)

        # take action
        if account_exists_with_mobile:
            # send otp
            verification_code = get_random_string(6)
            code_token = gen_uuid()
            code_generated_at = get_current_timestamp()
            # send the code to mobile
            country_code = "+91"
            code_sent_at = send_otp(country_code, account_mobile_number, verification_code)
            # store the token details
            set_kv({code_token: verification_code})
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
                account_service_access_auth_details = create_account_service_access_auth_details(
                    account_id=account.account_id, session_scope=self.session_scope)
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
            new_verification_code = get_random_string(6)
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
