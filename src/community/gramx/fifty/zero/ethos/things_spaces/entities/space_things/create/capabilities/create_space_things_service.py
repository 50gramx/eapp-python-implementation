import logging

from ethos.elint.services.product.identity.space.create_space_things_pb2 import (
    CreateThingsSpaceDomainResponse, CreateNodesCollarResponse
)
from ethos.elint.services.product.identity.space.create_space_things_pb2_grpc import (
    CreateServiceServicer
)

from application_context import ApplicationContext
from ethos.elint.entities.space_things_domain import SpaceThingsDomain
from ethos.elint.collars.Things50DC500000000 import Things50DC500000000
from support.db_service import add_new_entity
from support.helper_functions import gen_uuid


class CreateSpaceThingsService(CreateServiceServicer):
    def __init__(self):
        super(CreateSpaceThingsService, self).__init__()
        self.session_scope = self.__class__.__name__

    def CreateThingsSpaceDomain(self, request, context):
        logging.info("CreateSpaceThingsService:CreateThingsSpaceDomain invoked.")
        
        # Extract request details
        name = request.name
        description = request.description
        properties = request.properties

        # Generate a new SpaceThingsDomain
        space_things_domain_id = gen_uuid()
        new_space_things_domain = SpaceThingsDomain(
            space_things_domain_id=space_things_domain_id,
            name=name,
            description=description,
            properties=properties
        )

        # Save the SpaceThingsDomain entity to the database
        add_new_entity(new_space_things_domain)

        # Prepare the response
        create_things_space_domain_response = CreateThingsSpaceDomainResponse(
            domain=new_space_things_domain
        )

        return create_things_space_domain_response

    def CreateNodesCollar(self, request, context):
        logging.info("CreateSpaceThingsService:CreateNodesCollar invoked.")
        
        # Extract request collar details
        collar_request = request.collar
        
        # Validate collar details or perform additional logic (if needed)
        collar_id = gen_uuid()
        new_collar = Things50DC500000000(
            node_id=collar_id,
            name=collar_request.name,
            machine_class=collar_request.machine_class,
            storage_class=collar_request.storage_class,
            bandwidth_class=collar_request.bandwidth_class,
            operator_class=collar_request.operator_class,
            hashing_class=collar_request.hashing_class,
            base_os=collar_request.base_os,
            orchestrator_os=collar_request.orchestrator_os,
            node_liability=collar_request.node_liability,
            created_at=collar_request.created_at
        )

        # Save the collar entity to the database
        add_new_entity(new_collar)

        # Prepare the response
        create_nodes_collar_response = CreateNodesCollarResponse(
            collar=new_collar
        )

        return create_nodes_collar_response
