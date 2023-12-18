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

from ethos.elint.services.product.identity.account.access_account_pb2_grpc import \
    add_AccessAccountServiceServicer_to_server
from ethos.elint.services.product.identity.account.connect_account_pb2_grpc import \
    add_ConnectAccountServiceServicer_to_server
from ethos.elint.services.product.identity.account.create_account_pb2_grpc import \
    add_CreateAccountServiceServicer_to_server
from ethos.elint.services.product.identity.account.discover_account_pb2_grpc import \
    add_DiscoverAccountServiceServicer_to_server
from ethos.elint.services.product.identity.account.notify_account_pb2_grpc import \
    add_NotifyAccountServiceServicer_to_server
from ethos.elint.services.product.identity.account.pay_in_account_pb2_grpc import \
    add_PayInAccountServiceServicer_to_server

from application_context import ApplicationContext


def handle_account_services(server, aio: bool):
    if aio:
        pass
    else:
        add_CreateAccountServiceServicer_to_server(
            ApplicationContext.get_create_account_service(), server
        )
        logging.info(f'\t\t [x] create')
        add_AccessAccountServiceServicer_to_server(
            ApplicationContext.get_access_account_service(), server
        )
        logging.info(f'\t\t [x] access')
        add_ConnectAccountServiceServicer_to_server(
            ApplicationContext.get_connect_account_service(), server
        )
        logging.info(f'\t\t [x] connect')
        add_DiscoverAccountServiceServicer_to_server(
            ApplicationContext.get_discover_account_service(), server
        )
        logging.info(f'\t\t [x] discover')
        add_PayInAccountServiceServicer_to_server(
            ApplicationContext.get_pay_in_account_service(), server
        )
        logging.info(f'\t\t [x] pay in')
        add_NotifyAccountServiceServicer_to_server(
            ApplicationContext.get_notify_account_service(), server
        )
        logging.info(f'\t\t [x] notify')
    return server
