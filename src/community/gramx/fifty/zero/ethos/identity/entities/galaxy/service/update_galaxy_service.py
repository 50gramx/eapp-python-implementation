from ethos.elint.services.product.identity.galaxy.update_galaxy_pb2_grpc import UpdateGalaxyServiceServicer
from implementation.update_galaxy_impl import update_galaxy_impl
from support.application.tracing import trace_rpc, PYTHON_IMPLEMENTATION_TRACER

class UpdateGalaxyService(UpdateGalaxyServiceServicer):
    def __init__(self):
        super(UpdateGalaxyService, self).__init__()
        self.session_scope = self.__class__.__name__
        self.tracer = PYTHON_IMPLEMENTATION_TRACER
    
    def __del__(self):
        self.tracer.close()
    
    @trace_rpc()
    def UpdateGalaxy(self, request, context):
        return update_galaxy_impl(request=request, context=context)