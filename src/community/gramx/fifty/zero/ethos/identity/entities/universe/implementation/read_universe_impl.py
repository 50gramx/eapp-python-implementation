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
from support.database.universe_services import get_universe_service

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_universe_impl(request: ReadUniverseRequest) -> ReadUniverseResponse:
    logging.info("Starting ReadUniverse RPC")
    
    # get request params here
    logging.info(
        f"Received universe_id: {request.universe_id}")
    
    try:
        # Fetch the universe from the database
        universe = get_universe_service(request.universe_id)
        
        if not universe:
            context.abort(grpc.StatusCode.NOT_FOUND, "Universe not found")
        
        # Create the response
        response = ReadUniverseResponse(
            universe_id=universe.universe_id,
            universe_name=universe.universe_name,
            universe_created_at=universe.universe_created_at,
            universe_description=universe.universe_description,
            universe_updated_at=universe.universe_updated_at
        )
        return response
    
    except Exception as e:
        logging.error(f"Error reading universe: {e}")
        context.abort(grpc.StatusCode.INTERNAL, "Internal server error")


 

