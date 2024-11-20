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
from ethos.elint.entities import space_service_domain_pb2
from ethos.elint.services.product.service.space_service.access_space_service_pb2 import (
    SpaceServiceServicesAccessAuthDetails,
)
from ethos.elint.services.product.service.space_service.discover_space_service_pb2 import (
    GetSpaceServiceDomainByIdRequest,
)

from application_context import ApplicationContext


class DiscoverSpaceServiceConsumer:

    @staticmethod
    def get_space_service_domain_by_id(
        access_auth_details: SpaceServiceServicesAccessAuthDetails,
        space_service_domain_id: str,
    ) -> (bool, str, space_service_domain_pb2.SpaceServiceDomain):
        stub = ApplicationContext.discover_space_service_services_stub()
        response = stub.GetSpaceServiceDomainById(
            GetSpaceServiceDomainByIdRequest(
                access_auth=access_auth_details,
                space_service_domain_id=space_service_domain_id,
            )
        )
        return (
            response.response_meta.meta_done,
            response.response_meta.meta_message,
            response.space_service_domain,
        )

    @staticmethod
    def get_space_service_domains(
        access_auth_details: SpaceServiceServicesAccessAuthDetails,
    ) -> (bool, str, [space_service_domain_pb2.SpaceServiceDomain]):
        stub = ApplicationContext.discover_space_service_services_stub()
        response = stub.GetSpaceServiceDomains(access_auth_details)
        return (
            response.response_meta.meta_done,
            response.response_meta.meta_message,
            response.space_service_domains,
        )
