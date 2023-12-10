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
from ethos.elint.services.product.knowledge.space_knowledge.discover_space_knowledge_pb2 import \
    GetInferredSpaceKnowledgeDomainsResponse, GetSpaceKnowledgeDomainsResponse, GetSpaceKnowledgeDomainByIdResponse
from ethos.elint.services.product.knowledge.space_knowledge.discover_space_knowledge_pb2_grpc import \
    DiscoverSpaceKnowledgeServiceServicer

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge.access.consumers. \
    access_space_knowledge_consumer import AccessSpaceKnowledgeConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.models.knowledge_space_models import KnowledgeSpace


class DiscoverSpaceKnowledgeService(DiscoverSpaceKnowledgeServiceServicer):
    def __init__(self):
        super(DiscoverSpaceKnowledgeService, self).__init__()
        self.session_scope = self.__class__.__name__

    def GetInferredSpaceKnowledgeDomains(self, request, context):
        # todo: update this service
        logging.info("DiscoverSpaceKnowledgeService:GetInferredSpaceKnowledgeDomains")
        validate_done, validate_message = AccessSpaceKnowledgeConsumer.validate_space_knowledge_services(
            access_auth_details=request)
        meta = ResponseMeta(
            meta_done=validate_done,
            meta_message=validate_message)
        if validate_done is False:
            return GetInferredSpaceKnowledgeDomainsResponse(response_meta=meta)
        else:
            # get all inferred domains
            knowledge_space = KnowledgeSpace(space_knowledge_id=request.space_knowledge.space_knowledge_id)
            list_of_all_inferred_domains = knowledge_space.get_inferred_domain_all()
            return GetInferredSpaceKnowledgeDomainsResponse(
                space_knowledge_domain_inferred=list_of_all_inferred_domains, response_meta=meta)

    def GetSpaceKnowledgeDomains(self, request, context):
        logging.info("DiscoverSpaceKnowledgeService:GetSpaceKnowledgeDomains")
        validation_done, validation_message = AccessSpaceKnowledgeConsumer.validate_space_knowledge_services(
            access_auth_details=request)
        meta = ResponseMeta(
            meta_done=validation_done,
            meta_message=validation_message)
        if validation_done is False:
            return GetSpaceKnowledgeDomainsResponse(response_meta=meta)
        else:
            # get all domains
            knowledge_space = KnowledgeSpace(space_knowledge_id=request.space_knowledge.space_knowledge_id)
            space_knowledge_domains = knowledge_space.get_domain_all(space_knowledge=request.space_knowledge)
            return GetSpaceKnowledgeDomainsResponse(
                space_knowledge_domains=space_knowledge_domains, response_meta=meta)

    def GetSpaceKnowledgeDomainById(self, request, context):
        validation_done, validation_message = AccessSpaceKnowledgeConsumer.validate_space_knowledge_services(
            access_auth_details=request.access_auth)
        meta = ResponseMeta(
            meta_done=validation_done,
            meta_message=validation_message)
        if validation_done is False:
            return GetSpaceKnowledgeDomainByIdResponse(response_meta=meta)
        else:
            space_knowledge = request.access_auth.space_knowledge
            knowledge_space = KnowledgeSpace(
                space_knowledge_id=space_knowledge.space_knowledge_id)
            space_knowledge_domain = knowledge_space.get_domain_with_id(
                space_knowledge=space_knowledge,
                domain_id=request.space_knowledge_domain_id)
            return GetSpaceKnowledgeDomainByIdResponse(
                space_knowledge_domain=space_knowledge_domain,
                response_meta=meta
            )
