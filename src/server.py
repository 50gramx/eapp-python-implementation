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
import datetime
import logging
import multiprocessing
import os
import socket
import time
from concurrent import futures

import grpc
from ethos.elint.services.product.identity.account.access_account_pb2_grpc import \
    add_AccessAccountServiceServicer_to_server
from ethos.elint.services.product.identity.account.create_account_pb2_grpc import \
    add_CreateAccountServiceServicer_to_server

import db_session
from application_context import ApplicationContext
from loader import Loader

_LOGGER = logging.getLogger(__name__)

_ONE_DAY = datetime.timedelta(days=1)
_PROCESS_COUNT = multiprocessing.cpu_count()
_THREAD_CONCURRENCY = _PROCESS_COUNT
_MAX_WORKERS = int(os.environ['EA_SERVICE_IDENTITY_GRPC_MAX_WORKERS'])

PORT = os.environ.get('EAPP_SERVICE_IDENTITY_PORT', None)
if PORT is None:
    logging.error("PORT NOT FOUND!")

GRPC_MAX_CONNECTION_IDLE_MS = os.environ.get('EAPP_SERVICE_IDENTITY_GRPC_MAX_CONNECTION_IDLE_MS', None)
if GRPC_MAX_CONNECTION_IDLE_MS is None:
    GRPC_MAX_CONNECTION_IDLE_MS = 15000
else:
    GRPC_MAX_CONNECTION_IDLE_MS = int(GRPC_MAX_CONNECTION_IDLE_MS)

max_workers = _MAX_WORKERS


#
# _LOGGER = logging.getLogger(__name__)
# _LOGGER.setLevel(logging.INFO)


@contextlib.contextmanager
def run_server(port):
    # Initiate the DbSession
    db_session.DbSession.init_db_session()
    logging.info(f'DbSession started')

    # Load Context
    Loader.init_multiverse_identity_context()
    logging.info(f'Identity context loaded')

    options = (
        ('grpc.max_connection_idle_ms', GRPC_MAX_CONNECTION_IDLE_MS),
        # ('grpc.max_connection_age_ms', 5000),
        # ('grpc.max_connection_age_grace_ms', 10000),
        # ('grpc.client_idle_timeout_ms', 3000),
    )

    # Bind ThreadPoolExecutor and Services to server
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers),
        options=options
    )

    identity_layer = int(os.environ.get("EAPP_SERVICE_IDENTITY_LAYER", "0"))
    if identity_layer == 0:
        pass
    elif identity_layer == 1:
        pass
    elif identity_layer == 2:
        pass

    __add_account_servicer_to_server(server)
    __add_space_servicer_to_server(server)
    __add_account_assistant_servicer_to_server(server)
    __add_machine_servicer_to_server(server)

    # TODO: Pass down the credentials to secure port
    with open(os.environ['EAPP_SERVICE_IDENTITY_KEY'], 'rb') as f:
        private_key = f.read()

    with open(os.environ['EAPP_SERVICE_IDENTITY_COMMON_GRPC_EXTERNAL_CERTIFICATE_FILE'], 'rb') as f:
        certificate_chain = f.read()

    server_creds = grpc.ssl_server_credentials(
        ((private_key, certificate_chain,),))

    server_port = server.add_insecure_port(f"[::]:{PORT}")
    # server_port = server.add_secure_port(f"[::]:{PORT}", server_creds)

    server.start()
    try:
        yield server, server_port
    finally:
        server.stop()


def _wait_forever(server):
    try:
        while True:
            time.sleep(_ONE_DAY.total_seconds())
    except KeyboardInterrupt:
        server.stop(None)


def __add_account_servicer_to_server(server):
    add_CreateAccountServiceServicer_to_server(
        ApplicationContext.get_create_account_service(), server
    )
    add_AccessAccountServiceServicer_to_server(
        ApplicationContext.get_access_account_service(), server
    )
    # add_ConnectAccountServiceServicer_to_server(
    #     ApplicationContext.get_connect_account_service(), server
    # )
    # add_DiscoverAccountServiceServicer_to_server(
    #     ApplicationContext.get_discover_account_service(), server
    # )
    # add_PayInAccountServiceServicer_to_server(
    #     ApplicationContext.get_pay_in_account_service(), server
    # )
    # add_NotifyAccountServiceServicer_to_server(
    #     ApplicationContext.get_notify_account_service(), server
    # )
    return


