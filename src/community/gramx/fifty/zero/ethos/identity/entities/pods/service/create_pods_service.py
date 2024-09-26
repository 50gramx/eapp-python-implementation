from ethos.elint.services.product.identity.pods.create_pods_pb2_grpc import CreatePodsServiceServicer
from community.gramx.fifty.zero.ethos.identity.entities.pods.capabilities.implementation.create_pods_impl import CreatePodsImpl

from support.application.tracing import trace_rpc, PYTHON_IMPLEMENTATION_TRACER


class CreatePodsService(CreatePodsServiceServicer):
    def __init__(self):
        super(CreatePodsService, self).__init__()
        self.session_scope = self.__class__.__name__
        self.tracer = PYTHON_IMPLEMENTATION_TRACER

    def __del__(self):
        self.tracer.close()

    @trace_rpc()
    def CreateUniverse(self, request, context):
        return CreatePodsImpl(request=request)



