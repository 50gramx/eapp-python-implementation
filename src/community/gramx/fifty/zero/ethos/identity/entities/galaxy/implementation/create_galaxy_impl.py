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
import grpc

from ethos.elint.services.product.identity.galaxy.create_galaxy_pb2 import CreateGalaxyRequest
from ethos.elint.services.product.identity.galaxy.create_galaxy_pb2 import CreateGalaxyResponse
from support.database.galaxy_services import create_galaxy_service

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


'''
Request params:
---------------

galaxy_name : str
galaxy_description : str
'''

def create_galaxy_impl(request: CreateGalaxyRequest, context) -> CreateGalaxyResponse:
    logging.info("Starting Create Galaxy RPC")
    
    # Log request parameters
    logging.info(f"Received galaxy_name: {request.galaxy_name}")
    logging.info(f"Received galaxy_description: {request.galaxy_description}")
    
    try:
        # Call the database service to create the galaxy
        galaxy_obj = create_galaxy_service(request)

        # Create the response
        response = CreateGalaxyResponse(galaxy=galaxy_obj)
        return response
    
    except Exception as e:
        logging.error(f"Error creating galaxy: {e}")
        context.abort(grpc.StatusCode.INTERNAL, "Internal server error")
