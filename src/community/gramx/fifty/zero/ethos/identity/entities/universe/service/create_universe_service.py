from ethos.elint.services.product.identity.universe.create_universe_pb2_grpc import CreateUniverseServiceServicer

from community.gramx.fifty.zero.ethos.identity.entities.universe.implementation.create_universe_impl import \
    create_universe_impl
from support.application.tracing import trace_rpc, PYTHON_IMPLEMENTATION_TRACER


class CreateUniverseService(CreateUniverseServiceServicer):
    def __init__(self):
        super(CreateUniverseService, self).__init__()
        self.session_scope = self.__class__.__name__
        self.tracer = PYTHON_IMPLEMENTATION_TRACER

    def __del__(self):
        self.tracer.close()

    @trace_rpc()
    def CreateUniverse(self, request, context):
        return create_universe_impl(request=request)
