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
import logging

from community.gramx.fifty.zero.ethos.conversations.entities.message.capabilities.account.handler import \
    handle_message_account_services
from community.gramx.fifty.zero.ethos.conversations.entities.message.capabilities.account_assistant.handler import \
    handle_message_account_assistant_services
from community.gramx.fifty.zero.ethos.conversations.entities.message.handler import handle_message_services


def handle_conversations_services(server):
    handle_message_services(server)
    logging.info(f'\t [x] added message services')
    handle_message_account_services(server)
    logging.info(f'\t [x] added account message services')
    handle_message_account_assistant_services(server)
    logging.info(f'\t [x] added account assistant message services')
    logging.info(f'Conversations services added')
