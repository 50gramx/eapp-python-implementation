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
from ethos.elint.entities.space_knowledge_domain_pb2 import SpaceKnowledgeDomain
from ethos.elint.services.product.knowledge.space_knowledge.access_space_knowledge_pb2 import (
    SpaceKnowledgeServicesAccessAuthDetails,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain.create_space_knowledge_domain_pb2 import (
    CreateSpaceKnowledgeDomainRequest,
    CreateSpaceKnowledgeDomainResponse,
)

from application_context import ApplicationContext


class CreateSpaceKnowledgeDomainConsumer:

    @staticmethod
    def create_space_knowledge_domain(
        kauth: SpaceKnowledgeServicesAccessAuthDetails,
        name: str,
        desc: str,
        cnum: int,
        isol: bool,
    ) -> CreateSpaceKnowledgeDomainResponse:
        stub = ApplicationContext.create_space_knowledge_domain_service_stub()
        request = CreateSpaceKnowledgeDomainRequest(
            space_knowledge_services_access_auth_details=kauth,
            space_knowledge_domain_name=name,
            space_knowledge_domain_description=desc,
            space_knowledge_domain_collar_enum=cnum,
            space_knowledge_domain_isolated=isol,
        )
        response = stub.CreateSpaceKnowledgeDomain(request)
        return response
