from ethos.elint.services.product.identity.galaxy.create_galaxy_pb2_grpc import CreateGalaxyServiceServicer
from implementation.create_galaxy_impl import create_galaxy_impl
from support.application.tracing import trace_rpc, PYTHON_IMPLEMENTATION_TRACER

class CreateGalaxyService(CreateGalaxyServiceServicer):
    def __init__(self):
        super(CreateGalaxyService, self).__init__()
        self.session_scope = self.__class__.__name__
        self.tracer = PYTHON_IMPLEMENTATION_TRACER
    
    def __del__(self):
        self.tracer.close()
    
    @trace_rpc()
    def CreateGalaxy(self, request, context):
        return create_galaxy_impl(request=request, context=context)