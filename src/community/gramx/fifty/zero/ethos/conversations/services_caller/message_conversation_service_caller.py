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

from application_context import ApplicationContext
from ethos.elint.services.product.identity.account.access_account_pb2 import AccountServicesAccessAuthDetails
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails


def setup_account_conversations_caller(access_auth_details: AccountServicesAccessAuthDetails):
    stub = ApplicationContext.message_conversation_service_stub()
    response = stub.SetupAccountConversations(access_auth_details)
    return response.meta_done, response.meta_message


def setup_account_assistant_conversations_caller(access_auth_details: AccountAssistantServicesAccessAuthDetails):
    stub = ApplicationContext.message_conversation_service_stub()
    response = stub.SetupAccountAssistantConversations(access_auth_details)
    return response.meta_done, response.meta_message
