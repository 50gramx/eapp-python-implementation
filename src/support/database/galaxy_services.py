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


from ethos.elint.entities import galaxy_pb2

from db_session import DbSession
from community.gramx.fifty.zero.ethos.identity.models.base_models import Galaxy
from support.database.universe_services import get_universe
from support.helper_functions import format_datetime_to_timestamp


def get_galaxy(with_galaxy_id: str) -> galaxy_pb2.Galaxy:
    with DbSession.session_scope() as session:
        galaxy = session.query(Galaxy).filter(
            Galaxy.galaxy_id == with_galaxy_id
        ).first()
        galaxy_id = galaxy.galaxy_id
        galaxy_name = galaxy.galaxy_name
        galaxy_created_at = galaxy.galaxy_created_at
        universe_id = galaxy.universe_id
    # create the galaxy obj here wrt proto contract
    universe = get_universe(with_universe_id=universe_id)
    galaxy_obj = galaxy_pb2.Galaxy(
        galaxy_id=galaxy_id,
        galaxy_name=galaxy_name,
        universe=universe,
        galaxy_created_at=format_datetime_to_timestamp(galaxy_created_at)
    )
    return galaxy_obj


def get_our_galaxy() -> galaxy_pb2.Galaxy:
    with DbSession.session_scope() as session:
        galaxy = session.query(Galaxy).filter(
            Galaxy.galaxy_name == "Open Galaxy"
        ).first()
        galaxy_id = galaxy.galaxy_id
        galaxy_name = galaxy.galaxy_name
        galaxy_created_at = galaxy.galaxy_created_at
        universe_id = galaxy.universe_id
    # create the galaxy obj here wrt proto contract
    universe = get_universe(with_universe_id=universe_id)
    galaxy_obj = galaxy_pb2.Galaxy(
        galaxy_id=galaxy_id,
        galaxy_name=galaxy_name,
        universe=universe,
        galaxy_created_at=format_datetime_to_timestamp(galaxy_created_at)
    )
    return galaxy_obj
