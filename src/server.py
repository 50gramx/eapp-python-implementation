import argparse
import contextlib
import logging
import os
from concurrent import futures

import grpc

import db_session
from application_context import ApplicationContext
from ethos.elint.services.product.identity.account.onboard_account_pb2_grpc import \
    add_OnboardAccountServiceServicer_to_server
from ethos.elint.services.product.identity.organisation.onboard_organization_space_pb2_grpc import \
    add_OnboardOrganizationSpaceServiceServicer_to_server
from loader import Loader

PORT = os.environ.get('PORT', None)
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
    add_OnboardOrganizationSpaceServiceServicer_to_server(
        ApplicationContext.get_onboard_organization_space_service(), server
    )
    add_OnboardAccountServiceServicer_to_server(
        ApplicationContext.get_onboard_account_service(), server
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
        logging.info('Server is listening at port :%d', port)
        server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    Loader.init_identity_context('')
    main()
