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
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.discover_space_knowledge_domain_file_page_pb2 import \
    ListOfPageIds, GetPageTextByIdRes, GetPageByIdResponse
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.discover_space_knowledge_domain_file_page_pb2_grpc import \
    DiscoverSpaceKnowledgeDomainFilePageServiceServicer

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.access.consumers.access_space_knowledge_domain_consumer import \
    AccessSpaceKnowledgeDomainConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.models.knowledge_space_models import DomainKnowledgeSpace


class DiscoverSpaceKnowledgeDomainFilePageService(DiscoverSpaceKnowledgeDomainFilePageServiceServicer):
    def __init__(self):
        self.session_scope = self.__class__.__name__
        super(DiscoverSpaceKnowledgeDomainFilePageService, self).__init__()

    def GetAllPageIds(self, request, context):
        logging.info("DiscoverSpaceKnowledgeDomainFilePageService:GetAllPageIds")
        domain_access_consumer = AccessSpaceKnowledgeDomainConsumer
        validation_done, validation_message = domain_access_consumer.validate_space_knowledge_domain_services(request)
        if validation_done is False:
            return ListOfPageIds(response_meta=ResponseMeta(meta_done=validation_done, meta_message=validation_message))
        else:
            domain_knowledge_space = DomainKnowledgeSpace(
                space_knowledge_id=request.space_knowledge_domain.space_knowledge.space_knowledge_id,
                space_knowledge_domain_id=request.space_knowledge_domain.space_knowledge_domain_id)
            list_of_page_text_ids = domain_knowledge_space.get_page_text_all_id()
            return ListOfPageIds(space_knowledge_domain_file_page_ids=list_of_page_text_ids,
                                 response_meta=ResponseMeta(meta_done=validation_done, meta_message=validation_message))

    def GetPageTextById(self, request, context):
        logging.info("DiscoverSpaceKnowledgeDomainFilePageService:GetPageTextById")
        domain_access_consumer = AccessSpaceKnowledgeDomainConsumer
        validation_done, validation_message = domain_access_consumer.validate_space_knowledge_domain_services(
            request.access_auth_details)
        if validation_done is False:
            return GetPageTextByIdRes(meta=ResponseMeta(meta_done=validation_done, meta_message=validation_message))
        else:
            domain_knowledge_space = DomainKnowledgeSpace(
                space_knowledge_id=request.access_auth_details.space_knowledge_domain.space_knowledge.space_knowledge_id,
                space_knowledge_domain_id=request.access_auth_details.space_knowledge_domain.space_knowledge_domain_id)
            page_text = domain_knowledge_space.get_page_text_by_id(page_id=request.space_knowledge_domain_file_page_id)
            return GetPageTextByIdRes(page_text=page_text, meta=ResponseMeta(
                meta_done=validation_done, meta_message=validation_message))

    def GetPageById(self, request, context):
        logging.info("DiscoverSpaceKnowledgeDomainFilePageService:GetPageById")
        domain_access_consumer = AccessSpaceKnowledgeDomainConsumer
        validation_done, validation_message = domain_access_consumer.validate_space_knowledge_domain_services(
            request.access_auth_details)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetPageByIdResponse(response_meta=meta)
        else:
            space_knowledge_domain = request.access_auth_details.space_knowledge_domain
            space_knowledge = space_knowledge_domain.space_knowledge
            domain_knowledge_space = DomainKnowledgeSpace(
                space_knowledge_id=space_knowledge.space_knowledge_id,
                space_knowledge_domain_id=space_knowledge_domain.space_knowledge_domain_id)
            file_id = domain_knowledge_space.get_file_id_with_page_id(
                page_id=request.space_knowledge_domain_file_page_id)
            space_knowledge_domain_file = domain_knowledge_space.get_file_with_id(
                space_knowledge_domain=space_knowledge_domain, file_id=file_id)
            space_knowledge_domain_file_page = domain_knowledge_space.get_page_with_id(
                space_knowledge_domain_file=space_knowledge_domain_file,
                page_id=request.space_knowledge_domain_file_page_id)
            return GetPageByIdResponse(space_knowledge_domain_file_page=space_knowledge_domain_file_page,
                                       response_meta=meta)
