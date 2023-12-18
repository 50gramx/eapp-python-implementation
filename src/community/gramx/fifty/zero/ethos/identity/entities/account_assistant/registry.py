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

from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.access.capabilities.access_account_assistant_service import \
    AccessAccountAssistantService
from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.action.capabilities.action_account_assistant_service import \
    ActionAccountAssistantService
from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.connect.capabilities.connect_account_assistant_service import \
    ConnectAccountAssistantService
from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.create.capabilities.create_account_assistant_service import \
    CreateAccountAssistantService
from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.discover.capabilities.discover_account_assistant_service import \
    DiscoverAccountAssistantService
from support.application.registry import Registry


def register_account_assistant_services(aio: bool):
    if aio:
        action_account_assistant_service = ActionAccountAssistantService()
        Registry.register_service('action_account_assistant_service', action_account_assistant_service)
    else:
        access_account_assistant_service = AccessAccountAssistantService()
        Registry.register_service('access_account_assistant_service', access_account_assistant_service)
        create_account_assistant_service = CreateAccountAssistantService()
        Registry.register_service('create_account_assistant_service', create_account_assistant_service)
        connect_account_assistant_service = ConnectAccountAssistantService()
        Registry.register_service('connect_account_assistant_service', connect_account_assistant_service)
        discover_account_assistant_service = DiscoverAccountAssistantService()
        Registry.register_service('discover_account_assistant_service', discover_account_assistant_service)
    return
