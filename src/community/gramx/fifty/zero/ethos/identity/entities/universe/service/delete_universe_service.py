from ethos.elint.services.product.identity.universe.delete_universe_pb2_grpc import DeleteUniverseServiceServicer
from implementation.delete_universe_impl import delete_universe_impl
from support.application.tracing import trace_rpc, PYTHON_IMPLEMENTATION_TRACER

class DeleteUniverseService(DeleteUniverseServiceServicer):
    def __init__(self):
        super(DeleteUniverseService, self).__init__()
        self.session_scope = self.__class__.__name__
        self.tracer = PYTHON_IMPLEMENTATION_TRACER
    
    def __del__(self):
        self.tracer.close()
    
    @trace_rpc()
    def DeleteUniverse(self, request, context):
        return delete_universe_impl(request=request)