def __add_space_servicer_to_server(server):
    # add_CreateSpaceServiceServicer_to_server(
    #     ApplicationContext.get_create_space_service(), server
    # )
    # add_AccessSpaceServiceServicer_to_server(
    #     ApplicationContext.get_access_space_service(), server
    # )
    return


def __add_machine_servicer_to_server(server):
    # add_DiscoverMachineServiceServicer_to_server(
    #     ApplicationContext.get_discover_machine_service(), server
    # )
    return


def __add_account_assistant_servicer_to_server(server):
    # add_CreateAccountAssistantServiceServicer_to_server(
    #     ApplicationContext.get_create_account_assistant_service(), server
    # )
    # add_AccessAccountAssistantServiceServicer_to_server(
    #     ApplicationContext.get_access_account_assistant_service(), server
    # )
    # add_ConnectAccountAssistantServiceServicer_to_server(
    #     ApplicationContext.get_connect_account_assistant_service(), server
    # )
    # add_DiscoverAccountAssistantServiceServicer_to_server(
    #     ApplicationContext.get_discover_account_assistant_service(), server
    # )
    # add_ActionAccountAssistantServiceServicer_to_server(
    #     ApplicationContext.get_action_account_assistant_service(), server
    # )
    return


def _run_server(bind_address):
    """Start a server in a subprocess."""
    logging.info(f'Starting new server at {bind_address}')
    options = (('grpc.so_reuseport', 1),)

    # Bind ThreadPoolExecutor and Services to server
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=_MAX_WORKERS, ),
        options=options)
    #
    # server = grpc.server(
    #     futures.ThreadPoolExecutor(max_workers=max_workers)
    # )
    logging.info(f'gRPC Server Created at {bind_address}')

    # Initiate the DbSession
    db_session.DbSession.init_db_session()
    logging.info(f'DbSession started at {bind_address}')

    # Load Context
    Loader.init_multiverse_identity_context()
    logging.info(f'Identity context loaded at {bind_address}')

    __add_account_servicer_to_server(server)
    __add_space_servicer_to_server(server)
    __add_account_assistant_servicer_to_server(server)
    __add_machine_servicer_to_server(server)

    with open(os.environ['EAPP_SERVICE_IDENTITY_KEY'], 'rb') as f:
        private_key = f.read()

    with open(os.environ['EAPP_SERVICE_IDENTITY_COMMON_GRPC_EXTERNAL_CERTIFICATE_FILE'], 'rb') as f:
        certificate_chain = f.read()

    server_creds = grpc.ssl_server_credentials(
        ((private_key, certificate_chain,),))

    # server_port = server.add_insecure_port(f"[::]:{PORT}")
    server_port = server.add_secure_port(bind_address, server_creds)

    server.start()
    logging.info(f"Started a new server at {bind_address}")
    _wait_forever(server)


@contextlib.contextmanager
def _reserve_port():
    """Find and reserve a port for all subprocesses to use."""
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    if sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) == 0:
        raise RuntimeError("Failed to set SO_REUSEPORT.")
    sock.bind(('', 50501))
    try:
        logging.info(f"----------------------- Yielding Socket {sock.getsockname()[1]} -----------------------")
        yield sock.getsockname()[1]
    finally:
        logging.info("----------------------- Closing Socket at finally -----------------------")
        sock.close()


def main():
    with run_server(PORT) as (server, port):
        logging.info(f'\tEthosApp Identity Server is listening at port {port}')
        server.wait_for_termination()
    #
    # with _reserve_port() as port:
    #     bind_address = f"[::]:{port}"
    #     logging.info("Binding to '%s'", bind_address)
    #     sys.stdout.flush()
    #     workers = []
    #     for _ in range(_PROCESS_COUNT):
    #         # NOTE: It is imperative that the worker subprocesses be forked before
    #         # any gRPC servers start up. See
    #         # https://github.com/grpc/grpc/issues/16001 for more details.
    #         worker = multiprocessing.Process(target=_run_server,
    #                                          args=(bind_address,))
    #         logging.info("Binding done, Starting worker...")
    #         worker.start()
    #         workers.append(worker)
    #     for worker in workers:
    #         worker.join()


if __name__ == '__main__':
    # handler = logging.StreamHandler(sys.stdout)
    # formatter = logging.Formatter('[PID %(process)d] %(message)s')
    # handler.setFormatter(formatter)
    # _LOGGER.addHandler(handler)
    # _LOGGER.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO)  # warn: testing this
    main()
    # main()
