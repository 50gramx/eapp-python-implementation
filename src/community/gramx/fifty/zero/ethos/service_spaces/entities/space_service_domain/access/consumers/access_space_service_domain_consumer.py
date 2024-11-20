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
from ethos.elint.entities.space_service_domain_pb2 import SpaceServiceDomain
from ethos.elint.services.product.service.space_service.access_space_service_pb2 import (
    SpaceServiceServicesAccessAuthDetails,
)
from ethos.elint.services.product.service.space_service_domain.access_space_service_domain_pb2 import (
    SpaceServiceDomainAccessTokenRequest,
    SpaceServiceDomainServicesAccessAuthDetails,
)

from application_context import ApplicationContext


class AccessSpaceServiceDomainConsumer:

    @staticmethod
    def space_service_domain_access_token(
        access_auth_details: SpaceServiceServicesAccessAuthDetails,
        space_service_domain: SpaceServiceDomain,
    ) -> (SpaceServiceDomainServicesAccessAuthDetails, bool, str):
        stub = ApplicationContext.access_space_service_domain_service_stub()
        response = stub.SpaceServiceDomainAccessToken(
            SpaceServiceDomainAccessTokenRequest(
                space_service_services_access_auth_details=access_auth_details,
                space_service_domain=space_service_domain,
            )
        )
        return (
            response.space_service_domain_services_access_auth_details,
            response.space_service_domain_services_access_done,
            response.space_service_domain_services_access_message,
        )

    @staticmethod
    def validate_space_service_domain_services(
        access_auth_details: SpaceServiceDomainServicesAccessAuthDetails,
    ) -> (bool, str):
        stub = ApplicationContext.access_space_service_domain_service_stub()
        response = stub.ValidateSpaceServiceDomainServices(access_auth_details)
        return (
            response.space_service_domain_services_access_validation_done,
            response.space_service_domain_services_access_validation_message,
        )
