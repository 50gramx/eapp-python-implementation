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
from ethos.elint.services.product.knowledge.space_knowledge_domain.create_space_knowledge_domain_pb2 import \
    CreateAccountWhiteSpaceKnowledgeDomainResponse, CreateSpaceKnowledgeDomainResponse
from ethos.elint.services.product.knowledge.space_knowledge_domain.create_space_knowledge_domain_pb2_grpc import \
    CreateSpaceKnowledgeDomainServiceServicer

from application_context import ApplicationContext
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge.access.consumers.access_space_knowledge_consumer import \
    AccessSpaceKnowledgeConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge.discover.consumers.discover_space_knowledge_consumer import \
    DiscoverSpaceKnowledgeConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.access.consumers.access_space_knowledge_domain_consumer import \
    AccessSpaceKnowledgeDomainConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.models.knowledge_space_models import DomainKnowledgeSpace, \
    KnowledgeSpace
from support.data_store import DataStore


class CreateSpaceKnowledgeDomainService(CreateSpaceKnowledgeDomainServiceServicer):
    def __init__(self):
        super(CreateSpaceKnowledgeDomainService, self).__init__()
        self.session_scope = self.__class__.__name__

    def CreateAccountWhiteSpaceKnowledgeDomain(self, request, context):
        logging.info("CreateSpaceKnowledgeDomainService:CreateAccountWhiteSpaceKnowledgeDomain invoked.")
        space_knowledge = request.space_knowledge
        validation_done, validation_message = AccessSpaceKnowledgeConsumer.validate_space_knowledge_services(request)
        if validation_done is False:
            return CreateAccountWhiteSpaceKnowledgeDomainResponse(
                create_account_white_space_knowledge_domain_done=validation_done,
                create_account_white_space_knowledge_domain_message=validation_done)
        else:
            data_store_client = DataStore()
            knowledge_space = KnowledgeSpace(space_knowledge_id=space_knowledge.space_knowledge_id)
            space_knowledge_domain_id = knowledge_space.add_new_domain(domain_name="My White Knowledge Domain",
                                                                       domain_description="My Information",
                                                                       domain_collar_enum=0, domain_isolate=True)
            # TODO: fix this
            knowledge_space.add_new_inferred_domain(space_knowledge_id=space_knowledge.space_knowledge_id,
                                                    space_knowledge_domain_id=space_knowledge_domain_id)
            domain_knowledge_space = DomainKnowledgeSpace(space_knowledge_id=space_knowledge.space_knowledge_id,
                                                          space_knowledge_domain_id=space_knowledge_domain_id)
            # TODO: fix this
            domain_knowledge_space.add_new_inferring_account(space_knowledge_id=space_knowledge.space_knowledge_id,
                                                             account_id=space_knowledge.space.space_admin_id)
            access_auth_details, access_done, access_message = AccessSpaceKnowledgeDomainConsumer.space_knowledge_domain_access_token(
                request)
            data_store_client.create_space_knowledge_domain(
                space_knowledge_domain=access_auth_details.space_knowledge_domain
            )
            return CreateAccountWhiteSpaceKnowledgeDomainResponse(
                space_knowledge_domain_services_access_auth_details=access_auth_details,
                create_account_white_space_knowledge_domain_done=access_done,
                create_account_white_space_knowledge_domain_message=access_message)

    def CreateSpaceKnowledgeDomain(self, request, context):
        logging.info("CreateSpaceKnowledgeDomainService:CreateSpaceKnowledgeDomain invoked.")
        validation_done, validation_message = AccessSpaceKnowledgeConsumer.validate_space_knowledge_services(
            access_auth_details=request.space_knowledge_services_access_auth_details)
        meta = ResponseMeta(
            meta_done=validation_done,
            meta_message=validation_message)
        if validation_done is False:
            return CreateSpaceKnowledgeDomainResponse(response_meta=meta)
        else:
            charge_for_closed_domain_launch_response = ApplicationContext.pay_in_account_service_stub().ChargeForClosedDomainLaunch(
                request.space_knowledge_services_access_auth_details)
            if charge_for_closed_domain_launch_response.meta_done is False:
                return CreateSpaceKnowledgeDomainResponse(response_meta=ResponseMeta(
                    meta_done=False, meta_message=charge_for_closed_domain_launch_response.meta_message))
            else:
                space_knowledge = request.space_knowledge_services_access_auth_details.space_knowledge
                knowledge_space = KnowledgeSpace(space_knowledge_id=space_knowledge.space_knowledge_id)
                new_domain_id = knowledge_space.add_new_domain(
                    domain_name=request.space_knowledge_domain_name,
                    domain_description=request.space_knowledge_domain_description,
                    domain_collar_enum=request.space_knowledge_domain_collar_enum,
                    domain_isolate=request.space_knowledge_domain_isolated,
                )
                _, _, space_knowledge_domain = DiscoverSpaceKnowledgeConsumer.get_space_knowledge_domain_by_id(
                    request.space_knowledge_services_access_auth_details, new_domain_id)
                domain_access_auth_details, _, _ = AccessSpaceKnowledgeDomainConsumer.space_knowledge_domain_access_token(
                    request.space_knowledge_services_access_auth_details,
                    space_knowledge_domain)
                return CreateSpaceKnowledgeDomainResponse(
                    space_knowledge_domain_services_access_auth_details=domain_access_auth_details,
                    response_meta=meta)
