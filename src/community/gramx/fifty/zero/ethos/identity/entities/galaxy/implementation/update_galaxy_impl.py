import logging
import grpc

from ethos.elint.services.product.identity.galaxy.update_galaxy_pb2 import UpdateGalaxyRequest
from ethos.elint.services.product.identity.galaxy.update_galaxy_pb2 import UpdateGalaxyResponse
from support.database.galaxy_services import update_galaxy_service

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

'''
Request params:
---------------

galaxy_id : str
galaxy_name : str
universe : Universe
domain : str
galaxy_description : str
'''

def update_galaxy_impl(request: UpdateGalaxyRequest, context) -> UpdateGalaxyResponse:
    logging.info("Starting Update Galaxy RPC")
    
    # Log request parameters
    logging.info(f"Received galaxy_id: {request.galaxy_id}")
    
    try:
        # Call the database service to update the galaxy
        galaxy_obj = update_galaxy_service(request)

        # Create the response
        return UpdateGalaxyResponse(galaxy=galaxy_obj)
    
    except Exception as e:
        logging.error(f"Error updating galaxy: {e}")
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details(f"Internal server error: {e}")
        raise
