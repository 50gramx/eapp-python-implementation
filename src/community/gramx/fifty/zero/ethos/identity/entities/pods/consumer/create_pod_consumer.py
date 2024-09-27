import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime, timedelta

# Import the generated classes
from ethos.elint.services.product.identity.pods import create_pods_pb2, create_pods_pb2_grpc
from ethos.elint.collars import Service50DC499999999_pb2

    
    
def run():
    # Establish a connection to the server
    with grpc.insecure_channel('localhost:50051') as channel:  # Use the port you set in the server
        stub = create_pods_pb2_grpc.CreatePodsServiceStub(channel)

        # Create a pod
        pod = Service50DC499999999_pb2.Pod(name='my-pod', image='my-image')  # Update this line
        create_pod_request = create_pods_pb2.CreatePodRequest(pod=pod)
        create_pod_response = stub.CreatePod(create_pod_request)
        print("CreatePod Response:", create_pod_response.message)

        # Get pods
        get_pods_request = create_pods_pb2.GetPodsRequest()
        get_pods_response = stub.GetPods(get_pods_request)
        print("GetPods Response:")
        for p in get_pods_response.pods:
            print(f" - Pod Name: {p.name}, Image: {p.image}")

        # Get SSH credentials
        ssh_request = create_pods_pb2.GetSSHPodCredentialsRequest(pod_name='my-pod')
        ssh_response = stub.GetSSHPodCredentials(ssh_request)
        print("GetSSHPodCredentials Response:")
        print(f" - User: {ssh_response.credentials.user_name}, IP: {ssh_response.credentials.node_ip}")

        # Get nodes
        get_nodes_request = create_pods_pb2.GetNodesRequest()
        get_nodes_response = stub.GetNodes(get_nodes_request)
        print("GetNodes Response:")
        for node in get_nodes_response.nodes:
            print(f" - Node Name: {node.name}")

if __name__ == '__main__':
    run()

