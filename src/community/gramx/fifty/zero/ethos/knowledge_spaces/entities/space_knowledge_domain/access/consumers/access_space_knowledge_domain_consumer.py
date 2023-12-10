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
from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2 import \
    SpaceKnowledgeDomainServicesAccessAuthDetails, SpaceKnowledgeDomainAccessTokenRequest

from application_context import ApplicationContext


class AccessSpaceKnowledgeDomainConsumer:

    @staticmethod
    def space_knowledge_domain_access_token(
            access_auth_details: SpaceKnowledgeServicesAccessAuthDetails,
            space_knowledge_domain: SpaceKnowledgeDomain) -> (
            SpaceKnowledgeDomainServicesAccessAuthDetails, bool, str):
        stub = ApplicationContext.access_space_knowledge_domain_service_stub()
        response = stub.SpaceKnowledgeDomainAccessToken(SpaceKnowledgeDomainAccessTokenRequest(
            space_knowledge_services_access_auth_details=access_auth_details,
            space_knowledge_domain=space_knowledge_domain))
        return (response.space_knowledge_domain_services_access_auth_details,
                response.space_knowledge_domain_services_access_done,
                response.space_knowledge_domain_services_access_message)

    @staticmethod
    def validate_space_knowledge_domain_services(
            access_auth_details: SpaceKnowledgeDomainServicesAccessAuthDetails) -> (bool, str):
        stub = ApplicationContext.access_space_knowledge_domain_service_stub()
        response = stub.ValidateSpaceKnowledgeDomainServices(access_auth_details)
        return (response.space_knowledge_domain_services_access_validation_done,
                response.space_knowledge_domain_services_access_validation_message)
