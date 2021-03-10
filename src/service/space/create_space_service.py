from ethos.elint.entities import space_pb2
from ethos.elint.services.product.identity.space.create_space_pb2 import CreateAccountSpaceResponse
from ethos.elint.services.product.identity.space.create_space_pb2_grpc import CreateSpaceServiceServicer
from models.base_models import Space
from support.db_service import add_new_space, get_galaxy
from support.helper_functions import gen_uuid, format_timestamp_to_datetime


class CreateSpaceService(CreateSpaceServiceServicer):
    def __init__(self):
        super(CreateSpaceService, self).__init__()
        self.session_scope = self.__class__.__name__

    def CreateAccountSpace(self, request, context):
        print("CreateSpaceService:CreateAccountSpace invoked.")
        account = request.account
        space_accessibility_type = request.space_accessibility_type
        space_isolation_type = request.space_isolation_type
        requested_at = request.requested_at

        # create the space here
        space_id = gen_uuid()
        account_galaxy_id = account.account_galaxy_id
        account_galaxy = get_galaxy(with_galaxy_id=account_galaxy_id)
        space_admin_id = account.account_id
        space_entity_type = space_pb2.SpaceEntityType.Value('ACCOUNT')

        new_space = Space(
            space_id=space_id,
            space_admin_id=space_admin_id,
            galaxy_id=account_galaxy_id,
            space_accessibility_type=space_accessibility_type,
            space_isolation_type=space_isolation_type,
            space_entity_type=space_entity_type,
            space_created_at=format_timestamp_to_datetime(requested_at)
        )
        add_new_space(new_space)
        # create the response params here
        create_account_space_done = True
        create_account_space_message = "Space successfully created. Thanks."
        account_space = space_pb2.Space(
            galaxy=account_galaxy,
            space_id=space_id,
            space_accessibility_type=space_accessibility_type,
            space_isolation_type=space_isolation_type,
            space_entity_type=space_entity_type
        )
        # create the response here
        create_account_space_response = CreateAccountSpaceResponse(
            space=account_space,
            create_account_space_done=create_account_space_done,
            create_account_space_message=create_account_space_message
        )
        return create_account_space_response
