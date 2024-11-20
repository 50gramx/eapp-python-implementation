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
from ethos.elint.services.product.identity.space.access_space_pb2 import (
    SpaceServicesAccessAuthDetails,
)
from ethos.elint.services.product.service.space_service.access_space_service_pb2 import (
    SpaceServiceServicesAccessAuthDetails,
)

from application_context import ApplicationContext


class AccessSpaceServiceConsumer:

    @staticmethod
    def validate_space_service_services(
        access_auth_details: SpaceServiceServicesAccessAuthDetails,
    ) -> (bool, str):
        stub = ApplicationContext.access_space_service_service_stub()
        response = stub.ValidateSpaceServiceServices(access_auth_details)
        return (
            response.space_service_services_access_validation_done,
            response.space_service_services_access_validation_message,
        )

    @staticmethod
    def space_service_access_token(
        access_auth_details: SpaceServicesAccessAuthDetails,
    ) -> (bool, str, SpaceServiceServicesAccessAuthDetails):
        stub = ApplicationContext.access_space_service_service_stub()
        response = stub.SpaceServiceAccessToken(access_auth_details)
        return (
            response.space_service_services_access_done,
            response.space_service_services_access_message,
            response.space_service_services_access_auth_details,
        )
