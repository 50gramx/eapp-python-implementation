import logging
import grpc

from ethos.elint.services.product.identity.galaxy.read_galaxy_pb2 import ReadGalaxyRequest
from ethos.elint.services.product.identity.galaxy.read_galaxy_pb2 import ReadGalaxyResponse
from support.database.galaxy_services import read_galaxy_service

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

'''
Request params:
---------------

galaxy_id : str
'''

def read_galaxy_impl(request: ReadGalaxyRequest, context) -> ReadGalaxyResponse:
    logging.info("Starting Read Galaxy RPC")
    
    # Get request params here
    logging.info(f"Received galaxy_id: {request.galaxy_id}")
    
    try:
        # Call the database service to read the galaxy
        galaxy_obj = read_galaxy_service(request)

        # Create the response
        return ReadGalaxyResponse(galaxy=galaxy_obj)
    
    except Exception as e:
        logging.error(f"Error reading galaxy: {e}")
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details(f"Internal server error: {e}")
        raise
