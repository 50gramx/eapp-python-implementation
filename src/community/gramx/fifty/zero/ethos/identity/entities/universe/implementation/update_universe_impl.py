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
import datetime

from ethos.elint.services.product.identity.universe.update_universe_pb2 import UpdateUniverseRequest
from ethos.elint.services.product.identity.universe.update_universe_pb2 import UpdateUniverseResponse
from google.protobuf.timestamp_pb2 import Timestamp
import grpc
from support.helper_functions import  gen_uuid, get_current_timestamp, get_future_timestamp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_universe_impl(request: UpdateUniverseRequest):
    logging.info("Starting UpdateUniverse RPC")
    
     # get request params here
    logging.info(
        f"Received universe_name: {request.universe_name}")
    
    universe = universe.get(request.universe_name)
    
    if not universe:
        context.abort(grpc.StatusCode.NOT_FOUND, "Universe not found")

    # Update the universe details
    updated_at = Timestamp()
    updated_at.FromDatetime(datetime.datetime.utcnow())
    universe.universe_name = request.universe_name
    universe.universe_description = request.universe_description
    universe.universe_updated_at = updated_at

    # Store the updated universe
    universe[request.universe_id] = universe

        # Create the response
    response = UpdateUniverseResponse(
            universe_id=universe.universe_id,
            universe_name=universe.universe_name,
            universe_created_at=universe.universe_created_at,
            universe_description=universe.universe_description,
            universe_updated_at=updated_at
        )
    return response
