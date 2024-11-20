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

from ethos.elint.services.product.service.space_service_domain.access_space_service_domain_pb2 import (
    SpaceServiceDomainAccessTokenResponse,
    ValidateSpaceServiceDomainServicesResponse,
)
from ethos.elint.services.product.service.space_service_domain.access_space_service_domain_pb2_grpc import (
    AccessSpaceServiceDomainServiceServicer,
)

from src.community.gramx.fifty.zero.ethos.service_spaces.entities.space_service.access.consumers.access_space_service_consumer import (
    AccessSpaceServiceConsumer,
)
from support.session_manager import (
    create_space_service_domain_services_access_auth_details,
    is_persistent_session_valid,
)


class AccessSpaceServiceDomainService(AccessSpaceServiceDomainServiceServicer):
    def __init__(self):
        super(AccessSpaceServiceDomainService, self).__init__()
        self.session_scope = self.__class__.__name__

    def SpaceServiceDomainAccessToken(self, request, context):
        logging.info(
            "AccessSpaceServiceDomainService:SpaceServiceDomainAccessToken invoked."
        )
        validation_done, validation_message = (
            AccessSpaceServiceConsumer.validate_space_service_services(
                request.space_service_services_access_auth_details
            )
        )
        if validation_done is False:
            return SpaceServiceDomainAccessTokenResponse(
                space_service_domain_services_access_done=validation_done,
                space_service_domain_services_access_message=validation_message,
            )
        else:
            # service_space = ServiceSpace(space_service_id=space_service.space_service_id)
            # space_service_domain = service_space.get_domain_with_id(space_service=space_service, domain_id="")
            # if space_service_domain is None:
            #     create_response = create_account_white_space_service_domain_caller(request)
            #     space_service_domain = create_response.space_service_domain_services_\
            #           access_auth_details.space_service_domain
            access_auth_details = (
                create_space_service_domain_services_access_auth_details(
                    session_scope=self.session_scope,
                    space_service_domain=request.space_service_domain,
                )
            )
            return SpaceServiceDomainAccessTokenResponse(
                space_service_domain_services_access_auth_details=access_auth_details,
                space_service_domain_services_access_done=validation_done,
                space_service_domain_services_access_message=validation_message,
            )

    def ValidateSpaceServiceDomainServices(self, request, context):
        logging.info(
            "AccessSpaceServiceDomainService:ValidateSpaceServiceDomainServices invoked."
        )
        space_service_domain = request.space_service_domain
        space_service_domain_services_access_session_token_details = (
            request.space_service_domain_services_access_session_token_details
        )
        session_valid, session_valid_message = is_persistent_session_valid(
            session_token=space_service_domain_services_access_session_token_details.session_token,
            session_identifier=space_service_domain.id,
            session_scope=self.session_scope,
        )
        return ValidateSpaceServiceDomainServicesResponse(
            space_service_domain_services_access_validation_done=session_valid,
            space_service_domain_services_access_validation_message=session_valid_message,
        )
