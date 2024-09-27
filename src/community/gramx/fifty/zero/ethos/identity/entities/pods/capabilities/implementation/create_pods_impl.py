from datetime import datetime, timedelta

# Import generated classes from the compiled proto files
from ethos.elint.collars import Service50DC499999999_pb2
from ethos.elint.services.product.identity.pods import create_pods_pb2
from google.protobuf.timestamp_pb2 import Timestamp


class CreatePodsService():
    def CreatePod(self, request, context):
        # Simulating pod creation with dummy request data
        print(f"Received request to create pod: {request.pod.name}")
        
        # Dummy response for successful pod creation
        response = create_pods_pb2.CreatePodResponse()
        response.message = f"Pod '{request.pod.name}' created successfully with image '{request.pod.image}'!"
        return response

    def GetPods(self, request, context):
        # Simulating fetching a list of pods with dummy data
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

        # Creating response with dummy pods
        response = create_pods_pb2.GetPodsResponse()
        response.pods.extend(dummy_pods)
        return response

    def GetSSHPodCredentials(self, request, context):
        # Simulating SSH credentials response with dummy data
        credentials = Service50DC499999999_pb2.SSHPodCredentials(
            user_name="dummy_user",
            node_ip="192.168.1.1",
            ssh_command="ssh dummy_user@192.168.1.1",
            last_login=self._get_current_timestamp()
        )

        # Creating response with dummy SSH credentials
        response = create_pods_pb2.GetSSHPodCredentialsResponse(credentials=credentials)
        return response

    def GetNodes(self, request, context):
        # Simulating fetching node information with dummy data
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

        # Creating response with dummy nodes
        response = create_pods_pb2.GetNodesResponse()
        response.nodes.extend(dummy_nodes)
        return response

    @staticmethod
    def _get_current_timestamp():
        # Get the current time as google.protobuf.Timestamp
        current_time = datetime.now()
        timestamp = Timestamp()
        timestamp.FromDatetime(current_time)
        return timestamp

    @staticmethod
    def _get_future_timestamp():
        # Get a future timestamp (1 day from now) as google.protobuf.Timestamp
        future_time = datetime.now() + timedelta(days=1)
        timestamp = Timestamp()
        timestamp.FromDatetime(future_time)
        return timestamp

