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

from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2 import \
    SpaceKnowledgeDomainAccessTokenResponse, ValidateSpaceKnowledgeDomainServicesResponse
from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2_grpc import \
    AccessSpaceKnowledgeDomainServiceServicer

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge.access.consumers. \
    access_space_knowledge_consumer import AccessSpaceKnowledgeConsumer
from support.session_manager import create_space_knowledge_domain_services_access_auth_details, \
    is_persistent_session_valid


class AccessSpaceKnowledgeDomainService(AccessSpaceKnowledgeDomainServiceServicer):
    def __init__(self):
        super(AccessSpaceKnowledgeDomainService, self).__init__()
        self.session_scope = self.__class__.__name__

    def SpaceKnowledgeDomainAccessToken(self, request, context):
        logging.info("AccessSpaceKnowledgeDomainService:SpaceKnowledgeDomainAccessToken invoked.")
        validation_done, validation_message = AccessSpaceKnowledgeConsumer.validate_space_knowledge_services(
            request.space_knowledge_services_access_auth_details)
        if validation_done is False:
            return SpaceKnowledgeDomainAccessTokenResponse(
                space_knowledge_domain_services_access_done=validation_done,
                space_knowledge_domain_services_access_message=validation_message)
        else:
            # knowledge_space = KnowledgeSpace(space_knowledge_id=space_knowledge.space_knowledge_id)
            # space_knowledge_domain = knowledge_space.get_domain_with_id(space_knowledge=space_knowledge, domain_id="")
            # if space_knowledge_domain is None:
            #     create_response = create_account_white_space_knowledge_domain_caller(request)
            #     space_knowledge_domain = create_response.space_knowledge_domain_services_\
            #           access_auth_details.space_knowledge_domain
            access_auth_details = create_space_knowledge_domain_services_access_auth_details(
                session_scope=self.session_scope, space_knowledge_domain=request.space_knowledge_domain)
            return SpaceKnowledgeDomainAccessTokenResponse(
                space_knowledge_domain_services_access_auth_details=access_auth_details,
                space_knowledge_domain_services_access_done=validation_done,
                space_knowledge_domain_services_access_message=validation_message
            )

    def ValidateSpaceKnowledgeDomainServices(self, request, context):
        logging.info("AccessSpaceKnowledgeDomainService:ValidateSpaceKnowledgeDomainServices invoked.")
        space_knowledge_domain = request.space_knowledge_domain
        space_knowledge_domain_services_access_session_token_details = request. \
            space_knowledge_domain_services_access_session_token_details
        session_valid, session_valid_message = is_persistent_session_valid(
            session_token=space_knowledge_domain_services_access_session_token_details.session_token,
            session_identifier=space_knowledge_domain.space_knowledge_domain_id,
            session_scope=self.session_scope
        )
        return ValidateSpaceKnowledgeDomainServicesResponse(
            space_knowledge_domain_services_access_validation_done=session_valid,
            space_knowledge_domain_services_access_validation_message=session_valid_message
        )
