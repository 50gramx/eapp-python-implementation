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


from ethos.elint.entities import universe_pb2

from db_session import DbSession
from community.gramx.fifty.zero.ethos.identity.models.base_models import Universe
from support.helper_functions import format_datetime_to_timestamp


def get_universe(with_universe_id: str) -> universe_pb2.Universe:
    with DbSession.session_scope() as session:
        universe = session.query(Universe).filter(
            Universe.universe_id == with_universe_id
        ).first()
        # create the universe obj here wrt proto contract
        universe_obj = universe_pb2.Universe(
            universe_id=universe.universe_id,
            universe_name=universe.universe_name,
            universe_created_at=format_datetime_to_timestamp(universe.universe_created_at),
            universe_description=universe.universe_description,
            universe_updated_at=format_datetime_to_timestamp(universe.universe_updated_at),
        )
    return universe_obj
