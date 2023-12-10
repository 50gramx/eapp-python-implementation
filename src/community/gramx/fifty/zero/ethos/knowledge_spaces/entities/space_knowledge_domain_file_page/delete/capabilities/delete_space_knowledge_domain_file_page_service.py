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
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.delete_space_knowledge_domain_file_page_pb2_grpc import \
    DeleteSpaceKnowledgeDomainFilePageServiceServicer

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file.access.consumers.access_space_knowledge_domain_file_consumer import \
    AccessSpaceKnowledgeDomainFileConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page.access.consumers.access_space_knowledge_domain_file_page_consumer import \
    AccessSpaceKnowledgeDomainFilePageConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page_para.delete.consumers.delete_space_knowledge_domain_file_page_para_consumer import \
    DeleteSpaceKnowledgeDomainFilePageParaConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.models.knowledge_space_models import DomainKnowledgeSpace
from support.data_store import DataStore


class DeleteSpaceKnowledgeDomainFilePageService(DeleteSpaceKnowledgeDomainFilePageServiceServicer):
    def __init__(self):
        self.session_scope = self.__class__.__name__
        super(DeleteSpaceKnowledgeDomainFilePageService, self).__init__()

    def DeletePagesForFile(self, request, context):
        logging.info("DeleteSpaceKnowledgeDomainFilePageService:DeletePagesForFile")
        consumer = AccessSpaceKnowledgeDomainFileConsumer
        validation_done, validation_message = consumer.validate_space_knowledge_domain_file_services(request)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return meta
        else:
            data_store_client = DataStore()
            space_knowledge_domain_file = request.space_knowledge_domain_file
            space_knowledge_domain = space_knowledge_domain_file.space_knowledge_domain
            space_knowledge_id = space_knowledge_domain.space_knowledge.space_knowledge_id
            domain_knowledge_space = DomainKnowledgeSpace(
                space_knowledge_id=space_knowledge_id,
                space_knowledge_domain_id=space_knowledge_domain.space_knowledge_domain_id)
            page_ids = domain_knowledge_space.get_all_page_id_with_file_id(
                file_id=space_knowledge_domain_file.space_knowledge_domain_file_id)
            for page_id in page_ids:
                # retrieve page with id
                page = domain_knowledge_space.get_page_with_id(
                    space_knowledge_domain_file=space_knowledge_domain_file, page_id=page_id)
                # get page services access
                page_access_consumer = AccessSpaceKnowledgeDomainFilePageConsumer
                _, _, page_access_auth_details = page_access_consumer.space_knowledge_domain_file_page_access_token(
                    access_auth_details=request, space_knowledge_domain_file_page=page)
                # delete ParasForPage
                para_delete_consumer = DeleteSpaceKnowledgeDomainFilePageParaConsumer
                _, _ = para_delete_consumer.delete_paras_for_page(access_auth_details=page_access_auth_details)
                # delete page from data store
                data_store_client.delete_space_knowledge_domain_file_page(space_knowledge_domain_file_page=page)
                # delete page text
                domain_knowledge_space.delete_page_text_by_id(page_id=page_id)
                # delete page
                domain_knowledge_space.delete_page_by_id(page_id=page_id)
            return meta
