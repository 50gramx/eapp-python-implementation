from ethos.elint.services.product.identity.universe.read_universe_pb2_grpc import ReadUniverseServiceServicer
from implementation.read_universe_impl import read_universe_impl
from support.application.tracing import trace_rpc, PYTHON_IMPLEMENTATION_TRACER

class ReadUniverseService(ReadUniverseServiceServicer):
    def __init__(self):
        super(ReadUniverseService, self).__init__()
        self.session_scope = self.__class__.__name__
        self.tracer = PYTHON_IMPLEMENTATION_TRACER
    
    def __del__(self):
        self.tracer.close()
    
    @trace_rpc()
    def ReadUniverse(self, request, context):
        return read_universe_impl(request=request)