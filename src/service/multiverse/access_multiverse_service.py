import logging

from access.core_collaborator.authentication import AccessCommunityCollaboratorAuthentication
from access.multiverse.service_authentication import AccessMultiverseServicesAuthentication
from application_context import ApplicationContext
from ethos.elint.entities.generic_pb2 import ResponseMeta, TemporaryTokenDetails
from ethos.elint.services.product.identity.multiverse.access_multiverse_pb2 import ValidateCoreCollaboratorResponse, \
    VerifyCoreCollaboratorResponse
from ethos.elint.services.product.identity.multiverse.access_multiverse_pb2_grpc import AccessMultiverseServiceServicer
# from support.db_service import is_existing_core_collaborator
from support.helper_functions import get_random_string, gen_uuid, get_current_timestamp, get_future_timestamp, mail
from support.redis_service import set_kv, get_kv
from support.session_manager import update_persistent_session_last_requested_at, \
    is_persistent_session_valid


class AccessMultiverseService(AccessMultiverseServiceServicer):
    def __init__(self):
        super(AccessMultiverseService, self).__init__()
        self.session_scope = self.__class__.__name__

    def ValidateCoreCollaborator(self, request, context):
        logging.info("AccessMultiverseService:ValidateCoreCollaborator")
        # load from application context & pass the existing request and return based on the response
        community_collaborator_chain_services_stub = ApplicationContext.community_collaborator_chain_services_stub()
        if not community_collaborator_chain_services_stub.IsExistingCoreCollaborator(
                request.core_collaborator).meta_done:
            return ValidateCoreCollaboratorResponse(
                core_collaborator_exists=False,
                response_meta=ResponseMeta(
                    meta_done=False,
                    meta_message="Core Collaborator doesn't exists."
                )
            )
        else:
            # send otp
            verification_code = get_random_string(6)
            code_token = gen_uuid()
            code_generated_at = get_current_timestamp()
            # send the code to email
            f_name = request.core_collaborator.collaborator_name.first_name
            l_name = request.core_collaborator.collaborator_name.last_name
            c_code = request.core_collaborator.community_domain_code
            # --------------------------------
            message = f"50GRAMX: Your security code is: {verification_code}. " \
                      f"It expires in 10 minutes. Don't share this code with anyone."
            code_sent_at = mail(from_email="no-reply-identity-multiverse@50gramx.com",
                                to_email=f"{f_name}.{l_name}.{c_code}@50gramx.io",
                                subject="Validate Core Developer - Access 50GRAMx Multiverse",
                                plain_text_content=message)
            # store the token details
            set_kv(code_token, verification_code)
            # create the code token details here
            return ValidateCoreCollaboratorResponse(
                core_collaborator_access_auth_details=AccessCommunityCollaboratorAuthentication(
                    session_scope=self.session_scope,
                    core_collaborator_name_code=f"{f_name}.{l_name}.{c_code}"
                ).create_core_collaborator_authentication_details(),
                core_collaborator_exists=True,
                verification_code_token_details=TemporaryTokenDetails(
                    token=code_token,
                    generated_at=code_generated_at,
                    valid_till=get_future_timestamp(after_seconds=180)
                ),
                code_sent_at=code_sent_at,
                response_meta=ResponseMeta(
                    meta_done=True,
                    meta_message="OTP Sent to the email address."
                )
            )

    def VerifyCoreCollaborator(self, request, context):
        logging.info("AccessMultiverseService:VerifyCoreCollaborator")
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
                f_name, l_name, c_code = core_collaborator_access_auth_details.core_collaborator_name_code.split(".")
                return VerifyCoreCollaboratorResponse(
                    multiverse_service_access_auth_details=AccessMultiverseServicesAuthentication(
                        collaborator_first_name=f_name,
                        collaborator_last_name=l_name,
                        collaborator_community_code=c_code,
                        session_scope=self.session_scope
                    ).create_authentication_details(),
                    response_meta=ResponseMeta(
                        meta_done=True,
                        meta_message="Core Collaborator successfully verified."
                    )
                )
            else:
                return VerifyCoreCollaboratorResponse(
                    response_meta=ResponseMeta(
                        meta_done=False,
                        meta_message="Verification failed. Please check the sent OTP and retry again."
                    )
                )
        else:
            # resend the code and return the status
            new_verification_code = get_random_string(6)
            f_name, l_name, c_code = core_collaborator_access_auth_details.core_collaborator_name_code.split(".")
            message = f"50GRAMX: Your security code is: {new_verification_code}. " \
                      f"It expires in 10 minutes. Don't share this code with anyone."
            code_sent_at = mail(from_email="no-reply-identity-multiverse@50gramx.com",
                                to_email=f"{f_name}.{l_name}.{c_code}@50gramx.io",
                                subject="Validate Core Developer - Access 50GRAMx Multiverse",
                                plain_text_content=message)
            return VerifyCoreCollaboratorResponse(
                response_meta=ResponseMeta(
                    meta_done=False,
                    meta_message="Code resent. Please verify to continue."
                )
            )

    def ValidateMultiverseServices(self, request, context):
        logging.info("AccessMultiverseService:ValidateMultiverseServices")

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
        return ResponseMeta(
            meta_done=session_valid,
            meta_message=session_valid_message
        )
