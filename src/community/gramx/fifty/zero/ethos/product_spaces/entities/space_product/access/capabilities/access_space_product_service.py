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

from ethos.elint.services.product.product.space_product.access_space_product_pb2 import (
    SpaceProductAccessTokenResponse,
    ValidateSpaceProductServicesResponse,
)
from ethos.elint.services.product.product.space_product.access_space_product_pb2_grpc import (
    AccessSpaceProductServiceServicer,
)

from community.gramx.fifty.zero.ethos.identity.entities.space.access.consumers.access_space_consumer import (
    AccessSpaceConsumer,
)
from src.community.gramx.fifty.zero.ethos.product_spaces.entities.space_product.create.consumers.create_space_product_consumer import (
    CreateAccountSpaceProductConsumer,
)
from src.community.gramx.fifty.zero.ethos.product_spaces.models.space_product_model import (
    get_space_product,
)
from support.session_manager import (
    create_space_product_services_access_auth_details,
    is_persistent_session_valid,
)


class AccessSpaceProductService(AccessSpaceProductServiceServicer):
    def __init__(self):
        super(AccessSpaceProductService, self).__init__()
        self.session_scope = self.__class__.__name__

    def SpaceProductAccessToken(self, request, context):
        logging.info("AccessSpaceProductService:SpaceProductAccessToken invoked.")
        validation_done, validation_message = (
            AccessSpaceConsumer.validate_space_services(request)
        )
        if validation_done is False:
            return SpaceProductAccessTokenResponse(
                space_product_services_access_done=validation_done,
                space_product_services_access_message=validation_message,
            )
        else:
            space_product = get_space_product(
                space=request.space, with_space_id=request.space.space_id
            )
            if space_product is None:
                # TODO: Change to access auth after updating contract
                create_response = (
                    CreateAccountSpaceProductConsumer.create_account_space_product(
                        request
                    )
                )
                space_product = (
                    create_response.space_product_services_access_auth_details.space_product
                )
            space_product_services_access_auth_details = (
                create_space_product_services_access_auth_details(
                    session_scope=self.session_scope, space_product=space_product
                )
            )
            return SpaceProductAccessTokenResponse(
                space_product_services_access_auth_details=space_product_services_access_auth_details,
                space_product_services_access_done=validation_done,
                space_product_services_access_message=validation_message,
            )

    def ValidateSpaceProductServices(self, request, context):
        logging.info("AccessSpaceProductService:ValidateSpaceProductServices invoked.")
        space_product = request.space_product
        space_product_services_access_session_token_details = (
            request.space_product_services_access_session_token_details
        )

        # validate the space service
        if not space_product.space_product_id == space_product.space_product_id:
            space_product_services_access_validation_done = False
            space_product_services_access_validation_message = (
                "Requesting space service is not legit. "
                "This action will be reported."
            )
            # create the response here
            validate_space_product_services_response = ValidateSpaceProductServicesResponse(
                space_product_services_access_validation_done=space_product_services_access_validation_done,
                space_product_services_access_validation_message=space_product_services_access_validation_message,
            )
            return validate_space_product_services_response
        else:
            # validate the session
            session_valid, session_valid_message = is_persistent_session_valid(
                session_token=space_product_services_access_session_token_details.session_token,
                session_identifier=space_product.space_product_id,
                session_scope=self.session_scope,
            )
            # create the response here
            validate_space_product_services_response = ValidateSpaceProductServicesResponse(
                space_product_services_access_validation_done=session_valid,
                space_product_services_access_validation_message=session_valid_message,
            )
            return validate_space_product_services_response
