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
import asyncio
import contextlib
import logging
import os
import threading
from concurrent import futures
from time import sleep

import grpc
from grpc_health.v1 import health, health_pb2_grpc, health_pb2
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.grpc import aio_server_interceptor
from opentelemetry.instrumentation.grpc._server import OpenTelemetryServerInterceptor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

import db_session
from community.gramx.fifty.zero.ethos.conversations.handler import handle_conversations_services
from community.gramx.fifty.zero.ethos.identity.handler import handle_identity_services
from community.gramx.fifty.zero.ethos.knowledge_spaces.handler import handle_knowledge_spaces_services
from loader import Loader

trace.set_tracer_provider(TracerProvider())

# create a JaegerExporter
jaeger_exporter = OTLPSpanExporter(
    'jaeger:4317', insecure=True
)

# Create a BatchSpanProcessor and add the exporter to it
span_processor = BatchSpanProcessor(jaeger_exporter)

trace.get_tracer_provider().add_span_processor(
    span_processor
)

tracer = trace.get_tracer(__name__)


# grpc_server_instrumentor = GrpcInstrumentorServer()
# grpc_server_instrumentor.instrument()


def _toggle_health(health_servicer: health.HealthServicer, service: str):
    next_status = health_pb2.HealthCheckResponse.SERVING
    while True:
        if next_status == health_pb2.HealthCheckResponse.SERVING:
            next_status = health_pb2.HealthCheckResponse.NOT_SERVING
        else:
            next_status = health_pb2.HealthCheckResponse.SERVING

        health_servicer.set(service, next_status)
        sleep(5)


def _configure_health_server(server: grpc.Server):
    health_servicer = health.HealthServicer(
        experimental_non_blocking=True,
        experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=10),
    )
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

    # Use a daemon thread to toggle health status
    toggle_health_status_thread = threading.Thread(
        target=_toggle_health,
        args=(health_servicer, "helloworld.Greeter"),
        daemon=True,
    )
    toggle_health_status_thread.start()


def _init_db():
    # Initiate the DbSession
    db_session.DbSession.init_db_session()
    logging.info(f'DbSession started')


def _init_context(aio: bool = False):
    # Load Context
    Loader.init_multiverse_context()
    Loader.init_multiverse_identity_context(aio=aio)
    Loader.init_multiverse_conversations_context(aio=aio)
    Loader.init_multiverse_knowledge_spaces_context(aio=aio)


def _init_services(server, aio: bool = False):
    handle_identity_services(server=server, aio=aio)
    handle_conversations_services(server=server, aio=aio)
    handle_knowledge_spaces_services(server=server, aio=aio)


async def run_aio_server(port):
    _init_db()
    _init_context(aio=True)

    migration_thread_pool = futures.ThreadPoolExecutor(
        max_workers=int(os.environ['ERPC_MAX_WORKERS'])
    )

    options = [
        ("grpc.enable_keepalive", 0),
    ]

    interceptors = [
        aio_server_interceptor()
    ]

    server = grpc.aio.server(
        migration_thread_pool=migration_thread_pool,
        options=options,
        interceptors=interceptors,
    )

    _init_services(server=server, aio=True)

    server_port = server.add_insecure_port(f"[::]:{port}")
    _configure_health_server(server)
    await server.start()
    try:
        logging.info(f'\tEthosApps Python Asynchronous Capabilities are listening at port {server_port}')
        await server.wait_for_termination()
    finally:
        await server.stop()


@contextlib.contextmanager
def run_server(port):
    _init_db()
    _init_context()

    interceptors = [
        OpenTelemetryServerInterceptor(tracer),
    ]

    # Bind ThreadPoolExecutor and Services to server
    server = grpc.server(
        thread_pool=futures.ThreadPoolExecutor(
            max_workers=int(os.environ['ERPC_MAX_WORKERS'])
        ),
        options=[
            ("grpc.enable_keepalive", 0),
        ],
        interceptors=interceptors
    )

    _init_services(server=server)

    server_port = server.add_insecure_port(f"[::]:{port}")
    _configure_health_server(server)
    server.start()
    try:
        logging.info(f'\tEthosApps Python Synchronous Capabilities are listening at port {server_port}')
        server.wait_for_termination()
    finally:
        server.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start Hosting EthosApps Python Implementations')
    parser.add_argument('--aio', action='store_true')
    parser.add_argument('--debug', action='store_true')
    parser.set_defaults(feature=True)
    args = parser.parse_args()
    logging.basicConfig(level=(logging.DEBUG if args.debug else logging.INFO))
    if args.aio:
        logging.info("Starting Asynchronous Server")
        asyncio.run(run_aio_server(os.environ.get('ERPC_PORT', 80)))
    else:
        logging.info("Starting Synchronous Server")
        run_server(os.environ.get('ERPC_PORT', 80))
