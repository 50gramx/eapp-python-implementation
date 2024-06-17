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

from ethos.elint.services.product.identity.universe.read_universe_pb2 import ReadUniverseRequest
from ethos.elint.services.product.identity.universe.read_universe_pb2 import ReadUniverseResponse
from google.protobuf.timestamp_pb2 import Timestamp
import grpc
from support.helper_functions import  gen_uuid, get_current_timestamp, get_future_timestamp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_universe_impl(request: ReadUniverseRequest) -> ReadUniverseResponse:
    logging.info("Starting ReadUniverse RPC")
    
    # get request params here
    logging.info(
        f"Received universe_name: {request.universe_name}")
    
    universe = universe.get(request.universe_name)
    
    if not universe:
        context.abort(grpc.StatusCode.NOT_FOUND, "Universe not found")


    # Create the response
    response = ReadUniverseResponse(
            universe_id=universe.universe_id,
            universe_name=universe.universe_name,
            universe_created_at=universe.created_at,
            universe_description=request.universe.universe_description
        )
    return response

