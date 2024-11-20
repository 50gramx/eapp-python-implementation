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
import random
import string
from multiprocessing import context

import grpc
from ethos.elint.services.product.identity.universe.create_universe_pb2 import (
    CreateUniverseRequest,
    CreateUniverseResponse,
)

from support.database.universe_services import create_universe_service


def generate_random_name(self):
    return "".join(random.choices(string.ascii_letters, k=10))


"""
Request params:
---------------

universe_name : str
universe_description : str
"""


# TODO: Modify the below logic later to create universe name based on the template.
def create_universe_impl(request: CreateUniverseRequest) -> CreateUniverseResponse:
    logging.info("Starting CreateUniverse RPC")

    # get request params here
    logging.info(f"Received universe_name: {request.universe_name}")

    logging.info(f"Received universe_description: {request.universe_description}")

    try:

        # Call the database service to create the universe
        universe_obj = create_universe_service(request)

        # Create the response
        response = CreateUniverseResponse(
            universe_id=universe_obj.universe_id,
            universe_name=universe_obj.universe_name,
            universe_created_at=universe_obj.universe_created_at,
            universe_description=universe_obj.universe_description,
        )
        return response

    except Exception as e:
        logging.error(f"Error creating universe: {e}")
        context.abort(grpc.StatusCode.INTERNAL, "Internal server error")
