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

from ethos.elint.services.product.knowledge.space_knowledge_domain_file.access_space_knowledge_domain_file_pb2 import \
    SpaceKnowledgeDomainFileAccessTokenResponse, ValidateSpaceKnowledgeDomainFileServicesResponse
from ethos.elint.services.product.knowledge.space_knowledge_domain_file.access_space_knowledge_domain_file_pb2_grpc import \
    AccessSpaceKnowledgeDomainFileServiceServicer

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.access.consumers.access_space_knowledge_domain_consumer import \
    AccessSpaceKnowledgeDomainConsumer
from support.session_manager import create_space_knowledge_domain_file_services_access_auth_details, \
    is_persistent_session_valid


class AccessSpaceKnowledgeDomainFileService(AccessSpaceKnowledgeDomainFileServiceServicer):
    def __init__(self):
        super(AccessSpaceKnowledgeDomainFileService, self).__init__()
        self.session_scope = self.__class__.__name__

    def SpaceKnowledgeDomainFileAccessToken(self, request, context):
        logging.info("AccessSpaceKnowledgeDomainFileService:SpaceKnowledgeDomainFileAccessToken invoked.")
        # request params
        space_knowledge_domain_file = request.space_knowledge_domain_file
        validation_done, validation_message = AccessSpaceKnowledgeDomainConsumer. \
            validate_space_knowledge_domain_services(request.space_knowledge_domain_services_access_auth_details)
        if validation_done is False:
            return SpaceKnowledgeDomainFileAccessTokenResponse(
                space_knowledge_domain_file_services_access_done=validation_done,
                space_knowledge_domain_file_services_access_message=validation_message
            )
        else:
            auth_details = create_space_knowledge_domain_file_services_access_auth_details(
                session_scope=self.session_scope, space_knowledge_domain_file=space_knowledge_domain_file)
            return SpaceKnowledgeDomainFileAccessTokenResponse(
                space_knowledge_domain_file_services_access_auth_details=auth_details,
                space_knowledge_domain_file_services_access_done=validation_done,
                space_knowledge_domain_file_services_access_message=validation_message
            )

    def ValidateSpaceKnowledgeDomainFileServices(self, request, context):
        logging.info("AccessSpaceKnowledgeDomainFileService:ValidateSpaceKnowledgeDomainFileServices invoked.")
        session_valid, session_valid_message = is_persistent_session_valid(
            session_token=request.space_knowledge_domain_file_services_access_session_token_details.session_token,
            session_identifier=request.space_knowledge_domain_file.space_knowledge_domain_file_id,
            session_scope=self.session_scope)
        return ValidateSpaceKnowledgeDomainFileServicesResponse(
            space_knowledge_domain_file_services_access_validation_done=session_valid,
            space_knowledge_domain_file_services_access_validation_message=session_valid_message)
