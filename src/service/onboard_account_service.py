import logging
import os


from google.protobuf.timestamp_pb2 import Timestamp

from ethos.elint.entities.generic_pb2 import TemporaryTokenDetails, PersistentSessionTokenDetails
from ethos.elint.services.product.identity.account.onboard_account_pb2 import OnboardAccountResponse, \
    AccountOnboardStatus, VerifyOnboardingAccountResponse, AuthenticateOnboardedAccountResponse, \
    AccessAccountEthosIdentityTokenResponse
from ethos.elint.services.product.identity.account.onboard_account_pb2_grpc import OnboardAccountServiceServicer
from support.helper_functions import format_time2timestamp

logger = logging.getLogger(__name__)
identity_service_mail_id = os.environ['IDENTITY_MAIL_ID']
claim_account_verification_mail_subject = "Verify your account"
claim_account_verification_mail_body = "Short lived verification code: {0}"

timestamp = Timestamp()


class OnboardAccountService(OnboardAccountServiceServicer):
    """
    OnboardAccountService
    """

    def OnboardAccount(self, request, context):
        # # Getting the request params
        # try:
        #     account_email_id = request.account_email_id
        #     requested_at = request.requested_at
        # except Exception as err:
        #     account_email_id = None
        #     requested_at = None
        #     logger.error("request, exception: {}".format(str(err)))
        # # Some helper flags
        # account_claimable = False
        # account_exists = None
        #
        # # Validate email id
        # account_validated = validate_email_dns(account_email_id, check_mx=False, verify=False)
        #
        # # Generate Session Token
        # onboard_session_token = str(uuid.uuid4())
        # Registry.register_data(onboard_session_token, [account_email_id, requested_at, onboard_session_token])
        #
        # # check account exists in the accounts db
        # try:
        #     if account_validated and account_validated is not None:
        #         with DbSession.session_scope() as session:
        #             # Fetch the records
        #             exists_statement = exists().where(Account.account_email_id == account_email_id)
        #             result_set = session.query(Account).filter(exists_statement)
        #             session.commit()
        #             # Verify among the existing users
        #             for record in result_set:
        #                 if record.account_email_id == account_email_id:
        #                     logging.info(
        #                         f"Warning: re-onboard req by existing user, {record.account_id} at {requested_at}.")
        #                     account_exists = True
        #             if account_exists is not True and account_exists is None:
        #                 account_exists = False
        # except SQLAlchemyError as err:
        #     logger.error("SQLAlchemyError {}".format(str(err)))
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #
        # # Generate the boolean feedback about the claimability
        # if account_validated and not account_exists:
        #     account_claimable = True
        #
        # if account_claimable:
        #
        #     # Genreate the code, timing, token and register
        #     verification_code, code_generated_at = get_random_string(6)
        #     code_token = str(uuid.uuid4())
        #     code_generated_at = format_time2timestamp(code_generated_at)
        #     Registry.register_data(code_token, [verification_code, code_generated_at])
        #
        #     # Mail the onboarding account with Email Verification Token
        #     mail_successful = mail(
        #         from_email=identity_service_mail_id,
        #         to_email=account_email_id,
        #         subject=claim_account_verification_mail_subject,
        #         html_content=claim_account_verification_mail_body.format(verification_code)
        #     )
        #
        #     # Send back the response to client
        #     claim_account_response = ClaimAccountResponse(
        #         account_claimable=True,
        #         account_email_id=account_email_id,
        #         verification_code_token=code_token,
        #         onboard_session_token=onboard_session_token,
        #         code_sent_at=code_generated_at
        #     )
        #     logger.info(MessageToDict(claim_account_response, including_default_value_fields=True,
        #                               preserving_proto_field_name=True))
        #     return claim_account_response
        #
        # else:
        #
        #     # Send the response back to client with No Code Token, Not Claimable
        #     claim_account_response = ClaimAccountResponse(
        #         account_claimable=False,
        #         account_email_id=account_email_id,
        #         verification_code_token="NA",
        #         onboard_session_token=onboard_session_token,
        #         code_sent_at=format_time2timestamp(0)
        #     )
        #     logger.info(MessageToDict(claim_account_response, including_default_value_fields=True,
        #                               preserving_proto_field_name=True))
        #     return claim_account_response
        #
        # TODO: Temporary Response
        onboard_account_response = OnboardAccountResponse(
            account_details=request.account_details,
            account_onboard_status=AccountOnboardStatus(),
            verification_code_token_details=TemporaryTokenDetails(),
            onboard_session_token_details=PersistentSessionTokenDetails(),
            code_sent_at=format_time2timestamp(0)
        )
        return onboard_account_response

    # def ReRequestCodeClaimingAccount(self, request, context):
    #     # Get the data parameters from the request
    #     try:
    #         account_email_id = request.account_email_id
    #         generated_verification_code_token = request.generated_verification_code_token
    #         onboard_session_token = request.onboard_session_token
    #         requested_at = request.requested_at
    #     except Exception as err:
    #         account_email_id = None
    #         generated_verification_code_token = None
    #         onboard_session_token = None
    #         requested_at = None
    #         logger.error("request, exception: {}".format(str(err)))
    #     # Remove the old verification token from the registry
    #     Registry.delete_data(generated_verification_code_token)
    #     # Generate a new verification_code, code_token, generated_at
    #     verification_code, code_generated_at = get_random_string(6)
    #     code_token = str(uuid.uuid4())
    #     code_generated_at = format_time2timestamp(code_generated_at)
    #     Registry.register_data(code_token, [verification_code, code_generated_at])
    #     mail_successful = mail(
    #         from_email=identity_service_mail_id,
    #         to_email=account_email_id,
    #         subject=claim_account_verification_mail_subject,
    #         html_content=claim_account_verification_mail_body.format(verification_code)
    #     )
    #     return ReRequestCodeClaimingAccountResponse(
    #         account_email_id=account_email_id,
    #         verification_code_token=code_token,
    #         onboard_session_token=onboard_session_token,
    #         code_sent_at=code_generated_at
    #     )

    def VerifyOnboardingAccount(self, request, context):
        verify_onboarding_account_response = VerifyOnboardingAccountResponse(
            account_details=request.account_details,
            account_verified=True,
            verification_message="Successfully Verified",
            onboard_session_token_details=PersistentSessionTokenDetails(),
            onboard_organization_name="SELF",
            verified_at=format_time2timestamp(0)
        )
        return verify_onboarding_account_response

    def AuthenticateOnboardedAccount(self, request, context):
        authenticate_onboarded_account_response = AuthenticateOnboardedAccountResponse(
            account_details=request.account_details,
            account_authenticated=True,
            onboard_session_token_details=PersistentSessionTokenDetails(),
            authenticated_at=format_time2timestamp(0)
        )
        return authenticate_onboarded_account_response

    def AccessAccountEthosIdentityToken(self, request, context):
        access_account_ethos_identity_token_response = AccessAccountEthosIdentityTokenResponse(
            account_details=request.account_details,
            onboard_session_token_details=PersistentSessionTokenDetails(),
            identity_access_session_token_details=PersistentSessionTokenDetails()
        )
        return access_account_ethos_identity_token_response
