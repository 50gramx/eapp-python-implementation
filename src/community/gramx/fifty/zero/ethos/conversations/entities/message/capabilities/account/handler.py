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

from ethos.elint.services.product.conversation.message.account.receive_account_message_pb2_grpc import \
    add_ReceiveAccountMessageServiceServicer_to_server
from ethos.elint.services.product.conversation.message.account.send_account_message_pb2_grpc import \
    add_SendAccountMessageServiceServicer_to_server

from application_context import ApplicationContext


def handle_message_account_services(server, aio: bool):
    if aio:
        pass
    else:
        add_SendAccountMessageServiceServicer_to_server(
            ApplicationContext.get_send_account_message_service(), server
        )
        logging.info(f'\t\t [x] send')
        add_ReceiveAccountMessageServiceServicer_to_server(
            ApplicationContext.get_receive_account_message_service(), server
        )
        logging.info(f'\t\t [x] receive')
