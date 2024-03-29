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

from ethos.elint.entities.space_knowledge_domain_file_page_para_pb2 import SpaceKnowledgeDomainFilePagePara
from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2 import \
    SpaceKnowledgeDomainServicesAccessAuthDetails
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page_para.discover_space_knowledge_domain_file_page_para_pb2 import \
    GetParaByIdRequest

from application_context import ApplicationContext


class DiscoverSpaceKnowledgeDomainFilePageParaConsumer:

    @staticmethod
    def get_para_by_id(access_auth_details: SpaceKnowledgeDomainServicesAccessAuthDetails,
                       space_knowledge_domain_file_page_para_id: str) -> (
            bool, str, SpaceKnowledgeDomainFilePagePara):
        stub = ApplicationContext.discover_space_knowledge_domain_file_page_para_service_stub()
        response = stub.GetParaById(GetParaByIdRequest(
            access_auth_details=access_auth_details,
            space_knowledge_domain_file_page_para_id=space_knowledge_domain_file_page_para_id))
        return (response.response_meta.meta_done,
                response.response_meta.meta_message,
                response.space_knowledge_domain_file_page_para)
