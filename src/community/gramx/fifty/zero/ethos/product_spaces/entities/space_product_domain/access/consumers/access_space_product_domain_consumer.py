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
from ethos.elint.entities.space_product_domain_pb2 import SpaceProductDomain
from ethos.elint.services.product.product.space_product.access_space_product_pb2 import (
    SpaceProductServicesAccessAuthDetails,
)
from ethos.elint.services.product.product.space_product_domain.access_space_product_domain_pb2 import (
    SpaceProductDomainAccessTokenRequest,
    SpaceProductDomainServicesAccessAuthDetails,
)

from application_context import ApplicationContext


class AccessSpaceProductDomainConsumer:

    @staticmethod
    def space_product_domain_access_token(
        access_auth_details: SpaceProductServicesAccessAuthDetails,
        space_product_domain: SpaceProductDomain,
    ) -> (SpaceProductDomainServicesAccessAuthDetails, bool, str):
        stub = ApplicationContext.access_space_product_domain_service_stub()
        response = stub.SpaceProductDomainAccessToken(
            SpaceProductDomainAccessTokenRequest(
                space_product_services_access_auth_details=access_auth_details,
                space_product_domain=space_product_domain,
            )
        )
        return (
            response.space_product_domain_services_access_auth_details,
            response.space_product_domain_services_access_done,
            response.space_product_domain_services_access_message,
        )

    @staticmethod
    def validate_space_product_domain_services(
        access_auth_details: SpaceProductDomainServicesAccessAuthDetails,
    ) -> (bool, str):
        stub = ApplicationContext.access_space_product_domain_service_stub()
        response = stub.ValidateSpaceProductDomainServices(access_auth_details)
        return (
            response.space_product_domain_services_access_validation_done,
            response.space_product_domain_services_access_validation_message,
        )
