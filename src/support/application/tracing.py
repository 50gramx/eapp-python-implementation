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
import os
from functools import wraps

from grpc import StatusCode
from jaeger_client import Config
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentracing import tags
from opentracing.propagation import Format

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class AtlasTracer:
    def __init__(self):
        self.tracer = None

    # 1. We register the tracer from the provider
    @staticmethod
    def _register_tracer_provider(aio: bool):
        host_key = "ERPC_AIO_HOST" if aio else "ERPC_HOST"
        tracer_svc_name = os.environ.get(host_key, "ERPC_OPEN")
        tracer_res_svc = {SERVICE_NAME: tracer_svc_name}
        tracer_pvd_res = Resource.create(tracer_res_svc)
        tracer_pvd = TracerProvider(resource=tracer_pvd_res)
        trace.set_tracer_provider(tracer_pvd)  # set it here

    @staticmethod
    def _register_span_processor():
        # create a JaegerExporter
        jaeger_exporter = OTLPSpanExporter(
            'jaeger:4317', insecure=True
        )

        # Create a BatchSpanProcessor and add the exporter to it
        return BatchSpanProcessor(jaeger_exporter)

    @staticmethod
    def _register_tracer(aio: bool):
        AtlasTracer._register_tracer_provider(aio=aio)
        # 2. We get the tracer
        tracer = trace.get_tracer(__name__)

        # 3. We set the tracer provider with span exporter
        trace.get_tracer_provider().add_span_processor(
            AtlasTracer._register_span_processor()
        )
        return tracer

    @staticmethod
    def get(aio: bool = False):
        return AtlasTracer._register_tracer(aio=aio)

    @staticmethod
    def set_span_attr(key, value):
        current_span = trace.get_current_span()
        current_span.set_attribute(key, value)


def init_jaeger_tracer(service_name):
    logging.debug("init_tracer")
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'local_agent': {'reporting_host': 'jaeger', 'reporting_port': '6831'},
            'logging': True,
        },
        service_name=service_name,
    )
    return config.initialize_tracer()


PYTHON_IMPLEMENTATION_TRACER = init_jaeger_tracer('eapp-python-implementation')
logging.info("PYTHON_IMPLEMENTATION_TRACER")
ATLAS_TRACER = AtlasTracer.get()


def trace_rpc(tracer=PYTHON_IMPLEMENTATION_TRACER):
    def decorator(func):

        @wraps(func)
        def wrapper(self, request, context):
            span_name = func.__name__

            # Extract trace context from incoming request metadata
            metadata_dict = dict(context.invocation_metadata())
            logging.debug(f"metadata_dict: {metadata_dict}")
            span_ctx = tracer.extract(Format.TEXT_MAP, metadata_dict)

            # Start a new span for the incoming request
            with tracer.start_span(span_name, child_of=span_ctx) as span:
                # Inject trace context into outgoing request metadata
                tracer.inject(span.context, Format.TEXT_MAP, metadata_dict)
                metadata = [(key, value) for key, value in metadata_dict.items()]

                # Set custom tags
                span.set_tag("session_scope", self.session_scope)
                # Set gRPC tags
                span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
                span.set_tag(tags.PEER_SERVICE, 'unknown-service')

                try:
                    logging.info(f"{self.session_scope}:{span_name}")
                    logging.info(f"context: {context}")
                    return func(self, request, context)
                except Exception as e:
                    logging.error(f"An error occurred during {span_name} RPC: {e}")
                    # You might also want to modify the response or set gRPC status to signal the error.
                    context.set_code(StatusCode.INTERNAL)
                    context.set_details(f"Internal Server Error: {str(e)}")
                    raise  # Re-raise the exception after logging it

        return wrapper

    return decorator
