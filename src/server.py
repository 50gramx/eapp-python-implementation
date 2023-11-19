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

import contextlib
import logging
import os
from concurrent import futures

import grpc

import db_session
from community.gramx.fifty.zero.ethos.conversations.handler import handle_conversations_services
from community.gramx.fifty.zero.ethos.identity.handler import handle_identity_services
from loader import Loader

_LOGGER = logging.getLogger(__name__)

max_workers = int(os.environ['EAPP_SERVICE_IDENTITY_GRPC_MAX_WORKERS'])

PORT = os.environ.get('EAPP_SERVICE_IDENTITY_PORT', None)
if PORT is None:
    logging.error("PORT NOT FOUND!")

GRPC_MAX_CONNECTION_IDLE_MS = os.environ.get('EAPP_SERVICE_IDENTITY_GRPC_MAX_CONNECTION_IDLE_MS', None)
if GRPC_MAX_CONNECTION_IDLE_MS is None:
    GRPC_MAX_CONNECTION_IDLE_MS = 15000
else:
    GRPC_MAX_CONNECTION_IDLE_MS = int(GRPC_MAX_CONNECTION_IDLE_MS)


@contextlib.contextmanager
def run_server(port):
    # Initiate the DbSession
    db_session.DbSession.init_db_session()
    logging.info(f'DbSession started')

    # Load Context
    Loader.init_multiverse_identity_context()
    logging.info(f'Identity context loaded')
    Loader.init_multiverse_conversations_context()
    logging.info(f'Conversations context loaded')

    # Bind ThreadPoolExecutor and Services to server
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers)
    )

    # handle Identity Services
    handle_identity_services(server)
    logging.info(f'Identity services added')

    # handle conversations services
    handle_conversations_services(server)
    logging.info(f'Conversations services added')

    server_port = server.add_insecure_port(f"[::]:{port}")
    server.start()
    try:
        yield server, server_port
    finally:
        server.stop()


def main():
    with run_server(PORT) as (server, port):
        logging.info(f'\tEthosApp Identity Server is listening at port {port}')
        server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # warn: testing this
    main()
