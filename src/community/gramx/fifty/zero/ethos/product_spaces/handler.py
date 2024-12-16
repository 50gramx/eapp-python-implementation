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

from src.community.gramx.fifty.zero.ethos.product_spaces.entities.space_product.handler import (
    handle_space_product_services,
)
from src.community.gramx.fifty.zero.ethos.product_spaces.entities.space_product_domain.handler import (
    handle_space_product_domain_services,
)


def handle_product_spaces_services(server, aio: bool):
    handle_space_product_services(server, aio)
    logging.info(f"\t [x] added space product services")
    handle_space_product_domain_services(server, aio)
    logging.info(f"\t [x] added space product domain services")
    logging.info(f"Product Spaces services added")
