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
from community.gramx.fifty.zero.ethos.product_spaces.entities.space_product.access.capabilities.access_space_product_service import (
    AccessSpaceProductService,
)
from community.gramx.fifty.zero.ethos.product_spaces.entities.space_product.create.capabilities.create_space_product_service import (
    CreateSpaceProductService,
)
from community.gramx.fifty.zero.ethos.product_spaces.entities.space_product.discover.capabilities.discover_space_product_service import (
    DiscoverSpaceProductService,
)
from support.application.registry import Registry


def register_space_product_services(aio: bool):
    if aio:
        pass
    else:
        create_space_product_service = CreateSpaceProductService()
        Registry.register_service(
            "create_space_product_service", create_space_product_service
        )
        access_space_product_service = AccessSpaceProductService()
        Registry.register_service(
            "access_space_product_service", access_space_product_service
        )
        discover_space_product_service = DiscoverSpaceProductService()
        Registry.register_service(
            "discover_space_product_service", discover_space_product_service
        )
