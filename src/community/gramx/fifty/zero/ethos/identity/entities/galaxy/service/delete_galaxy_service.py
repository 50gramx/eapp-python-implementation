from ethos.elint.services.product.identity.galaxy.delete_galaxy_pb2_grpc import DeleteGalaxyServiceServicer
from implementation.delete_galaxy_impl import delete_galaxy_impl
from support.application.tracing import trace_rpc, PYTHON_IMPLEMENTATION_TRACER

class DeletGalaxyService(DeleteGalaxyServiceServicer):
    def __init__(self):
        super(DeletGalaxyService, self).__init__()
        self.session_scope = self.__class__.__name__
        self.tracer = PYTHON_IMPLEMENTATION_TRACER
    
    def __del__(self):
        self.tracer.close()
    
    @trace_rpc()
    def DeleteGalaxy(self, request, context):
        return delete_galaxy_impl(request=request, context=context)