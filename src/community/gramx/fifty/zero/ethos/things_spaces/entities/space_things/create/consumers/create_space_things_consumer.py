from ethos.elint.services.product.identity.space_things.create_space_things_pb2 import (
    CreateThingsSpaceDomainRequest, CreateNodesCollarRequest
)
from ethos.elint.services.product.identity.space.access_space_pb2 import SpaceServicesAccessAuthDetails
from ethos.elint.collars.Things50DC500000000_pb2 import Things50DC500000000

from application_context import ApplicationContext
from support.helper_functions import get_current_timestamp


class CreateSpaceThingsConsumer:

    @staticmethod
    def create_things_space_domain(access_auth: SpaceServicesAccessAuthDetails):
        # Stub to connect to the gRPC service
        stub = ApplicationContext.get_create_space_things_domain_service()
        
        # Define the request for creating a new SpaceThings domain
        request = CreateThingsSpaceDomainRequest(
            name="My Space Domain",
            description="This is a new space domain for my space things",
            properties={
                "property1": "value1",
                "property2": "value2"
            }
        )
        
        # Make the gRPC call and return the response
        return stub.CreateThingsSpaceDomain(request)

    @staticmethod
    def create_nodes_collar(access_auth: SpaceServicesAccessAuthDetails):
        # Stub to connect to the gRPC service
        stub = ApplicationContext.create_space_things_service_stub()

        # Define a new collar to be added
        collar_request = Things50DC500000000(
            name="Node Collar",
            machine_class={
                "id": "mc-001",
                "main_class": "High Performance",
                "sub_classes": "GPU, High Memory",
                "vcpu": 16,
                "ram_gib": 64.0,
                "machine_type": "n1-standard",
                "machine_category": "Compute Optimized"
            },
            storage_class={
                "id": "sc-001",
                "main_class": "Fast Storage",
                "sub_classes": "SSD, NVMe",
                "fast_storage": 100.0,
                "standard_storage": 500.0,
                "slow_storage": 1000.0
            },
            bandwidth_class={
                "id": "bc-001",
                "main_class": "High Bandwidth",
                "sub_classes": "Fiber",
                "locale_network_bandwidth_class": 10000.0,
                "main_network_bandwidth_class": 1000.0,
                "main_network_bandwidth_static_address": True
            },
            operator_class={
                "id": "op-001",
                "main_class": "Certified",
                "sub_classes": "Human, AI",
                "human_operator_class": True,
                "collaborator_operator_class": False,
                "certified_operator_class": True
            },
            hashing_class={
                "id": "hc-001",
                "main_class": "SHA-256",
                "sub_classes": "Cryptographic",
                "chain_hash_generation_class": True
            },
            base_os={
                "id": "bos-001",
                "name": "Ubuntu",
                "arch": "x86_64"
            },
            orchestrator_os={
                "id": "oros-001",
                "name": "Kubernetes",
                "version": "1.21"
            },
            node_liability={
                "id": "nl-001",
                "liability": "High",
                "license_id": "lic-001"
            },
            created_at=get_current_timestamp()
        )

        # Create the request for creating a collar node
        request = CreateNodesCollarRequest(collar=collar_request)
        
        # Make the gRPC call and return the response
        return stub.CreateNodesCollar(request)
