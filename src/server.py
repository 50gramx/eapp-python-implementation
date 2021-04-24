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

import argparse
import contextlib
import logging
import os
from concurrent import futures

import grpc

import db_session
from application_context import ApplicationContext
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
from ethos.elint.services.product.identity.space.access_space_pb2_grpc import add_AccessSpaceServiceServicer_to_server
from ethos.elint.services.product.identity.space.create_space_pb2_grpc import add_CreateSpaceServiceServicer_to_server
from loader import Loader

PORT = os.environ.get('EAPP_SERVICE_IDENTITY_PORT', None)
if PORT is None:
    logging.error("PORT NOT FOUND!")

max_workers = int(os.environ['EA_SERVICE_IDENTITY_GRPC_MAX_WORKERS'])

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


@contextlib.contextmanager
def run_server(port):
    # Initiate the DbSession
    db_session.DbSession.init_db_session()
    # Bind ThreadPoolExecutor and Services to server
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers)
    )

    add_CreateAccountServiceServicer_to_server(
        ApplicationContext.get_create_account_service(), server
    )
    add_AccessAccountServiceServicer_to_server(
        ApplicationContext.get_access_account_service(), server
    )
    add_ConnectAccountServiceServicer_to_server(
        ApplicationContext.get_connect_account_service(), server
    )
    add_DiscoverAccountServiceServicer_to_server(
        ApplicationContext.get_discover_account_service(), server
    )
    add_PayInAccountServiceServicer_to_server(
        ApplicationContext.get_pay_in_account_service(), server
    )

    add_CreateSpaceServiceServicer_to_server(
        ApplicationContext.get_create_space_service(), server
    )
    add_AccessSpaceServiceServicer_to_server(
        ApplicationContext.get_access_space_service(), server
    )

    add_CreateAccountAssistantServiceServicer_to_server(
        ApplicationContext.get_create_account_assistant_service(), server
    )
    add_AccessAccountAssistantServiceServicer_to_server(
        ApplicationContext.get_access_account_assistant_service(), server
    )
    add_ConnectAccountAssistantServiceServicer_to_server(
        ApplicationContext.get_connect_account_assistant_service(), server
    )
    add_DiscoverAccountAssistantServiceServicer_to_server(
        ApplicationContext.get_discover_account_assistant_service(), server
    )
    add_ActionAccountAssistantServiceServicer_to_server(
        ApplicationContext.get_action_account_assistant_service(), server
    )

    add_NotifyAccountServiceServicer_to_server(
        ApplicationContext.get_notify_account_service(), server
    )

    # TODO: Pass down the credentials to secure port
    server_port = server.add_insecure_port(f"[::]:{PORT}")

    server.start()
    try:
        yield server, server_port
    finally:
        server.stop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',
                        nargs='?',
                        type=int,
                        default=50502,
                        help='the listening port')
    args = parser.parse_args()

    with run_server(args.port) as (server, port):
        logging.info(f'\tEthosApp Identity Server is listening at port {port}')
        server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    Loader.init_identity_context('')
    main()
