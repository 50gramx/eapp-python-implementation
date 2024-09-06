import grpc
from concurrent import futures
from db_session import DbSession

from ethos.elint.services.product.identity.space_things.create_space_things_pb2 import CreateThingsSpaceDomainRequest, CreateThingsSpaceDomainResponse
from ethos.elint.services.product.identity.space_things.create_space_things_pb2_grpc import CreateServiceServicer, add_CreateServiceServicer_to_server

from community.gramx.fifty.zero.ethos.things_spaces.models.base_models import SpaceThings
from community.gramx.fifty.zero.ethos.things_spaces.models.things_space_models import ThingsSpace

class CreateService(CreateServiceServicer):

    def CreateThingsSpaceDomain(self, request: CreateThingsSpaceDomainRequest, context: grpc.ServicerContext) -> CreateThingsSpaceDomainResponse:
        space_things_id = None
        
        try:
            # Check if SpaceThings already exists
            with DbSession.session_scope() as session:
                existing_space_thing = session.query(SpaceThings).filter_by(name=request.space_things_name).first()
                if existing_space_thing:
                    space_things_id = existing_space_thing.id
                else:
                    # Validate required fields
                    if not request.admin_id or not request.space_id:
                        context.set_details("Admin ID and Space ID are required to create a new SpaceThings.")
                        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                        return CreateThingsSpaceDomainResponse()

                    # Create a new SpaceThings using the class method
                    space_things_id = SpaceThings.add_new_space_things(
                        session=session,
                        name=request.space_things_name,
                        admin_id=request.admin_id,
                        space_id=request.space_id,
                    )

            # Handle missing domain_collar_id
            domain_collar_id = request.domain_collar_id if request.domain_collar_id else "default_collar_id"

            # Create a SpaceThingsDomain
            domain_model = ThingsSpace(space_things_id=space_things_id)
            domain_id = domain_model.add_new_domain(
                domain_name=request.domain_name,
                domain_description=request.domain_description,
                domain_collar_id=domain_collar_id,
                domain_isolate=request.domain_isolate or False  # or True based on the request properties
            )

            # Retrieve the created domain to return
            space_things_domain = domain_model.get_domain_with_id(
                SpaceThings(id=space_things_id),
                domain_id
            )

            return CreateThingsSpaceDomainResponse(
                domain=space_things_domain
            )

        except grpc.RpcError as e:
            context.set_details(f"gRPC error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return CreateThingsSpaceDomainResponse()

        except Exception as e:
            context.set_details(f"Unexpected error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return CreateThingsSpaceDomainResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_CreateServiceServicer_to_server(CreateService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
