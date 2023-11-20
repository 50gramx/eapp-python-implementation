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

from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account.access_account_pb2 import ReAccountAccessTokenResponse
from ethos.elint.services.product.identity.account.access_account_pb2_grpc import AccessAccountServiceServicer
from opentracing import tags
from opentracing.propagation import Format

from access.account.services_authentication import AccessAccountServicesAuthentication
from community.gramx.fifty.zero.ethos.identity.entities.account.access.capabilities.implementations.validate_account_impl import \
    validate_account_impl
from community.gramx.fifty.zero.ethos.identity.entities.account.access.capabilities.implementations.validate_account_services_impl import \
    validate_account_services_impl
from community.gramx.fifty.zero.ethos.identity.entities.account.access.capabilities.implementations.verify_account_impl import \
    verify_account_impl
from community.gramx.fifty.zero.ethos.identity.services_caller.account_service_caller import \
    validate_account_services_caller
from support.application.tracing import init_tracer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def trace_rpc(tracer, span_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, context):
            metadata_dict = dict(context.invocation_metadata())
            span_ctx = tracer.extract(Format.TEXT_MAP, metadata_dict)
            with tracer.start_active_span(span_name, child_of=span_ctx) as scope:
                scope.span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
                scope.span.set_tag(tags.PEER_SERVICE, 'unknown-service')
                try:
                    return func(self, request, context)
                except Exception as e:
                    logging.error(f"An error occurred during {span_name} RPC: {e}")
                    # You might also want to modify the response or set gRPC status to signal the error.
                    raise  # Re-raise the exception after logging it

        return wrapper

    return decorator


tracer = init_tracer('access-account-service')


class AccessAccountService(AccessAccountServiceServicer):
    def __init__(self):
        super(AccessAccountService, self).__init__()
        self.session_scope = self.__class__.__name__
        self.tracer = tracer

    def __del__(self):
        self.tracer.close()

    @trace_rpc(tracer, 'ValidateAccount')
    def ValidateAccount(self, request, context):
        return validate_account_impl(request=request, session_scope=self.session_scope)

    def VerifyAccount(self, request, context):
        # Convert the metadata to a dictionary for opentracing.
        metadata_dict = dict(context.invocation_metadata())

        # Extract span context using the TEXT_MAP format.
        span_ctx = self.tracer.extract(Format.TEXT_MAP, metadata_dict)
        with self.tracer.start_active_span('VerifyAccount', child_of=span_ctx) as scope:
            # Add some tags
            scope.span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
            scope.span.set_tag(tags.PEER_SERVICE, 'unknown-service')  # or wherever the request is coming from
            logging.info("AccessAccountService:VerifyAccount")
            try:
                return verify_account_impl(request=request, session_scope=self.session_scope)
            except Exception as e:
                logging.error(f"An error occurred during VerifyAccount RPC: {e}")
                # You might also want to modify the response or set gRPC status to signal the error.

    def ValidateAccountServices(self, request, context):
        # Convert the metadata to a dictionary for opentracing.
        metadata_dict = dict(context.invocation_metadata())

        # Extract span context using the TEXT_MAP format.
        span_ctx = self.tracer.extract(Format.TEXT_MAP, metadata_dict)
        with self.tracer.start_active_span('ValidateAccountServices', child_of=span_ctx) as scope:
            # Add some tags
            scope.span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
            scope.span.set_tag(tags.PEER_SERVICE, 'unknown-service')  # or wherever the request is coming from
            logging.info(f"{self.session_scope}:ValidateAccountServices")
            try:
                return validate_account_services_impl(request=request, session_scope=self.session_scope)
            except Exception as e:
                logging.error(f"An error occurred during ValidateAccountServices RPC: {e}")
                # You might also want to modify the response or set gRPC status to signal the error.

    def ReAccountAccessToken(self, request, context):
        logging.info("AccessAccountService:ReAccountAccessToken")
        validation_done, validation_message = validate_account_services_caller(
            request.account_service_access_auth_details)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            if validation_message == "Session has expired. Retrieve a new session.":
                return ReAccountAccessTokenResponse(
                    account_service_access_auth_details=AccessAccountServicesAuthentication(
                        session_scope=self.session_scope,
                        account_id=request.account_service_access_auth_details.account.account_id
                    ).create_authentication_details(),
                    response_meta=ResponseMeta(meta_done=True, meta_message="New Session retrieved."))
            else:
                # Not authorised access, do not create one
                return ReAccountAccessTokenResponse(
                    account_service_access_auth_details=request.account_service_access_auth_details,
                    response_meta=meta)
        else:
            # Session is valid, no need to create one
            return ReAccountAccessTokenResponse(
                account_service_access_auth_details=request.account_service_access_auth_details,
                response_meta=ResponseMeta(meta_done=True, meta_message="Session is already valid."))
