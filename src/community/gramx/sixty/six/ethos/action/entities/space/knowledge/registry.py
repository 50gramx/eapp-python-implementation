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
from community.gramx.sixty.six.ethos.action.entities.space.knowledge.capabilities.space_knowledge_action_service import \
    SpaceKnowledgeActionService
from support.application.registry import Registry


def register_space_knowledge_action_services(aio: bool):
    if aio:
        pass
    else:
        space_knowledge_action_service = SpaceKnowledgeActionService()
        Registry.register_service('space_knowledge_action_service', space_knowledge_action_service)
