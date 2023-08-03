import logging

from ethos.elint.entities.generic_pb2 import ResponseMeta, TemporaryTokenDetails
from ethos.elint.services.product.identity.multiverse.access_multiverse_pb2 import ValidateCoreCollaboratorResponse, \
    VerifyCoreCollaboratorResponse
from ethos.elint.services.product.identity.universe.access_universe_pb2_grpc import AccessUniverseServiceServicer
from support.db_service import is_existing_core_collaborator
from support.helper_functions import get_random_string, gen_uuid, get_current_timestamp, get_future_timestamp, mail
from support.redis_service import set_kv, get_kv
from support.session_manager import create_core_collaborator_access_auth_details, \
    update_persistent_session_last_requested_at, create_multiverse_services_access_auth_details, \
    is_persistent_session_valid


class AccessUniverseService(AccessUniverseServiceServicer):
    def __init__(self):
        super(AccessUniverseService, self).__init__()
        self.session_scope = self.__class__.__name__

    def UniverseAccessToken(self, request, context):
        pass

    def ValidateCoreCollaborator(self, request, context):
        logging.info("AccessUniverseService:ValidateCoreCollaborator")
        # fetch request params
        f_name = request.core_collaborator.collaborator_name.first_name
        l_name = request.core_collaborator.collaborator_name.last_name
        c_code = request.core_collaborator.community_domain_code
        # check if exists
        core_collaborator_exists = is_existing_core_collaborator(
            collaborator_first_name=f_name,
            collaborator_last_name=l_name,
            collaborator_community_code=c_code
        )
        if not core_collaborator_exists:
            response_meta = ResponseMeta(
                meta_done=False,
                meta_message="Core Collaborator doesn't exists."
            )
            validate_core_collaborator_response = ValidateCoreCollaboratorResponse(
                core_collaborator_exists=core_collaborator_exists,
                response_meta=response_meta
            )
        else:
            # send otp
            verification_code = get_random_string(6)
            code_token = gen_uuid()
            code_generated_at = get_current_timestamp()
            # send the code to email
            message = f"50GRAMX: Your security code is: {verification_code}. " \
                      f"It expires in 10 minutes. Don't share this code with anyone."
            code_sent_at = mail(from_email="no-reply-identity-multiverse@50gramx.com",
                                to_email=f"{f_name}.{l_name}.{c_code}@50gramx.io",
                                subject="Validate Core Developer - Access 50GRAMx Universe",
                                plain_text_content=message)
            # store the token details
            set_kv(code_token, verification_code)
            # create the code token details here
            verification_code_token_details = TemporaryTokenDetails(
                token=code_token,
                generated_at=code_generated_at,
                valid_till=get_future_timestamp(after_seconds=180)
            )
            response_meta = ResponseMeta(
                meta_done=True,
                meta_message="OTP Sent to the email address."
            )
            validate_core_collaborator_response = ValidateCoreCollaboratorResponse(
                core_collaborator_access_auth_details=create_core_collaborator_access_auth_details(
                    core_collaborator_name_code=f"{f_name}.{l_name}.{c_code}",
                    session_scope=self.session_scope
                ),
                core_collaborator_exists=core_collaborator_exists,
                verification_code_token_details=verification_code_token_details,
                code_sent_at=code_sent_at,
                response_meta=response_meta
            )
        return validate_core_collaborator_response

    def VerifyCoreCollaborator(self, request, context):
        logging.info("AccessUniverseService:VerifyCoreCollaborator")
        # get the request params here
        core_collaborator_access_auth_details = request.core_collaborator_access_auth_details
        resend_code = request.resend_code
        verification_code_token_details = request.verification_code_token_details
        verification_code = request.verification_code
        requested_at = request.requested_at

        # update the session here
        update_persistent_session_last_requested_at(
            core_collaborator_access_auth_details.core_collaborator_access_auth_session_token_details.session_token,
            requested_at)

        if not resend_code:
            # verify the code and return the status
            sent_verification_code = get_kv(verification_code_token_details.token)
            if verification_code == sent_verification_code:
                # verification successful
                verification_done = True
                verification_message = "Core Collaborator successfully verified."
                # access account id
                f_name, l_name, c_code = core_collaborator_access_auth_details.core_collaborator_name_code.split(".")
                account_service_access_auth_details = create_multiverse_services_access_auth_details(
                    collaborator_first_name=f_name,
                    collaborator_last_name=l_name,
                    collaborator_community_code=c_code,
                    session_scope=self.session_scope
                )
                response_meta = ResponseMeta(
                    meta_done=verification_done,
                    meta_message=verification_message
                )
                verify_core_collaborator_response = VerifyCoreCollaboratorResponse(
                    multiverse_service_access_auth_details=account_service_access_auth_details,
                    response_meta=response_meta
                )
            else:
                # verification failed
                response_meta = ResponseMeta(
                    meta_done=False,
                    meta_message="Verification failed. Please check the sent OTP and retry again."
                )
                verify_core_collaborator_response = VerifyCoreCollaboratorResponse(response_meta=response_meta)
        else:
            # resend the code and return the status
            new_verification_code = get_random_string(6)
            f_name, l_name, c_code = core_collaborator_access_auth_details.core_collaborator_name_code.split(".")
            message = f"50GRAMX: Your security code is: {new_verification_code}. " \
                      f"It expires in 10 minutes. Don't share this code with anyone."
            code_sent_at = mail(from_email="no-reply-identity-multiverse@50gramx.com",
                                to_email=f"{f_name}.{l_name}.{c_code}@50gramx.io",
                                subject="Validate Core Developer - Access 50GRAMx Universe",
                                plain_text_content=message)
            # create the response here
            response_meta = ResponseMeta(
                meta_done=False,
                meta_message="Code resent. Please verify to continue."
            )
            verify_core_collaborator_response = VerifyCoreCollaboratorResponse(response_meta=response_meta)
        return verify_core_collaborator_response

    def ValidateUniverseServices(self, request, context):
        logging.info("AccessUniverseService:ValidateUniverseServices")

        core_collaborator = request.core_collaborator
        multiverse_services_access_session_token_details = request.multiverse_services_access_session_token_details

        # validate the session
        core_collaborator_identifier = f"{core_collaborator.collaborator_name.first_name}." \
                                       f"{core_collaborator.collaborator_name.first_name}." \
                                       f"{core_collaborator.community_domain_code}"
        session_valid, session_valid_message = is_persistent_session_valid(
            multiverse_services_access_session_token_details.session_token,
            core_collaborator_identifier,
            self.session_scope
        )
        response_meta = ResponseMeta(
            meta_done=session_valid,
            meta_message=session_valid_message
        )
        return response_meta
