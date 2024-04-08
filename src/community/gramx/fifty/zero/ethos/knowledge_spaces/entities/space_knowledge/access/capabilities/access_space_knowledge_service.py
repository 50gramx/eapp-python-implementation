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

from ethos.elint.services.product.knowledge.space_knowledge.access_space_knowledge_pb2 import \
    ValidateSpaceKnowledgeServicesResponse, SpaceKnowledgeAccessTokenResponse
from ethos.elint.services.product.knowledge.space_knowledge.access_space_knowledge_pb2_grpc import \
    AccessSpaceKnowledgeServiceServicer

from community.gramx.fifty.zero.ethos.identity.entities.space.access.consumers.access_space_consumer import AccessSpaceConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge.create. \
    consumers.create_space_knowledge_consumer import CreateAccountSpaceKnowledgeConsumer
from support.db_service import get_space_knowledge
from support.session_manager import create_space_knowledge_services_access_auth_details, is_persistent_session_valid


class AccessSpaceKnowledgeService(AccessSpaceKnowledgeServiceServicer):
    def __init__(self):
        super(AccessSpaceKnowledgeService, self).__init__()
        self.session_scope = self.__class__.__name__

    def SpaceKnowledgeAccessToken(self, request, context):
        logging.info("AccessSpaceKnowledgeService:SpaceKnowledgeAccessToken invoked.")
        validation_done, validation_message = AccessSpaceConsumer.validate_space_services(request)
        if validation_done is False:
            return SpaceKnowledgeAccessTokenResponse(
                space_knowledge_services_access_done=validation_done,
                space_knowledge_services_access_message=validation_message
            )
        else:
            space_knowledge = get_space_knowledge(space=request.space, with_space_id=request.space.space_id)
            if space_knowledge is None:
                # TODO: Change to access auth after updating contract
                create_response = CreateAccountSpaceKnowledgeConsumer.create_account_space_knowledge(request)
                space_knowledge = create_response.space_knowledge_services_access_auth_details.space_knowledge
            space_knowledge_services_access_auth_details = create_space_knowledge_services_access_auth_details(
                session_scope=self.session_scope, space_knowledge=space_knowledge)
            return SpaceKnowledgeAccessTokenResponse(
                space_knowledge_services_access_auth_details=space_knowledge_services_access_auth_details,
                space_knowledge_services_access_done=validation_done,
                space_knowledge_services_access_message=validation_message
            )

    def ValidateSpaceKnowledgeServices(self, request, context):
        logging.info("AccessSpaceKnowledgeService:ValidateSpaceKnowledgeServices invoked.")
        space_knowledge = request.space_knowledge
        space_knowledge_services_access_session_token_details = request. \
            space_knowledge_services_access_session_token_details

        # validate the space knowledge
        if not space_knowledge.space_knowledge_id == space_knowledge.space_knowledge_id:
            space_knowledge_services_access_validation_done = False
            space_knowledge_services_access_validation_message = "Requesting space knowledge is not legit. " \
                                                                 "This action will be reported."
            # create the response here
            validate_space_knowledge_services_response = ValidateSpaceKnowledgeServicesResponse(
                space_knowledge_services_access_validation_done=space_knowledge_services_access_validation_done,
                space_knowledge_services_access_validation_message=space_knowledge_services_access_validation_message
            )
            return validate_space_knowledge_services_response
        else:
            # validate the session
            session_valid, session_valid_message = is_persistent_session_valid(
                session_token=space_knowledge_services_access_session_token_details.session_token,
                session_identifier=space_knowledge.space_knowledge_id,
                session_scope=self.session_scope
            )
            # create the response here
            validate_space_knowledge_services_response = ValidateSpaceKnowledgeServicesResponse(
                space_knowledge_services_access_validation_done=session_valid,
                space_knowledge_services_access_validation_message=session_valid_message
            )
            return validate_space_knowledge_services_response
