#   /*************************************************************************
#   *
#   * AMIT KUMAR KHETAN CONFIDENTIAL
#   * __________________
#   *
#   *  [2017] - [2024] Amit Kumar Khetan
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

from ethos.elint.services.product.identity.universe.discover_universe_pb2_grpc import DiscoverUniverseServiceServicer

from community.gramx.fifty.zero.ethos.identity.entities.universe.discover.capabilities.implementations.by_id_impl import \
    by_id_impl
from support.application.tracing import trace_rpc, PYTHON_IMPLEMENTATION_TRACER


class DiscoverUniverseService(DiscoverUniverseServiceServicer):
    def __init__(self):
        super(DiscoverUniverseService, self).__init__()
        self.session_scope = self.__class__.__name__
        self.tracer = PYTHON_IMPLEMENTATION_TRACER

    def __del__(self):
        self.tracer.close()

    @trace_rpc()
    def ByID(self, request, context):
        return by_id_impl(request=request, context=context)
