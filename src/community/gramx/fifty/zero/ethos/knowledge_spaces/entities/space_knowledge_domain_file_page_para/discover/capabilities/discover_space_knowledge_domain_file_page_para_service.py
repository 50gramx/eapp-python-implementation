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
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page_para.discover_space_knowledge_domain_file_page_para_pb2 import \
    ListOfParaIds, GetParaTextByIdRes, GetParaByIdResponse
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page_para.discover_space_knowledge_domain_file_page_para_pb2_grpc import \
    DiscoverSpaceKnowledgeDomainFilePageParaServiceServicer

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.access.consumers.access_space_knowledge_domain_consumer import \
    AccessSpaceKnowledgeDomainConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page.discover.consumers.discover_space_knowledge_domain_file_page_consumer import \
    DiscoverSpaceKnowledgeDomainFilePageConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.models.knowledge_space_models import DomainKnowledgeSpace


class DiscoverSpaceKnowledgeDomainFilePageParaService(DiscoverSpaceKnowledgeDomainFilePageParaServiceServicer):
    def __init__(self):
        self.session_scope = self.__class__.__name__
        super(DiscoverSpaceKnowledgeDomainFilePageParaService, self).__init__()

    def GetAllParaIds(self, request, context):
        logging.info("DiscoverSpaceKnowledgeDomainFilePageParaService:GetAllParaIds")
        domain_access_consumer = AccessSpaceKnowledgeDomainConsumer
        validation_done, validation_message = domain_access_consumer.validate_space_knowledge_domain_services(request)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return ListOfParaIds(response_meta=meta)
        else:
            domain_knowledge_space = DomainKnowledgeSpace(
                space_knowledge_id=request.space_knowledge_domain.space_knowledge.space_knowledge_id,
                space_knowledge_domain_id=request.space_knowledge_domain.space_knowledge_domain_id)
            list_of_page_para_text_ids = domain_knowledge_space.get_para_text_all_id()
            return ListOfParaIds(space_knowledge_domain_file_page_para_ids=list_of_page_para_text_ids,
                                 response_meta=meta)

    def GetParaTextById(self, request, context):
        logging.info("DiscoverSpaceKnowledgeDomainFilePageParaService:GetParaTextById")
        domain_access_consumer = AccessSpaceKnowledgeDomainConsumer
        validation_done, validation_message = domain_access_consumer.validate_space_knowledge_domain_services(
            request.access_auth_details)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetParaTextByIdRes(response_meta=meta)
        else:
            domain_knowledge_space = DomainKnowledgeSpace(
                space_knowledge_id=request.access_auth_details.space_knowledge_domain.space_knowledge.space_knowledge_id,
                space_knowledge_domain_id=request.access_auth_details.space_knowledge_domain.space_knowledge_domain_id)
            para_text = domain_knowledge_space.get_para_text_by_id(
                para_id=request.space_knowledge_domain_file_page_para_id)
            return GetParaTextByIdRes(para_text=para_text, response_meta=meta)

    def GetParaById(self, request, context):
        logging.info("DiscoverSpaceKnowledgeDomainFilePageParaService:GetParaById")
        domain_access_consumer = AccessSpaceKnowledgeDomainConsumer
        validation_done, validation_message = domain_access_consumer.validate_space_knowledge_domain_services(
            request.access_auth_details)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetParaByIdResponse(response_meta=meta)
        else:
            logging.info(f"DEBUG:: {request}")
            space_knowledge_domain = request.access_auth_details.space_knowledge_domain
            space_knowledge = space_knowledge_domain.space_knowledge
            domain_knowledge_space = DomainKnowledgeSpace(
                space_knowledge_id=space_knowledge.space_knowledge_id,
                space_knowledge_domain_id=space_knowledge_domain.space_knowledge_domain_id)
            logging.info(f"DEBUG: para_id: {request.space_knowledge_domain_file_page_para_id}")
            page_id = domain_knowledge_space.get_page_id_with_para_id(
                para_id=request.space_knowledge_domain_file_page_para_id)
            logging.info(f"DEBUG: page_id: {page_id}")
            page_discover_consumer = DiscoverSpaceKnowledgeDomainFilePageConsumer
            _, _, page = page_discover_consumer.get_page_by_id(
                access_auth_details=request.access_auth_details,
                space_knowledge_domain_file_page_id=page_id)
            para = domain_knowledge_space.get_para_with_id(
                para_id=request.space_knowledge_domain_file_page_para_id,
                space_knowledge_domain_file_page=page)
            return GetParaByIdResponse(space_knowledge_domain_file_page_para=para, response_meta=meta)
