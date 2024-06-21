from ethos.elint.services.product.identity.galaxy.read_galaxy_pb2_grpc import ReadGalaxyServiceServicer
from implementation.read_galaxy_impl import read_galaxy_impl
from support.application.tracing import trace_rpc, PYTHON_IMPLEMENTATION_TRACER

class ReadGalaxyService(ReadGalaxyServiceServicer):
    def __init__(self):
        super(ReadGalaxyService, self).__init__()
        self.session_scope = self.__class__.__name__
        self.tracer = PYTHON_IMPLEMENTATION_TRACER
    
    def __del__(self):
        self.tracer.close()
    
    @trace_rpc()
    def ReadGalaxy(self, request, context):
        return read_galaxy_impl(request=request, context=context)