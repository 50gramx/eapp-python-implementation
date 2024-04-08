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
from ethos.elint.entities.space_knowledge_domain_file_page_pb2 import SpaceKnowledgeDomainFilePage
from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2 import \
    SpaceKnowledgeDomainServicesAccessAuthDetails
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.discover_space_knowledge_domain_file_page_pb2 import \
    GetPageByIdRequest
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.discover_space_knowledge_domain_file_page_pb2 import \
    GetPageTextByIdReq

from application_context import ApplicationContext


class DiscoverSpaceKnowledgeDomainFilePageConsumer:

    @staticmethod
    def get_page_by_id(access_auth_details: SpaceKnowledgeDomainServicesAccessAuthDetails,
                       space_knowledge_domain_file_page_id: str) -> (
            bool, str, SpaceKnowledgeDomainFilePage):
        stub = ApplicationContext.discover_space_knowledge_domain_file_page_service_stub()
        response = stub.GetPageById(GetPageByIdRequest(
            access_auth_details=access_auth_details,
            space_knowledge_domain_file_page_id=space_knowledge_domain_file_page_id))
        return (response.response_meta.meta_done,
                response.response_meta.meta_message,
                response.space_knowledge_domain_file_page)

    @staticmethod
    def get_page_text_by_id(access_auth_details: SpaceKnowledgeDomainServicesAccessAuthDetails,
                            page_id: str) -> (
            bool, str, str):
        stub = ApplicationContext.discover_space_knowledge_domain_file_page_service_stub()
        response = stub.GetPageTextById(
            GetPageTextByIdReq(access_auth_details=access_auth_details, space_knowledge_domain_file_page_id=page_id))
        return response.meta.meta_done, response.meta.meta_message, response.page_text
