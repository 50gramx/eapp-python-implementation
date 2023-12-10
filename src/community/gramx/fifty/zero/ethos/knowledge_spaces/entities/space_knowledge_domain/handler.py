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
from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2_grpc import \
    add_AccessSpaceKnowledgeDomainServiceServicer_to_server
from ethos.elint.services.product.knowledge.space_knowledge_domain.create_space_knowledge_domain_pb2_grpc import \
    add_CreateSpaceKnowledgeDomainServiceServicer_to_server
from ethos.elint.services.product.knowledge.space_knowledge_domain.discover_space_knowledge_domain_pb2_grpc import \
    add_DiscoverSpaceKnowledgeDomainServiceServicer_to_server

from application_context import ApplicationContext


def handle_space_knowledge_domain_services(server):
    add_AccessSpaceKnowledgeDomainServiceServicer_to_server(
        ApplicationContext.get_access_space_knowledge_domain_service(), server
    )
    add_CreateSpaceKnowledgeDomainServiceServicer_to_server(
        ApplicationContext.get_create_space_knowledge_domain_service(), server
    )
    add_DiscoverSpaceKnowledgeDomainServiceServicer_to_server(
        ApplicationContext.get_discover_space_knowledge_domain_service(), server
    )
