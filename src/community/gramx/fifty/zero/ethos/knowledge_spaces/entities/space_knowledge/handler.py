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
from ethos.elint.services.product.knowledge.space_knowledge.access_space_knowledge_pb2_grpc import \
    add_AccessSpaceKnowledgeServiceServicer_to_server
from ethos.elint.services.product.knowledge.space_knowledge.create_space_knowledge_pb2_grpc import \
    add_CreateSpaceKnowledgeServiceServicer_to_server
from ethos.elint.services.product.knowledge.space_knowledge.discover_space_knowledge_pb2_grpc import \
    add_DiscoverSpaceKnowledgeServiceServicer_to_server

from application_context import ApplicationContext


def handle_space_knowledge_services(server):
    add_AccessSpaceKnowledgeServiceServicer_to_server(
        ApplicationContext.get_access_space_knowledge_service(), server
    )
    add_CreateSpaceKnowledgeServiceServicer_to_server(
        ApplicationContext.get_create_space_knowledge_service(), server
    )
    add_DiscoverSpaceKnowledgeServiceServicer_to_server(
        ApplicationContext.get_discover_space_knowledge_service(), server
    )
