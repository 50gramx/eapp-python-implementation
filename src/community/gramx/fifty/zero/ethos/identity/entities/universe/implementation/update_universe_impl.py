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
from multiprocessing import context

import grpc
from ethos.elint.services.product.identity.universe.update_universe_pb2 import (
    UpdateUniverseRequest,
    UpdateUniverseResponse,
)

from support.database.universe_services import update_universe_service

"""
Request params:
---------------

universe_id : str
"""


def update_universe_impl(request: UpdateUniverseRequest) -> UpdateUniverseResponse:
    logging.info("Starting UpdateUniverse RPC")

    # Get request parameters
    logging.info(f"Received universe_id: {request.universe_id}")

    try:
        # Update the universe using the database service
        universe_obj = update_universe_service(request)

        # Create the response
        response = UpdateUniverseResponse(
            universe_id=universe_obj.universe_id,
            universe_name=universe_obj.universe_name,
            universe_created_at=universe_obj.universe_created_at,
            universe_description=universe_obj.universe_description,
            universe_updated_at=universe_obj.universe_updated_at,  # Ensure to include the updated_at field
        )
        return response

    except Exception as e:
        logging.error(f"Error updating universe: {e}")
        context.abort(grpc.StatusCode.INTERNAL, "Internal server error")
