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

from ethos.elint.entities.space_knowledge_domain_pb2 import (
    RankedAnswer,
    SpaceKnowledgeDomain,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2 import (
    SpaceKnowledgeDomainServicesAccessAuthDetails,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain.discover_space_knowledge_domain_pb2 import (
    GetAllDomainFilesResponse,
    GetBestAnswersRequest,
)

from application_context import ApplicationContext


class DiscoverSpaceKnowledgeDomainConsumer:

    @staticmethod
    def get_all_domain_files(
        skd_auth: SpaceKnowledgeDomainServicesAccessAuthDetails,
    ) -> GetAllDomainFilesResponse:
        stub = ApplicationContext.discover_space_knowledge_domain_service_stub()
        logging.info(
            f"DiscoverSpaceKnowledgeDomainConsumer:get_all_domain_files: {stub}"
        )
        logging.info(
            f"DiscoverSpaceKnowledgeDomainConsumer:get_all_domain_files: {type(stub)}"
        )
        response = stub.GetAllDomainFiles(skd_auth)
        return response

    @staticmethod
    def get_updated_domain(
        access_auth_details: SpaceKnowledgeDomainServicesAccessAuthDetails,
    ) -> SpaceKnowledgeDomain:
        stub = ApplicationContext.discover_space_knowledge_domain_service_stub()
        response = stub.GetUpdatedDomain(access_auth_details)
        return response

    @staticmethod
    def get_best_answers(
        access_auth_details: SpaceKnowledgeDomainServicesAccessAuthDetails,
        best_answers_count: int,
        question: str,
    ) -> (bool, str, [RankedAnswer]):
        stub = ApplicationContext.discover_space_knowledge_domain_service_stub()
        request = GetBestAnswersRequest(
            access_auth_details=access_auth_details,
            best_answers_count=best_answers_count,
            question=question,
        )
        response = stub.GetBestAnswers(request)
        return (
            response.response_meta.meta_done,
            response.response_meta.meta_message,
            response.ranked_answers,
        )
