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


from ethos.elint.collars.DC499999994_caps_pb2 import (
    AuthWithSkincareProduct,
    RepeatedDC499999994,
    SPDAuthWithCollarID,
)
from ethos.elint.collars.DC499999994_pb2 import DC499999994
from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.knowledge.space_knowledge.access_space_knowledge_pb2 import (
    SpaceKnowledgeServicesAccessAuthDetails,
)
from ethos.elint.services.product.product.space_product_domain.access_space_product_domain_pb2 import (
    SpaceProductDomainServicesAccessAuthDetails,
)

from src.application_context import ApplicationContext


class DC499999994EPME5000Consumer:

    @staticmethod
    def create(request: AuthWithSkincareProduct) -> ResponseMeta:
        stub = ApplicationContext.dc499999994_epme5000_capabilities_stub()
        response = stub.Create(request)
        return response

    @staticmethod
    def list(
        request: SpaceProductDomainServicesAccessAuthDetails,
    ) -> RepeatedDC499999994:
        stub = ApplicationContext.dc499999994_epme5000_capabilities_stub()
        response = stub.List(request)
        return response

    @staticmethod
    def get(
        spd_auth: SpaceProductDomainServicesAccessAuthDetails,
        sk_auth: SpaceKnowledgeServicesAccessAuthDetails,
        c_id: str,
    ) -> DC499999994:
        stub = ApplicationContext.dc499999994_epme5000_capabilities_stub()
        request = SPDAuthWithCollarID(auth=spd_auth, sk_auth=sk_auth, collar_id=c_id)
        response = stub.Get(request)
        return response
