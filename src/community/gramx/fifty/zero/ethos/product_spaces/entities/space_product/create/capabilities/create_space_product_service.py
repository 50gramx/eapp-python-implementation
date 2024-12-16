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

from ethos.elint.services.product.product.space_product.create_space_product_pb2 import (
    CreateAccountSpaceProductResponse,
)
from ethos.elint.services.product.product.space_product.create_space_product_pb2_grpc import (
    CreateSpaceProductServiceServicer,
)

from application_context import ApplicationContext
from community.gramx.fifty.zero.ethos.product_spaces.models.product_space_models import (
    ProductSpace,
)
from src.community.gramx.fifty.zero.ethos.product_spaces.models.space_product_model import (
    SpaceProduct,
)
from support.db_service import add_new_entity
from support.helper_functions import format_timestamp_to_datetime, gen_uuid


class CreateSpaceProductService(CreateSpaceProductServiceServicer):
    def __init__(self):
        super(CreateSpaceProductService, self).__init__()
        self.session_scope = self.__class__.__name__

    def CreateAccountSpaceProduct(self, request, context):
        logging.info("CreateSpaceProductService:CreateAccountSpaceProduct")
        space_services_access_auth_details = request.space_services_access_auth_details
        space_product_name = request.space_product_name
        requested_at = request.requested_at

        # validate the auth details
        access_space_service_stub = ApplicationContext.access_space_service_stub()
        validate_space_service_response = (
            access_space_service_stub.ValidateSpaceServices(
                space_services_access_auth_details
            )
        )
        # handle the response here
        space_service_access_validation_done = (
            validate_space_service_response.space_service_access_validation_done
        )
        space_service_access_validation_message = (
            validate_space_service_response.space_service_access_validation_message
        )

        if space_service_access_validation_done is False:
            # return without creating a space service
            # create the response here
            create_account_space_product_response = CreateAccountSpaceProductResponse(
                create_account_space_product_done=space_service_access_validation_done,
                create_account_space_product_message=space_service_access_validation_message,
            )
        else:
            # create the space service params here
            space_product_id = gen_uuid()
            space = space_services_access_auth_details.space
            space_product_admin_account_id = space.space_admin_id
            # create the space service here
            new_space_product = SpaceProduct(
                space_product_id=space_product_id,
                space_product_name=space_product_name,
                space_product_admin_account_id=space_product_admin_account_id,
                space_id=space.space_id,
                created_at=format_timestamp_to_datetime(requested_at),
            )
            # add the entity to database
            add_new_entity(new_space_product)
            product_space = ProductSpace(space_product_id=space_product_id)
            product_space.setup_product_space()

            # request SpaceProductToken with access_space_product
            # to generate space_product_services_access_auth_details
            access_space_product_service_stub = (
                ApplicationContext.access_space_product_service_stub()
            )
            access_space_product_token_response = (
                access_space_product_service_stub.SpaceProductAccessToken(
                    space_services_access_auth_details
                )
            )
            space_product_services_access_auth_details = (
                access_space_product_token_response.space_product_services_access_auth_details
            )

            # create the response params here
            create_account_space_product_done = True
            create_account_space_product_message = (
                "Space Service successfully created. Thanks."
            )

            # create the response here
            create_account_space_product_response = CreateAccountSpaceProductResponse(
                space_product_services_access_auth_details=space_product_services_access_auth_details,
                create_account_space_product_done=create_account_space_product_done,
                create_account_space_product_message=create_account_space_product_message,
            )
        return create_account_space_product_response
