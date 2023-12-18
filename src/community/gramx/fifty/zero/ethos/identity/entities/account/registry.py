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
from community.gramx.fifty.zero.ethos.identity.entities.account.access.capabilities.access_account_service import \
    AccessAccountService
from community.gramx.fifty.zero.ethos.identity.entities.account.connect.capabilities.connect_account_service import \
    ConnectAccountService
from community.gramx.fifty.zero.ethos.identity.entities.account.create.capabilities.create_account_service import \
    CreateAccountService
from community.gramx.fifty.zero.ethos.identity.entities.account.discover.capabilities.discover_account_service import \
    DiscoverAccountService
from community.gramx.fifty.zero.ethos.identity.entities.account.notify.capabilities.notify_account_service import \
    NotifyAccountService
from community.gramx.fifty.zero.ethos.identity.entities.account.pay.capabiliities.pay_in_account_service import \
    PayInAccountService
from support.application.registry import Registry


def register_account_services(aio: bool):
    if aio:
        pass
    else:
        create_account_service = CreateAccountService()
        Registry.register_service('create_account_service', create_account_service)
        access_account_service = AccessAccountService()
        Registry.register_service('access_account_service', access_account_service)
        connect_account_service = ConnectAccountService()
        Registry.register_service('connect_account_service', connect_account_service)
        discover_account_service = DiscoverAccountService()
        Registry.register_service('discover_account_service', discover_account_service)
        pay_in_account_service = PayInAccountService()
        Registry.register_service('pay_in_account_service', pay_in_account_service)
        notify_account_service = NotifyAccountService()
        Registry.register_service('notify_account_service', notify_account_service)
    return
