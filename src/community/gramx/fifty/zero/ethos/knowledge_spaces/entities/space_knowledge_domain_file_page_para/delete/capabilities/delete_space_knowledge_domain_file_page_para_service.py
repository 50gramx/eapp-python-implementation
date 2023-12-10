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
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page_para.delete_space_knowledge_domain_file_page_para_pb2_grpc import \
    DeleteSpaceKnowledgeDomainFilePageParaServiceServicer

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page.access.consumers.access_space_knowledge_domain_file_page_consumer import \
    AccessSpaceKnowledgeDomainFilePageConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.models.knowledge_space_models import DomainKnowledgeSpace
from support.data_store import DataStore


class DeleteSpaceKnowledgeDomainFilePageParaService(DeleteSpaceKnowledgeDomainFilePageParaServiceServicer):
    def __init__(self):
        self.session_scope = self.__class__.__name__
        super(DeleteSpaceKnowledgeDomainFilePageParaService, self).__init__()

    def DeleteParasForPage(self, request, context):
        logging.info("DeleteSpaceKnowledgeDomainFilePageParaService:DeleteParasForPage")
        page_access_consumer = AccessSpaceKnowledgeDomainFilePageConsumer
        validation_done, validation_message = page_access_consumer.validate_space_knowledge_domain_file_page_services(
            request)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return meta
        else:
            page = request.space_knowledge_domain_file_page
            file = page.space_knowledge_domain_file
            domain = file.space_knowledge_domain
            knowledge = domain.space_knowledge
            # download the page from data store
            data_store_client = DataStore()
            data_store_client.download_space_knowledge_domain_file_page(space_knowledge_domain_file_page=page)
            tmp_page_filepath = data_store_client.get_tmp_page_filepath(page=page)
            domain_knowledge_space = DomainKnowledgeSpace(space_knowledge_id=knowledge.space_knowledge_id,
                                                          space_knowledge_domain_id=domain.space_knowledge_domain_id)
            # get all the paras
            para_ids = domain_knowledge_space.get_all_para_id_with_page_id(
                page_id=page.space_knowledge_domain_file_page_id)
            for para_id in para_ids:
                # delete all the para texts
                domain_knowledge_space.delete_para_text_by_id(para_id=para_id)
                # delete all the para qa_contexts
                domain_knowledge_space.delete_domain_qa_context_with_para_id(para_id=para_id)
                # delete all the para
                domain_knowledge_space.delete_para_by_id(para_id=para_id)
            return meta
