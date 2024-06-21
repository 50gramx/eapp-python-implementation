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

from ethos.elint.services.product.identity.galaxy.create_galaxy_pb2_grpc import add_CreateGalaxyServiceServicer_to_server
from ethos.elint.services.product.identity.galaxy.read_galaxy_pb2_grpc import add_ReadGalaxyServiceServicer_to_server
from ethos.elint.services.product.identity.galaxy.update_galaxy_pb2_grpc import add_UpdateGalaxyServiceServicer_to_server
from ethos.elint.services.product.identity.galaxy.delete_galaxy_pb2_grpc import add_DeleteGalaxyServiceServicer_to_server

from application_context import ApplicationContext


def handle_galaxy_services(server, aio: bool):
    if aio:
        pass
    else:
        add_CreateGalaxyServiceServicer_to_server(
            ApplicationContext.get_create_galaxy_service, server
        )
        logging.info(f'\t\t [x] create galaxy')
        
        add_ReadGalaxyServiceServicer_to_server(
            ApplicationContext.get_read_galaxy_service(), server
        )
        logging.info(f'\t\t [x] read galaxy')
        
        add_UpdateGalaxyServiceServicer_to_server(
            ApplicationContext.get_update_galaxy_service(), server
        )
        logging.info(f'\t\t [x] update galaxy')
        
        add_DeleteGalaxyServiceServicer_to_server(
            ApplicationContext.get_delete_galaxy_service(), server
        )
        logging.info(f'\t\t [x] delete galaxy')
        
    return server
