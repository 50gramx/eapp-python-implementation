#   /*************************************************************************
#   *
#   * AMIT KUMAR KHETAN CONFIDENTIAL
#   * __________________
#   *
#   *  [2017] - [2024] Amit Kumar Khetan
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

from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.access_space_knowledge_domain_file_page_pb2 import \
    SpaceKnowledgeDomainFilePageServicesAccessAuthDetails

from application_context import ApplicationContext


class CreateSpaceKnowledgeDomainFilePageParaConsumer:

    @staticmethod
    def extract_paras_from_page(
            page_services_access_auth_details: SpaceKnowledgeDomainFilePageServicesAccessAuthDetails):
        # call the service to extract paras from page
        logging.info("Calling the service: ExtractParasFromPage")
        stub = ApplicationContext.create_space_knowledge_domain_file_page_para_service_stub()
        response_generator = stub.ExtractParasFromPage(
            page_services_access_auth_details
        )
        logging.info(response_generator)
        pass
