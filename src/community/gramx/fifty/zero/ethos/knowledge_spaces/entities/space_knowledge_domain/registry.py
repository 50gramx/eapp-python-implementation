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
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.access.capabilities.access_space_knowledge_domain_service import \
    AccessSpaceKnowledgeDomainService
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.create.capabilities.create_space_knowledge_domain_service import \
    CreateSpaceKnowledgeDomainService
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.discover.capabilities.discover_space_knowledge_domain_service import \
    DiscoverSpaceKnowledgeDomainService
from support.application.registry import Registry


def register_space_knowledge_domain_services(aio: bool):
    if aio:
        pass
    else:
        create_space_knowledge_domain_service = CreateSpaceKnowledgeDomainService()
        Registry.register_service('create_space_knowledge_domain_service', create_space_knowledge_domain_service)
        access_space_knowledge_domain_service = AccessSpaceKnowledgeDomainService()
        Registry.register_service('access_space_knowledge_domain_service', access_space_knowledge_domain_service)
        discover_space_knowledge_domain_service = DiscoverSpaceKnowledgeDomainService()
        Registry.register_service('discover_space_knowledge_domain_service', discover_space_knowledge_domain_service)
