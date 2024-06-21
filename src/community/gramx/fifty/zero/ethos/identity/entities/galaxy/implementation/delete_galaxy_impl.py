import logging
import grpc

from ethos.elint.services.product.identity.galaxy.create_galaxy_pb2 import CreateGalaxyRequest
from ethos.elint.services.product.identity.galaxy.create_galaxy_pb2 import CreateGalaxyResponse
from support.database.galaxy_services import create_galaxy_service

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_galaxy_impl(request: CreateGalaxyRequest, context) -> CreateGalaxyResponse:
    logging.info("Starting Create Galaxy RPC")
    
    # Log request parameters
    logging.info(f"Received galaxy_name: {request.galaxy_name}")
    logging.info(f"Received galaxy_description: {request.galaxy_description}")
    
    try:
        # Call the database service to create the galaxy
        galaxy_obj = create_galaxy_service(request)

        # Create the response
        return CreateGalaxyResponse(galaxy=galaxy_obj)
    
    except Exception as e:
        logging.error(f"Error creating galaxy: {e}")
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details(f"Internal server error: {e}")
        raise
