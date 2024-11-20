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
import logging

from ethos.elint.services.product.service.space_service.create_space_service_pb2 import (
    CreateAccountSpaceServiceResponse,
)
from ethos.elint.services.product.service.space_service.create_space_service_pb2_grpc import (
    CreateSpaceServiceServiceServicer,
)

from application_context import ApplicationContext
from community.gramx.fifty.zero.ethos.service_spaces.models.service_space_models import (
    ServiceSpace,
)
from src.community.gramx.fifty.zero.ethos.service_spaces.models.space_service_model import (
    SpaceService,
)
from support.data_store import DataStore
from support.db_service import add_new_entity
from support.helper_functions import format_timestamp_to_datetime, gen_uuid


class CreateSpaceServiceService(CreateSpaceServiceServiceServicer):
    def __init__(self):
        super(CreateSpaceServiceService, self).__init__()
        self.session_scope = self.__class__.__name__

    def CreateAccountSpaceService(self, request, context):
        logging.info("CreateSpaceServiceService:CreateAccountSpaceService")
        space_service_access_auth_details = request.space_service_access_auth_details
        space_service_name = request.space_service_name
        requested_at = request.requested_at

        # validate the auth details
        access_space_service_stub = ApplicationContext.access_space_service_stub()
        validate_space_services_response = (
            access_space_service_stub.ValidateSpaceServices(
                space_service_access_auth_details
            )
        )
        # handle the response here
        space_service_access_validation_done = (
            validate_space_services_response.space_service_access_validation_done
        )
        space_service_access_validation_message = (
            validate_space_services_response.space_service_access_validation_message
        )

        if space_service_access_validation_done is False:
            # return without creating a space service
            # create the response here
            create_account_space_service_response = CreateAccountSpaceServiceResponse(
                create_account_space_service_done=space_service_access_validation_done,
                create_account_space_service_message=space_service_access_validation_message,
            )
        else:
            # create the space service params here
            space_service_id = gen_uuid()
            space = space_service_access_auth_details.space
            space_service_admin_account_id = space.space_admin_id
            # create the space service here
            new_space_service = SpaceService(
                space_service_id=space_service_id,
                space_service_name=space_service_name,
                space_service_admin_account_id=space_service_admin_account_id,
                space_id=space.space_id,
                created_at=format_timestamp_to_datetime(requested_at),
            )
            # add the entity to database
            add_new_entity(new_space_service)
            service_space = ServiceSpace(space_service_id=space_service_id)
            service_space.setup_service_space()

            # request SpaceServiceToken with access_space_service
            # to generate space_service_services_access_auth_details
            access_space_service_service_stub = (
                ApplicationContext.access_space_service_service_stub()
            )
            access_space_service_token_response = (
                access_space_service_service_stub.SpaceServiceAccessToken(
                    space_service_access_auth_details
                )
            )
            space_service_services_access_auth_details = (
                access_space_service_token_response.space_service_services_access_auth_details
            )

            # create the space service key in data store
            data_store_client = DataStore()
            data_store_client.create_space_service(
                space_service=space_service_services_access_auth_details.space_service
            )

            # create the response params here
            create_account_space_service_done = True
            create_account_space_service_message = (
                "Space Service successfully created. Thanks."
            )

            # create the response here
            create_account_space_service_response = CreateAccountSpaceServiceResponse(
                space_service_services_access_auth_details=space_service_services_access_auth_details,
                create_account_space_service_done=create_account_space_service_done,
                create_account_space_service_message=create_account_space_service_message,
            )
        return create_account_space_service_response
