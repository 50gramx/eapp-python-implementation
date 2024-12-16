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

from ethos.elint.services.product.product.space_product_domain.access_space_product_domain_pb2 import (
    SpaceProductDomainAccessTokenResponse,
    ValidateSpaceProductDomainServicesResponse,
)
from ethos.elint.services.product.product.space_product_domain.access_space_product_domain_pb2_grpc import (
    AccessSpaceProductDomainServiceServicer,
)

from src.community.gramx.fifty.zero.ethos.product_spaces.entities.space_product.access.consumers.access_space_product_consumer import (
    AccessSpaceProductConsumer,
)
from support.session_manager import (
    create_space_product_domain_services_access_auth_details,
    is_persistent_session_valid,
)


class AccessSpaceProductDomainService(AccessSpaceProductDomainServiceServicer):
    def __init__(self):
        super(AccessSpaceProductDomainService, self).__init__()
        self.session_scope = self.__class__.__name__

    def SpaceProductDomainAccessToken(self, request, context):
        logging.info(
            "AccessSpaceProductDomainService:SpaceProductDomainAccessToken invoked."
        )
        validation_done, validation_message = (
            AccessSpaceProductConsumer.validate_space_product_services(
                request.space_product_services_access_auth_details
            )
        )
        if validation_done is False:
            return SpaceProductDomainAccessTokenResponse(
                space_product_domain_services_access_done=validation_done,
                space_product_domain_services_access_message=validation_message,
            )
        else:
            # service_space = ServiceSpace(space_product_id=space_product.space_product_id)
            # space_product_domain = service_space.get_domain_with_id(space_product=space_product, domain_id="")
            # if space_product_domain is None:
            #     create_response = create_account_white_space_product_domain_caller(request)
            #     space_product_domain = create_response.space_product_domain_services_\
            #           access_auth_details.space_product_domain
            access_auth_details = (
                create_space_product_domain_services_access_auth_details(
                    session_scope=self.session_scope,
                    space_product_domain=request.space_product_domain,
                )
            )
            return SpaceProductDomainAccessTokenResponse(
                space_product_domain_services_access_auth_details=access_auth_details,
                space_product_domain_services_access_done=validation_done,
                space_product_domain_services_access_message=validation_message,
            )

    def ValidateSpaceProductDomainServices(self, request, context):
        logging.info(
            "AccessSpaceProductDomainService:ValidateSpaceProductDomainServices invoked."
        )
        space_product_domain = request.space_product_domain
        space_product_domain_services_access_session_token_details = (
            request.space_product_domain_services_access_session_token_details
        )
        session_valid, session_valid_message = is_persistent_session_valid(
            session_token=space_product_domain_services_access_session_token_details.session_token,
            session_identifier=space_product_domain.id,
            session_scope=self.session_scope,
        )
        return ValidateSpaceProductDomainServicesResponse(
            space_product_domain_services_access_validation_done=session_valid,
            space_product_domain_services_access_validation_message=session_valid_message,
        )
