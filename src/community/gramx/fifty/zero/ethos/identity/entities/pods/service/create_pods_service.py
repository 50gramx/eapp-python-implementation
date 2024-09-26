from ethos.elint.collars import Service50DC499999999_pb2
from ethos.elint.services.product.identity.pods import create_pods_pb2
from ethos.elint.services.product.identity.pods.create_pods_pb2_grpc import \
    CreatePodsServiceServicer
from support.application.tracing import PYTHON_IMPLEMENTATION_TRACER, trace_rpc


class CreatePodsService(CreatePodsServiceServicer):
    def __init__(self):
        print("init CreatePodsService")
        super(CreatePodsService, self).__init__()
        self.session_scope = self.__class__.__name__
        self.tracer = PYTHON_IMPLEMENTATION_TRACER

    def __del__(self):
        self.tracer.close()

    @trace_rpc()
    def CreatePod(self, request, context):
        print("CreatePod invoked")  # Simulating pod creation with dummy data
        pod = request.pod
        print(f"Creating pod: {pod.name}")

        # Create a new Pod object to simulate saving it (if applicable)
        new_pod = Service50DC499999999_pb2.Pod(
            name=pod.name,
            image=pod.image,
            container_ports=pod.container_ports,
            env_vars=pod.env_vars,
            expiration_time=pod.expiration_time,  # Can be set from request or modified here
        )

        # You could add logic here to save the pod to a database or in-memory store

        # Simulating a response
        response = create_pods_pb2.CreatePodResponse()
        response.message = f"Pod '{new_pod.name}' created successfully!"
        return response
