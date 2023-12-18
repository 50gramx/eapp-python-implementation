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

from community.gramx.fifty.zero.ethos.conversations.entities.message.capabilities.account.capabilities.receive_account_message_service import \
    ReceiveAccountMessageService
from community.gramx.fifty.zero.ethos.conversations.entities.message.capabilities.account.capabilities.send_account_message_service import \
    SendAccountMessageService
from support.application.registry import Registry


def register_account_message_services(aio: bool):
    if aio:
        pass
    else:
        send_account_message_service = SendAccountMessageService()
        Registry.register_service('send_account_message_service', send_account_message_service)
        receive_account_message_service = ReceiveAccountMessageService()
        Registry.register_service('receive_account_message_service', receive_account_message_service)
