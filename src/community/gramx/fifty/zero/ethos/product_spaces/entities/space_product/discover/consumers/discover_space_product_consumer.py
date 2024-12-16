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
from ethos.elint.entities import space_product_domain_pb2
from ethos.elint.services.product.product.space_product.access_space_product_pb2 import (
    SpaceProductServicesAccessAuthDetails,
)
from ethos.elint.services.product.product.space_product.discover_space_product_pb2 import (
    GetSpaceProductDomainByIdRequest,
)

from application_context import ApplicationContext


class DiscoverSpaceProductConsumer:

    @staticmethod
    def get_space_product_domain_by_id(
        access_auth_details: SpaceProductServicesAccessAuthDetails,
        space_product_domain_id: str,
    ) -> (bool, str, space_product_domain_pb2.SpaceProductDomain):
        stub = ApplicationContext.discover_space_product_services_stub()
        response = stub.GetSpaceProductDomainById(
            GetSpaceProductDomainByIdRequest(
                access_auth=access_auth_details,
                space_product_domain_id=space_product_domain_id,
            )
        )
        return (
            response.response_meta.meta_done,
            response.response_meta.meta_message,
            response.space_product_domain,
        )

    @staticmethod
    def get_space_product_domains(
        access_auth_details: SpaceProductServicesAccessAuthDetails,
    ) -> (bool, str, [space_product_domain_pb2.SpaceProductDomain]):
        stub = ApplicationContext.discover_space_product_services_stub()
        response = stub.GetSpaceProductDomains(access_auth_details)
        return (
            response.response_meta.meta_done,
            response.response_meta.meta_message,
            response.space_product_domains,
        )
