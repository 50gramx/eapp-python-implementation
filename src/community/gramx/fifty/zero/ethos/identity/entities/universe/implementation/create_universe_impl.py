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
import uuid
import datetime
import random
import string

from ethos.elint.services.product.identity.universe.create_universe_pb2 import CreateUniverseRequest
from ethos.elint.services.product.identity.universe.create_universe_pb2 import CreateUniverseResponse
from google.protobuf.timestamp_pb2 import Timestamp
from support.helper_functions import  gen_uuid, get_current_timestamp, get_future_timestamp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def generate_random_name(self):
        return ''.join(random.choices(string.ascii_letters, k=10))

def create_universe_impl(request: CreateUniverseRequest) -> CreateUniverseResponse:
    logging.info("Starting CreateUniverse RPC")
    
    # get request params here
    logging.info(
        f"Received universe_description: {request.universe_description}")
    
    universe_id = str(uuid.uuid4())
    created_at = Timestamp()
    created_at.FromDatetime(datetime.datetime.utcnow())
    universe_name = generate_random_name()

    # Create the response
    response = CreateUniverseResponse(
            universe_id=universe_id,
            universe_name=universe_name,
            universe_created_at=created_at,
            universe_description=request.universe_description
        )
    return response

