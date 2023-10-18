#   /*************************************************************************
#   *
#   * AMIT KUMAR KHETAN CONFIDENTIAL
#   * __________________
#   *
#   *  [2017] - [2021] Amit Kumar Khetan
#   *  All Rights Reserved.
#   *
#   * NOTICE:  All information contained herein is, and remains
#   * the property of Amit Kumar Khetan and its suppliers,
#   * if any.  The intellectual and technical concepts contained
#   * herein are proprietary to Amit Kumar Khetan
#   * and its suppliers and may be covered by U.S. and Foreign Patents,
#   * patents in process, and are protected by trade secret or copyright law.
#   * Dissemination of this information or reproduction of this material
#   * is strictly forbidden unless prior written permission is obtained
#   * from Amit Kumar Khetan.
#   */

from ethos.elint.entities import space_pb2
from ethos.elint.services.product.identity.space.create_space_pb2 import CreateAccountSpaceResponse
from ethos.elint.services.product.identity.space.create_space_pb2_grpc import CreateSpaceServiceServicer

from models.base_models import Space
from support.database.galaxy_services import get_galaxy
from support.database.space_services import add_new_space
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
