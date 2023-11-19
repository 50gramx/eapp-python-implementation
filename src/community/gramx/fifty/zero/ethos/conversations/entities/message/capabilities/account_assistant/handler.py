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
from ethos.elint.services.product.conversation.message.account_assistant.receive_account_assistant_message_pb2_grpc import \
    add_ReceiveAccountAssistantMessageServiceServicer_to_server
from ethos.elint.services.product.conversation.message.account_assistant.send_account_assistant_message_pb2_grpc import \
    add_SendAccountAssistantMessageServiceServicer_to_server

from application_context import ApplicationContext


def handle_message_account_assistant_services(server):
    add_SendAccountAssistantMessageServiceServicer_to_server(
        ApplicationContext.get_send_account_assistant_message_service(), server
    )
    add_ReceiveAccountAssistantMessageServiceServicer_to_server(
        ApplicationContext.get_receive_account_assistant_message_service(), server
    )
