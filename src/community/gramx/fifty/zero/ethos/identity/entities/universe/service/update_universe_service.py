from ethos.elint.services.product.identity.universe.update_universe_pb2_grpc import UpdateUniverseServiceServicer

from community.gramx.fifty.zero.ethos.identity.entities.universe.implementation.update_universe_impl import \
    update_universe_impl
from support.application.tracing import trace_rpc, PYTHON_IMPLEMENTATION_TRACER


class UpdateUniverseService(UpdateUniverseServiceServicer):
    def __init__(self):
        super(UpdateUniverseService, self).__init__()
        self.session_scope = self.__class__.__name__
        self.tracer = PYTHON_IMPLEMENTATION_TRACER

    def __del__(self):
        self.tracer.close()

    @trace_rpc()
    def UpdateUniverse(self, request, context):
        return update_universe_impl(request=request)
