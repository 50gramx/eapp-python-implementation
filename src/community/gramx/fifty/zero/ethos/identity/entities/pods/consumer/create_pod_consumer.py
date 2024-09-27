import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime, timedelta

# Import the generated classes
from ethos.elint.services.product.identity.pods import create_pods_pb2, create_pods_pb2_grpc
from ethos.elint.collars import Service50DC499999999_pb2

# Establish a connection to the server
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        print('COnsumer started')
        stub = create_pods_pb2_grpc.CreatePodsServiceStub(channel)

        # 1. Calling CreatePod
        print("----- Calling CreatePod -----")
        expiration_time = _get_future_timestamp()

        pod = Service50DC499999999_pb2.Pod(
            name="consumer-pod-1",
            image="consumer/image:v1",
            container_ports=[8080, 9090],
            env_vars=[
                Service50DC499999999_pb2.EnvVar(name="EXAMPLE_ENV", value="12345")
            ], 
            expiration_time=expiration_time
        )

        create_pod_request = create_pods_pb2.CreatePodRequest(pod=pod)
        create_pod_response = stub.CreatePod(create_pod_request)
        print(f"CreatePod Response: {create_pod_response.message}\n")

        # 2. Calling GetPods
        print("----- Calling GetPods -----")
        get_pods_request = create_pods_pb2.GetPodsRequest()
        get_pods_response = stub.GetPods(get_pods_request)
        for pod in get_pods_response.pods:
            print(f"Pod Name: {pod.name}, Image: {pod.image}, Expiration: {pod.expiration_time}\n")

        # 3. Calling GetSSHPodCredentials
        print("----- Calling GetSSHPodCredentials -----")
        ssh_pod_request = create_pods_pb2.GetSSHPodCredentialsRequest(pod_name="consumer-pod-1")
        ssh_pod_response = stub.GetSSHPodCredentials(ssh_pod_request)
        print(f"SSH Credentials:\n Username: {ssh_pod_response.credentials.user_name}\n"
              f" Node IP: {ssh_pod_response.credentials.node_ip}\n"
              f" SSH Command: {ssh_pod_response.credentials.ssh_command}\n"
              f" Last Login: {ssh_pod_response.credentials.last_login}\n")

        # 4. Calling GetNodes
        print("----- Calling GetNodes -----")
        get_nodes_request = create_pods_pb2.GetNodesRequest()
        get_nodes_response = stub.GetNodes(get_nodes_request)
        for node in get_nodes_response.nodes:
            print(f"Node Name: {node.name}, Status: {node.status}\n"
                  f"Addresses: {node.addresses}, Labels: {node.labels}\n")


def _get_current_timestamp():
    """Helper function to return current time as google.protobuf.Timestamp."""
    current_time = datetime.now()
    timestamp = Timestamp()
    timestamp.FromDatetime(current_time)
    return timestamp


def _get_future_timestamp():
    """Helper function to return a future timestamp (1 day from now) as google.protobuf.Timestamp."""
    future_time = datetime.now() + timedelta(days=1)
    timestamp = Timestamp()
    timestamp.FromDatetime(future_time)
    return timestamp


if __name__ == '__main__':
    run()
