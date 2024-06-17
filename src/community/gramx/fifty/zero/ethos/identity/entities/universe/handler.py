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

from ethos.elint.services.product.identity.universe.create_universe_pb2_grpc import add_CreateUniverseServiceServicer_to_server
from ethos.elint.services.product.identity.universe.read_universe_pb2_grpc import add_ReadUniverseServiceServicer_to_server
from ethos.elint.services.product.identity.universe.update_universe_pb2_grpc import add_UpdateUniverseServiceServicer_to_server
from ethos.elint.services.product.identity.universe.delete_universe_pb2_grpc import add_DeleteUniverseServiceServicer_to_server

from application_context import ApplicationContext


def handle_universe_services(server, aio: bool):
    if aio:
        pass
    else:
        add_CreateUniverseServiceServicer_to_server(
            ApplicationContext.get_create_universe_service, server
        )
        logging.info(f'\t\t [x] create universe')
        
        add_ReadUniverseServiceServicer_to_server(
            ApplicationContext.get_read_universe_service(), server
        )
        logging.info(f'\t\t [x] read universe')
        
        add_UpdateUniverseServiceServicer_to_server(
            ApplicationContext.get_update_universe_service(), server
        )
        logging.info(f'\t\t [x] update universe')
        
        add_DeleteUniverseServiceServicer_to_server(
            ApplicationContext.get_delete_universe_service(), server
        )
        logging.info(f'\t\t [x] delete universe')
        
    return server
