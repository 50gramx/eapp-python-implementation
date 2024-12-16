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
from ethos.elint.services.product.product.space_product_domain.create_space_product_domain_pb2_grpc import (
    CreateSpaceProductDomainServiceServicer,
)

from src.community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.create.consumers.create_space_knowledge_domain_consumer import (
    CreateSpaceKnowledgeDomainConsumer,
)
from src.community.gramx.fifty.zero.ethos.product_spaces.entities.space_product.access.consumers.access_space_product_consumer import (
    AccessSpaceProductConsumer,
)
from src.community.gramx.fifty.zero.ethos.product_spaces.entities.space_product.discover.consumers.discover_space_product_consumer import (
    DiscoverSpaceProductConsumer,
)
from src.community.gramx.fifty.zero.ethos.product_spaces.entities.space_product_domain.access.consumers.access_space_product_domain_consumer import (
    AccessSpaceProductDomainConsumer,
)
from src.community.gramx.fifty.zero.ethos.product_spaces.models.product_space_models import (
    ProductSpace,
)


class CreateSpaceProductDomainService(CreateSpaceProductDomainServiceServicer):
    def __init__(self):
        super(CreateSpaceProductDomainService, self).__init__()
        self.session_scope = self.__class__.__name__

    def CreateDC499999994(self, request, context):
        logging.info("CreateSpaceProductDomainService:CreateDC499999994.")
        is_valid, valid_message = (
            AccessSpaceProductConsumer.validate_space_product_services(
                access_auth_details=request.auth
            )
        )
        meta = ResponseMeta(meta_done=is_valid, meta_message=valid_message)
        if is_valid is False:
            return meta
        else:
            # generic validation stuff
            # TODO: pay for the service

            space_product = request.auth.space_product
            product_space = ProductSpace(
                space_product_id=space_product.space_product_id
            )
            
            collar_code = "DC499999994"
            domain_id = product_space.add_new_domain(
                domain_name=request.name,
                domain_description=request.description,
                domain_collar_code=collar_code,
                domain_isolate=request.is_isolated,
            )

            _, _, space_product_domain = (
                DiscoverSpaceProductConsumer.get_space_product_domain_by_id(
                    request.auth,
                    domain_id,
                )
            )
            domain_access_auth_details, _, _ = (
                AccessSpaceProductDomainConsumer.space_product_domain_access_token(
                    request.auth,
                    space_product_domain,
                )
            )

            skincare_product = request.dc499999994.skincare_product
            # TODO: add dc499999994 create request and service call

            return meta
