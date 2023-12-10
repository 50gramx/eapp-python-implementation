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
from ethos.elint.services.product.knowledge.space_knowledge_domain_file.delete_space_knowledge_domain_file_pb2_grpc import \
    DeleteSpaceKnowledgeDomainFileServiceServicer

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.access.consumers.access_space_knowledge_domain_consumer import \
    AccessSpaceKnowledgeDomainConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file.access.consumers.access_space_knowledge_domain_file_consumer import \
    AccessSpaceKnowledgeDomainFileConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file.delete.consumers.delete_space_knowledge_domain_file_consumer import \
    DeleteSpaceKnowledgeDomainFileConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.models.knowledge_space_models import KnowledgeSpace, \
    DomainKnowledgeSpace
from support.data_store import DataStore


class DeleteSpaceKnowledgeDomainFileService(DeleteSpaceKnowledgeDomainFileServiceServicer):
    def __init__(self):
        self.session_scope = self.__class__.__name__
        super(DeleteSpaceKnowledgeDomainFileService, self).__init__()

    def DeleteSpaceKnowledgeDomainFile(self, request, context):
        logging.info("DeleteSpaceKnowledgeDomainFileService:DeleteSpaceKnowledgeDomainFile")
        validation_done, validation_message = AccessSpaceKnowledgeDomainConsumer.validate_space_knowledge_domain_services(
            request.space_knowledge_domain_services_access_auth_details)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return meta
        else:
            space_knowledge_domain = request.space_knowledge_domain_services_access_auth_details.space_knowledge_domain
            space_knowledge = space_knowledge_domain.space_knowledge
            # access file services
            _, _, file_services_access_auth_details = AccessSpaceKnowledgeDomainFileConsumer.space_knowledge_domain_file_access_token(
                request.space_knowledge_domain_services_access_auth_details, request.space_knowledge_domain_file)
            # delete PagesForFile
            _, _ = DeleteSpaceKnowledgeDomainFileConsumer.delete_pages_for_file(file_services_access_auth_details)
            # delete file from data store
            data_store_client = DataStore()
            data_store_client.delete_space_knowledge_domain_file(
                space_knowledge_domain_file=request.space_knowledge_domain_file)
            # delete file
            domain_knowledge_space = DomainKnowledgeSpace(
                space_knowledge_id=space_knowledge.space_knowledge_id,
                space_knowledge_domain_id=space_knowledge_domain.space_knowledge_domain_id)
            domain_knowledge_space.delete_file_by_id(
                file_id=request.space_knowledge_domain_file.space_knowledge_domain_file_id)
            KnowledgeSpace(
                space_knowledge_id=space_knowledge.space_knowledge_id
            ).update_domain_last_updated_at(
                space_knowledge_domain_id=space_knowledge_domain.space_knowledge_domain_id
            )
            return meta
