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

from ethos.elint.services.product.identity.universe.delete_universe_pb2 import DeleteUniverseRequest
from ethos.elint.services.product.identity.universe.delete_universe_pb2 import DeleteUniverseResponse
from google.protobuf.timestamp_pb2 import Timestamp
import grpc
from support.helper_functions import  gen_uuid, get_current_timestamp, get_future_timestamp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def delete_universe_impl(request: DeleteUniverseResponse) -> DeleteUniverseResponse:
    logging.info("Starting DeleteUniverse RPC")
    
     # get request params here
    logging.info(
        f"Received universe_name: {request.universe_name}")
    
    universe = universe.pop(request.universe_name, None)
    if not universe:
        context.abort(grpc.StatusCode.NOT_FOUND, "Universe not found")

        # Create the response
    response = DeleteUniverseResponse(
        universe_id=universe.universe_id,
        universe_name=universe.universe_name,
        universe_created_at=universe.universe_created_at,
        universe_description=universe.universe_description,
        universe_updated_at=universe.universe_updated_at
        )
    return response
