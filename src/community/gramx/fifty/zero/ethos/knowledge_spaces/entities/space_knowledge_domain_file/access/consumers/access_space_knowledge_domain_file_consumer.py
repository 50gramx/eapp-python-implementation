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
from ethos.elint.entities import space_knowledge_domain_file_pb2
from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2 import \
    SpaceKnowledgeDomainServicesAccessAuthDetails
from ethos.elint.services.product.knowledge.space_knowledge_domain_file.access_space_knowledge_domain_file_pb2 import \
    SpaceKnowledgeDomainFileServicesAccessAuthDetails, SpaceKnowledgeDomainFileAccessTokenRequest

from application_context import ApplicationContext


class AccessSpaceKnowledgeDomainFileConsumer:

    @staticmethod
    def space_knowledge_domain_file_access_token(
            access_auth_details: SpaceKnowledgeDomainServicesAccessAuthDetails,
            space_knowledge_domain_file: space_knowledge_domain_file_pb2.SpaceKnowledgeDomainFile
    ) -> (bool, str, SpaceKnowledgeDomainFileServicesAccessAuthDetails):
        request = SpaceKnowledgeDomainFileAccessTokenRequest(
            space_knowledge_domain_services_access_auth_details=access_auth_details,
            space_knowledge_domain_file=space_knowledge_domain_file)
        stub = ApplicationContext.access_space_knowledge_domain_file_service_stub()
        response = stub.SpaceKnowledgeDomainFileAccessToken(request)
        return (response.space_knowledge_domain_file_services_access_done,
                response.space_knowledge_domain_file_services_access_message,
                response.space_knowledge_domain_file_services_access_auth_details)

    @staticmethod
    def validate_space_knowledge_domain_file_services(
            access_auth_details: SpaceKnowledgeDomainFileServicesAccessAuthDetails) -> (bool, str):
        stub = ApplicationContext.access_space_knowledge_domain_file_service_stub()
        response = stub.ValidateSpaceKnowledgeDomainFileServices(access_auth_details)
        return (response.space_knowledge_domain_file_services_access_validation_done,
                response.space_knowledge_domain_file_services_access_validation_message)
