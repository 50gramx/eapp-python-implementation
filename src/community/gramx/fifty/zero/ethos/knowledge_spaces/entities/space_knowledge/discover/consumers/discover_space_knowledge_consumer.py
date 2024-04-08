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
from ethos.elint.entities.space_knowledge_domain_pb2 import SpaceKnowledgeDomain
from ethos.elint.services.product.knowledge.space_knowledge.access_space_knowledge_pb2 import \
    SpaceKnowledgeServicesAccessAuthDetails
from ethos.elint.services.product.knowledge.space_knowledge.discover_space_knowledge_pb2 import \
    GetSpaceKnowledgeDomainByIdRequest

from application_context import ApplicationContext


class DiscoverSpaceKnowledgeConsumer:

    @staticmethod
    def get_space_knowledge_domain_by_id(access_auth_details: SpaceKnowledgeServicesAccessAuthDetails,
                                         space_knowledge_domain_id: str) -> (bool, str, SpaceKnowledgeDomain):
        stub = ApplicationContext.discover_space_knowledge_services_stub()
        response = stub.GetSpaceKnowledgeDomainById(GetSpaceKnowledgeDomainByIdRequest(
            access_auth=access_auth_details, space_knowledge_domain_id=space_knowledge_domain_id))
        return response.response_meta.meta_done, response.response_meta.meta_message, response.space_knowledge_domain

    @staticmethod
    def get_space_knowledge_domains(
            access_auth_details: SpaceKnowledgeServicesAccessAuthDetails) -> (bool, str, [SpaceKnowledgeDomain]):
        stub = ApplicationContext.discover_space_knowledge_services_stub()
        response = stub.GetSpaceKnowledgeDomains(access_auth_details)
        return response.response_meta.meta_done, response.response_meta.meta_message, response.space_knowledge_domains
