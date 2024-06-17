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

from ethos.elint.services.product.identity.universe.delete_universe_pb2 import DeleteUniverseRequest
from ethos.elint.services.product.identity.universe.delete_universe_pb2 import DeleteUniverseResponse
import grpc
from support.database.universe_services import delete_universe_service

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


'''
Request params:
---------------

universe_id : str
'''

# TODO: Modify the below logic later to archive the universe instead of deleting.
def delete_universe_impl(request: DeleteUniverseRequest) -> DeleteUniverseResponse:
    logging.info("Starting DeleteUniverse RPC")
    
     # get request params here
    logging.info(
        f"Received universe_id: {request.universe_id}")
    
    try:
        # Delete the universe using the database service
        universe_obj = delete_universe_service(request)
        
        # Create the response
        response = DeleteUniverseResponse(
            universe_id=universe_obj.universe_id,
            universe_name=universe_obj.universe_name,
            universe_created_at=universe_obj.universe_created_at,
            universe_description=universe_obj.universe_description,
            universe_updated_at=universe_obj.universe_updated_at 
        )
        return response
    
    except Exception as e:
        logging.error(f"Error deleting universe: {e}")
        context.abort(grpc.StatusCode.INTERNAL, "Internal server error")
