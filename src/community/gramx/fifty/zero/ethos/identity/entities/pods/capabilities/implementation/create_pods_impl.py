from datetime import datetime, timedelta

# Import generated classes from the compiled proto files
from ethos.elint.collars import Service50DC499999999_pb2
from ethos.elint.services.product.identity.pods import create_pods_pb2
from google.protobuf.timestamp_pb2 import Timestamp



class CreatePodsService():
    def CreatePod(self, request, context):
        # Implement your logic to create a pod
        pod = request.pod
        # Simulate pod creation logic
        response_message = f"Pod '{pod.name}' created successfully."
        return create_pods_pb2.CreatePodResponse(message=response_message)

    def GetPods(self, request, context):
        # Simulate fetching pods
        pods = [Service50DC499999999_pb2.Pod(name='pod1', image='nginx'),
                Service50DC499999999_pb2.Pod(name='pod2', image='redis')]
        return create_pods_pb2.GetPodsResponse(pods=pods)

    def GetSSHPodCredentials(self, request, context):
        # Simulate fetching SSH credentials
        credentials = Service50DC499999999_pb2.SSHPodCredentials(
            user_name='admin',
            node_ip='192.168.1.1',
            ssh_command='ssh admin@192.168.1.1',
            last_login=Timestamp()
        )
        return create_pods_pb2.GetSSHPodCredentialsResponse(credentials=credentials)

    def GetNodes(self, request, context):
        # Simulate fetching node info
        nodes = [
            Service50DC499999999_pb2.NodeInfo(name='node1'),
            Service50DC499999999_pb2.NodeInfo(name='node2')
        ]
        return create_pods_pb2.GetNodesResponse(nodes=nodes)