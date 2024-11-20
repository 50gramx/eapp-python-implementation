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

from ethos.elint.services.product.service.space_service.access_space_service_pb2_grpc import (
    add_AccessSpaceServiceServiceServicer_to_server,
)
from ethos.elint.services.product.service.space_service.create_space_service_pb2_grpc import (
    add_CreateSpaceServiceServiceServicer_to_server,
)
from ethos.elint.services.product.service.space_service.discover_space_service_pb2_grpc import (
    add_DiscoverSpaceServiceServiceServicer_to_server,
)

from application_context import ApplicationContext


def handle_space_service_services(server, aio: bool):
    if aio:
        pass
    else:
        add_AccessSpaceServiceServiceServicer_to_server(
            ApplicationContext.get_access_space_service_service(), server
        )
        logging.info(f"\t\t [x] access")
        add_CreateSpaceServiceServiceServicer_to_server(
            ApplicationContext.get_create_space_service_service(), server
        )
        logging.info(f"\t\t [x] create")
        add_DiscoverSpaceServiceServiceServicer_to_server(
            ApplicationContext.get_discover_space_service_service(), server
        )
        logging.info(f"\t\t [x] discover")
