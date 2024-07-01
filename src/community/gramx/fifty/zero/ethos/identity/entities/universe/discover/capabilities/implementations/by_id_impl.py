#   /*************************************************************************
#   *
#   * AMIT KUMAR KHETAN CONFIDENTIAL
#   * __________________
#   *
#   *  [2017] - [2024] Amit Kumar Khetan
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

from ethos.elint.entities import universe_pb2
from grpc import StatusCode

from support.database.universe_services import get_universe

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def by_id_impl(request: universe_pb2.Universe, context) -> universe_pb2.Universe:
    try:
        # Fetch the universe from the database
        universe = get_universe(universe_id=request.universe_id)

        if not universe:
            context.abort(StatusCode.NOT_FOUND, "Universe not found")

        return universe

    except Exception as e:
        logging.error(f"Error reading universe: {e}")
        context.abort(StatusCode.INTERNAL, "Internal server error")
