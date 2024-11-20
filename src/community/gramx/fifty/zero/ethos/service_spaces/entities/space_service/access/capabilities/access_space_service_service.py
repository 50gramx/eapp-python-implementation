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

from ethos.elint.services.product.service.space_service.access_space_service_pb2 import (
    SpaceServicesAccessTokenResponse,
    ValidateSpaceServiceServicesResponse,
)
from ethos.elint.services.product.service.space_service.access_space_service_pb2_grpc import (
    AccessSpaceServiceServiceServicer,
)

from community.gramx.fifty.zero.ethos.identity.entities.space.access.consumers.access_space_consumer import (
    AccessSpaceConsumer,
)
from src.community.gramx.fifty.zero.ethos.service_spaces.entities.space_service.create.consumers.create_space_service_consumer import (
    CreateAccountSpaceServiceConsumer,
)
from src.community.gramx.fifty.zero.ethos.service_spaces.models.space_service_model import (
    get_space_service,
)
from support.session_manager import (
    create_space_service_services_access_auth_details,
    is_persistent_session_valid,
)


class AccessSpaceServiceService(AccessSpaceServiceServiceServicer):
    def __init__(self):
        super(AccessSpaceServiceService, self).__init__()
        self.session_scope = self.__class__.__name__

    def SpaceServiceAccessToken(self, request, context):
        logging.info("AccessSpaceServiceService:SpaceServiceAccessToken invoked.")
        validation_done, validation_message = (
            AccessSpaceConsumer.validate_space_services(request)
        )
        if validation_done is False:
            return SpaceServicesAccessTokenResponse(
                space_service_services_access_done=validation_done,
                space_service_services_access_message=validation_message,
            )
        else:
            space_service = get_space_service(
                space=request.space, with_space_id=request.space.space_id
            )
            if space_service is None:
                # TODO: Change to access auth after updating contract
                create_response = (
                    CreateAccountSpaceServiceConsumer.create_account_space_service(
                        request
                    )
                )
                space_service = (
                    create_response.space_service_services_access_auth_details.space_service
                )
            space_service_services_access_auth_details = (
                create_space_service_services_access_auth_details(
                    session_scope=self.session_scope, space_service=space_service
                )
            )
            return SpaceServicesAccessTokenResponse(
                space_service_services_access_auth_details=space_service_services_access_auth_details,
                space_service_services_access_done=validation_done,
                space_service_services_access_message=validation_message,
            )

    def ValidateSpaceServiceServices(self, request, context):
        logging.info("AccessSpaceServiceService:ValidateSpaceServiceServices invoked.")
        space_service = request.space_service
        space_service_services_access_session_token_details = (
            request.space_service_services_access_session_token_details
        )

        # validate the space service
        if not space_service.space_service_id == space_service.space_service_id:
            space_service_services_access_validation_done = False
            space_service_services_access_validation_message = (
                "Requesting space service is not legit. "
                "This action will be reported."
            )
            # create the response here
            validate_space_service_services_response = ValidateSpaceServiceServicesResponse(
                space_service_services_access_validation_done=space_service_services_access_validation_done,
                space_service_services_access_validation_message=space_service_services_access_validation_message,
            )
            return validate_space_service_services_response
        else:
            # validate the session
            session_valid, session_valid_message = is_persistent_session_valid(
                session_token=space_service_services_access_session_token_details.session_token,
                session_identifier=space_service.space_service_id,
                session_scope=self.session_scope,
            )
            # create the response here
            validate_space_service_services_response = ValidateSpaceServiceServicesResponse(
                space_service_services_access_validation_done=session_valid,
                space_service_services_access_validation_message=session_valid_message,
            )
            return validate_space_service_services_response
