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
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.access_space_knowledge_domain_file_page_pb2 import \
    SpaceKnowledgeDomainFilePageServicesAccessAuthDetails

from application_context import ApplicationContext


class DeleteSpaceKnowledgeDomainFilePageParaConsumer:

    @staticmethod
    def delete_paras_for_page(access_auth_details: SpaceKnowledgeDomainFilePageServicesAccessAuthDetails) -> (
            bool, str):
        stub = ApplicationContext.delete_space_knowledge_domain_file_page_para_service_stub()
        response = stub.DeleteParasForPage(access_auth_details)
        return response.meta_done, response.meta_message
