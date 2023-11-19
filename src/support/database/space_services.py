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


from ethos.elint.entities import space_pb2
from ethos.elint.entities.space_pb2 import SpaceAccessibilityType, SpaceIsolationType, SpaceEntityType

from db_session import DbSession
from community.gramx.fifty.zero.ethos.identity.models.base_models import Space
from support.database.galaxy_services import get_galaxy
from support.helper_functions import format_datetime_to_timestamp


def add_new_space(space: Space) -> None:
    with DbSession.session_scope() as session:
        session.add(space)
        session.commit()
    return


def get_space(with_space_id: str = None, with_account_id: str = None) -> space_pb2.Space:
    with DbSession.session_scope() as session:
        if with_space_id is not None:
            space = session.query(Space).filter(
                Space.space_id == with_space_id
            ).first()
        else:
            space = session.query(Space).filter(
                Space.space_admin_id == with_account_id
            ).first()
        if space is None:
            return None
        galaxy_id = space.galaxy_id
        space_id = space.space_id
        space_accessibility_type = space.space_accessibility_type
        space_isolation_type = space.space_isolation_type
        space_entity_type = space.space_entity_type
        space_admin_id = space.space_admin_id
        space_created_at = space.space_created_at
    # create the space obj wrt proto contract
    space_obj = space_pb2.Space(
        space_id=space_id,
        galaxy=get_galaxy(with_galaxy_id=galaxy_id),
        space_accessibility_type=SpaceAccessibilityType.Name(int(space_accessibility_type)),
        space_isolation_type=SpaceIsolationType.Name(int(space_isolation_type)),
        space_entity_type=SpaceEntityType.Name(int(space_entity_type)),
        space_admin_id=space_admin_id,
        space_created_at=format_datetime_to_timestamp(space_created_at)
    )
    return space_obj
