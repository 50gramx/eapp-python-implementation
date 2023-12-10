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

from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.access_space_knowledge_domain_file_page_pb2 import \
    SpaceKnowledgeDomainFilePageAccessTokenResponse, ValidateSpaceKnowledgeDomainFilePageServicesResponse
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.access_space_knowledge_domain_file_page_pb2_grpc import \
    AccessSpaceKnowledgeDomainFilePageServiceServicer

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file.access.consumers.access_space_knowledge_domain_file_consumer import \
    AccessSpaceKnowledgeDomainFileConsumer
from support.session_manager import create_space_knowledge_domain_file_page_services_access_auth_details, \
    is_persistent_session_valid


class AccessSpaceKnowledgeDomainFilePageService(AccessSpaceKnowledgeDomainFilePageServiceServicer):
    def __init__(self):
        super(AccessSpaceKnowledgeDomainFilePageService, self).__init__()
        self.session_scope = self.__class__.__name__

    def SpaceKnowledgeDomainFilePageAccessToken(self, request, context):
        logging.info("AccessSpaceKnowledgeDomainFilePageService:SpaceKnowledgeDomainFilePageAccessToken invoked.")
        space_knowledge_domain_file_page = request.space_knowledge_domain_file_page
        validation_done, validation_message = AccessSpaceKnowledgeDomainFileConsumer.validate_space_knowledge_domain_file_services(
            request.space_knowledge_domain_file_services_access_auth_details)
        if validation_done is False:
            return SpaceKnowledgeDomainFilePageAccessTokenResponse(access_done=validation_done,
                                                                   access_message=validation_message)
        else:
            access_auth_details = create_space_knowledge_domain_file_page_services_access_auth_details(
                session_scope=self.session_scope,
                space_knowledge_domain_file_page=space_knowledge_domain_file_page
            )
            return SpaceKnowledgeDomainFilePageAccessTokenResponse(access_auth_details=access_auth_details,
                                                                   access_done=validation_done,
                                                                   access_message=validation_message)

    def ValidateSpaceKnowledgeDomainFilePageServices(self, request, context):
        logging.info("AccessSpaceKnowledgeDomainFilePageService:ValidateSpaceKnowledgeDomainFilePageServices invoked.")
        session_valid, session_valid_message = is_persistent_session_valid(
            session_token=request.space_knowledge_domain_file_page_services_access_session_token_details.session_token,
            session_identifier=request.space_knowledge_domain_file_page.space_knowledge_domain_file_page_id,
            session_scope=self.session_scope)
        return ValidateSpaceKnowledgeDomainFilePageServicesResponse(
            space_knowledge_domain_file_page_services_access_validation_done=session_valid,
            space_knowledge_domain_file_page_services_access_validation_message=session_valid_message)
