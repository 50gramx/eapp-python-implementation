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
from functools import wraps

from grpc import StatusCode
from jaeger_client import Config
from opentracing import tags
from opentracing.propagation import Format

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def init_tracer(service_name):
    logging.info("init_tracer")
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'local_agent': {'reporting_host': 'jaeger', 'reporting_port': '6831'},
            'logging': True,
        },
        service_name=service_name,
    )
    return config.initialize_tracer()


PYTHON_IMPLEMENTATION_TRACER = init_tracer('eapp-python-implementation')
logging.info("PYTHON_IMPLEMENTATION_TRACER")


def trace_rpc(tracer=PYTHON_IMPLEMENTATION_TRACER):
    logging.info("...into trace_rpc...")

    def decorator(func):
        logging.info("...into decorator...")

        @wraps(func)
        def wrapper(self, request, context):
            logging.info("...into wrapper...")
            span_name = func.__name__

            # Extract trace context from incoming request metadata
            metadata_dict = dict(context.invocation_metadata())
            span_ctx = tracer.extract(Format.TEXT_MAP, metadata_dict)

            # Start a new span for the incoming request
            with tracer.start_span(span_name, child_of=span_ctx) as span:
                # Inject trace context into outgoing request metadata
                tracer.inject(span.context, Format.TEXT_MAP, metadata_dict)
                metadata = [(key, value) for key, value in metadata_dict.items()]

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
