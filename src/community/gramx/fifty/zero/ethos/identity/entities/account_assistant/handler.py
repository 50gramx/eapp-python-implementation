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

from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2_grpc import \
    add_AccessAccountAssistantServiceServicer_to_server
from ethos.elint.services.product.identity.account_assistant.action_account_assistant_pb2_grpc import \
    add_ActionAccountAssistantServiceServicer_to_server
from ethos.elint.services.product.identity.account_assistant.connect_account_assistant_pb2_grpc import \
    add_ConnectAccountAssistantServiceServicer_to_server
from ethos.elint.services.product.identity.account_assistant.create_account_assistant_pb2_grpc import \
    add_CreateAccountAssistantServiceServicer_to_server
from ethos.elint.services.product.identity.account_assistant.discover_account_assistant_pb2_grpc import \
    add_DiscoverAccountAssistantServiceServicer_to_server

from application_context import ApplicationContext


def handle_account_assistant_services(server, aio: bool):
    if aio:
        add_ActionAccountAssistantServiceServicer_to_server(
            ApplicationContext.get_action_account_assistant_service(), server
        )
        logging.info(f'\t\t [x] action')
    else:
        add_CreateAccountAssistantServiceServicer_to_server(
            ApplicationContext.get_create_account_assistant_service(), server
        )
        logging.info(f'\t\t [x] create')
        add_AccessAccountAssistantServiceServicer_to_server(
            ApplicationContext.get_access_account_assistant_service(), server
        )
        logging.info(f'\t\t [x] access')
        add_ConnectAccountAssistantServiceServicer_to_server(
            ApplicationContext.get_connect_account_assistant_service(), server
        )
        logging.info(f'\t\t [x] connect')
        add_DiscoverAccountAssistantServiceServicer_to_server(
            ApplicationContext.get_discover_account_assistant_service(), server
        )
        logging.info(f'\t\t [x] discover')
    return
