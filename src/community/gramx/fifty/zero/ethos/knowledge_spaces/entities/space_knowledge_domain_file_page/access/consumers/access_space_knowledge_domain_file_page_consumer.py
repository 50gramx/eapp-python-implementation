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
from ethos.elint.entities import space_knowledge_domain_file_page_pb2
from ethos.elint.services.product.knowledge.space_knowledge_domain_file.access_space_knowledge_domain_file_pb2 import \
    SpaceKnowledgeDomainFileServicesAccessAuthDetails
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.access_space_knowledge_domain_file_page_pb2 import \
    SpaceKnowledgeDomainFilePageServicesAccessAuthDetails, SpaceKnowledgeDomainFilePageAccessTokenRequest

from application_context import ApplicationContext


class AccessSpaceKnowledgeDomainFilePageConsumer:

    @staticmethod
    def space_knowledge_domain_file_page_access_token(
            access_auth_details: SpaceKnowledgeDomainFileServicesAccessAuthDetails,
            space_knowledge_domain_file_page: space_knowledge_domain_file_page_pb2.SpaceKnowledgeDomainFilePage
    ) -> (bool, str, SpaceKnowledgeDomainFilePageServicesAccessAuthDetails):
        request = SpaceKnowledgeDomainFilePageAccessTokenRequest(
            space_knowledge_domain_file_services_access_auth_details=access_auth_details,
            space_knowledge_domain_file_page=space_knowledge_domain_file_page)
        stub = ApplicationContext.access_space_knowledge_domain_file_page_service_stub()
        response = stub.SpaceKnowledgeDomainFilePageAccessToken(request)
        return (response.access_done, response.access_message, response.access_auth_details)

    @staticmethod
    def validate_space_knowledge_domain_file_page_services(
            access_auth_details: SpaceKnowledgeDomainFilePageServicesAccessAuthDetails) -> (bool, str):
        stub = ApplicationContext.access_space_knowledge_domain_file_page_service_stub()
        response = stub.ValidateSpaceKnowledgeDomainFilePageServices(access_auth_details)
        return (response.space_knowledge_domain_file_page_services_access_validation_done,
                response.space_knowledge_domain_file_page_services_access_validation_message)
