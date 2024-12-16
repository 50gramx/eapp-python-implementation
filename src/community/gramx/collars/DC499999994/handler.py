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

from ethos.elint.collars.DC499999994_caps_pb2_grpc import (
    add_DC499999994EPME5000CapabilitiesServicer_to_server,
)

from application_context import ApplicationContext


def handle_DC499999994_services(server, aio: bool):
    if aio:
        pass
    else:
        add_DC499999994EPME5000CapabilitiesServicer_to_server(
            ApplicationContext.get_dc499999994_epme5000_capabilities(), server
        )
        logging.info(f"\t [x] added EPME5000 capabilities")
        logging.info(f"DC499999994 services added")
    return server
