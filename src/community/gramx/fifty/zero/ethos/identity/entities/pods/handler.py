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


from ethos.elint.services.product.identity.pods.create_pods_pb2_grpc import add_CreatePodsServiceServicer_to_server


from application_context import ApplicationContext


def handle_pods_services(server, aio: bool):
    if aio:
        pass
    else:
        add_CreatePodsServiceServicer_to_server(
            ApplicationContext.get_create_pods_service
        )
        logging.info(f'\t\t [x] create pods')
    return server