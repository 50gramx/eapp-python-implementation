import grpc
from concurrent import futures
import time
from datetime import datetime, timedelta

from ethos.elint.collars import Service50DC499999999_pb2
from ethos.elint.services.product.identity.pods import create_pods_pb2, create_pods_pb2_grpc


class CreatePodsImpl(create_pods_pb2_grpc.CreatePodsServiceServicer):
    def CreatePod(self, request, context):
        # Simulating pod creation with dummy data
        pod = request.pod
        print(f"Creating pod: {pod.name}")

        # Create a new Pod object to simulate saving it (if applicable)
        new_pod = Service50DC499999999_pb2.Pod(
            name=pod.name,
            image=pod.image,
            container_ports=pod.container_ports,
            env_vars=pod.env_vars,
            expiration_time=pod.expiration_time  # Can be set from request or modified here
        )
        
        # You could add logic here to save the pod to a database or in-memory store

        # Simulating a response
        response = create_pods_pb2.CreatePodResponse()
        response.message = f"Pod '{new_pod.name}' created successfully!"
        return response

    def GetPods(self, request, context):
        # Simulating fetching a list of pods
        dummy_pods = []
        for i in range(3):  # Dummy data for 3 pods
            pod = Service50DC499999999_pb2.Pod(
                name=f"dummy-pod-{i}",
                image="dummy/image:latest",
                container_ports=[80, 443],
                env_vars=[
                    Service50DC499999999_pb2.EnvVar(name="ENV_VAR", value="value")
                ],
                expiration_time=self._get_future_timestamp()
            )
            dummy_pods.append(pod)

        response = create_pods_pb2.GetPodsResponse()
        response.pods.extend(dummy_pods)
        return response

    def GetSSHPodCredentials(self, request, context):
        # Simulating SSH credentials response
        credentials = Service50DC499999999_pb2.SSHPodCredentials(
            user_name="dummy_user",
            node_ip="192.168.1.1",
            ssh_command="ssh dummy_user@192.168.1.1",
            last_login=self._get_current_timestamp()
        )
        response = create_pods_pb2.GetSSHPodCredentialsResponse(credentials=credentials)
        return response

    def GetNodes(self, request, context):
        # Simulating fetching node information
        dummy_nodes = []
        for i in range(2):  # Dummy data for 2 nodes
            node = Service50DC499999999_pb2.NodeInfo(
                name=f"node-{i}",
                addresses={"internal": "192.168.1.10", "external": "10.0.0.10"},
                labels={"env": "test"},
                annotations={"description": "This is a test node"},
                status="Ready"
            )
            dummy_nodes.append(node)

        response = create_pods_pb2.GetNodesResponse()
        response.nodes.extend(dummy_nodes)
        return response

    @staticmethod
    def _get_current_timestamp():
        return create_pods_pb2.Timestamp(seconds=int(time.time()), nanos=0)

    @staticmethod
    def _get_future_timestamp():
        future_time = datetime.now() + timedelta(days=1)
        return create_pods_pb2.Timestamp(seconds=int(future_time.timestamp()), nanos=0)
