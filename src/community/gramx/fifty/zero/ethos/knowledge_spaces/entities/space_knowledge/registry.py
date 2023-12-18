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
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge.access.capabilities.access_space_knowledge_service import \
    AccessSpaceKnowledgeService
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge.create.capabilities.create_space_knowledge_service import \
    CreateSpaceKnowledgeService
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge.discover.capabilities.discover_space_knowledge_service import \
    DiscoverSpaceKnowledgeService
from support.application.registry import Registry


def register_space_knowledge_services(aio: bool):
    if aio:
        pass
    else:
        create_space_knowledge_service = CreateSpaceKnowledgeService()
        Registry.register_service('create_space_knowledge_service', create_space_knowledge_service)
        access_space_knowledge_service = AccessSpaceKnowledgeService()
        Registry.register_service('access_space_knowledge_service', access_space_knowledge_service)
        discover_space_knowledge_service = DiscoverSpaceKnowledgeService()
        Registry.register_service('discover_space_knowledge_service', discover_space_knowledge_service)
