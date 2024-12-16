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

from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.product.space_product.discover_space_product_pb2 import (
    GetDomainsByCollarCodeResponse,
    GetSpaceProductDomainByIdResponse,
    GetSpaceProductDomainsResponse,
)
from ethos.elint.services.product.product.space_product.discover_space_product_pb2_grpc import (
    DiscoverSpaceProductServiceServicer,
)

from community.gramx.fifty.zero.ethos.product_spaces.models.product_space_models import (
    ProductSpace,
)
from src.community.gramx.fifty.zero.ethos.product_spaces.entities.space_product.access.consumers.access_space_product_consumer import (
    AccessSpaceProductConsumer,
)


class DiscoverSpaceProductService(DiscoverSpaceProductServiceServicer):
    def __init__(self):
        super(DiscoverSpaceProductService, self).__init__()
        self.session_scope = self.__class__.__name__

    def GetSpaceProductDomains(self, request, context):
        logging.info("DiscoverSpaceProductService:GetSpaceProductDomains")
        validation_done, validation_message = (
            AccessSpaceProductConsumer.validate_space_product_services(
                access_auth_details=request
            )
        )
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetSpaceProductDomainsResponse(response_meta=meta)
        else:
            # get all domains
            product_space = ProductSpace(
                space_product_id=request.space_product.space_product_id
            )
            space_product_domains = product_space.get_domain_all(
                space_product=request.space_product
            )
            return GetSpaceProductDomainsResponse(
                space_product_domains=space_product_domains, response_meta=meta
            )

    def GetSpaceProductDomainById(self, request, context):
        validation_done, validation_message = (
            AccessSpaceProductConsumer.validate_space_product_services(
                access_auth_details=request.access_auth
            )
        )
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetSpaceProductDomainByIdResponse(response_meta=meta)
        else:
            space_product = request.access_auth.space_product
            product_space = ProductSpace(
                space_product_id=space_product.space_product_id
            )
            space_product_domain = product_space.get_domain_with_id(
                space_product=space_product, domain_id=request.space_product_domain_id
            )
            return GetSpaceProductDomainByIdResponse(
                space_product_domain=space_product_domain, response_meta=meta
            )

    def GetDomainsByCollarCode(self, request, context):
        validation_done, validation_message = (
            AccessSpaceProductConsumer.validate_space_product_services(
                access_auth_details=request.access_auth
            )
        )
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetDomainsByCollarCodeResponse(response_meta=meta)
        else:
            space_product = request.access_auth.space_product
            product_space = ProductSpace(
                space_product_id=space_product.space_product_id
            )
            space_product_domain = product_space.get_domain_with_id(
                space_product=space_product, domain_id=request.space_product_domain_id
            )
            return GetSpaceProductDomainByIdResponse(
                space_product_domain=space_product_domain, response_meta=meta
            )
