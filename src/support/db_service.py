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
from ethos.elint.entities import space_knowledge_pb2
from ethos.elint.entities import space_pb2

from community.gramx.fifty.zero.ethos.knowledge_spaces.models.base_models import SpaceKnowledge
from db_session import DbSession
from support.helper_functions import format_datetime_to_timestamp


def add_new_entity(entity) -> None:
    """
    Adds a new record in the database table of specified entity
    :param entity: an entity of Base Class (base_models.py)
    :return: None
    """
    with DbSession.session_scope() as session:
        session.add(entity)
        session.commit()
    return


def get_space_knowledge(space: space_pb2.Space, with_space_knowledge_id: str = None,
                        with_space_id: str = None) -> space_knowledge_pb2.SpaceKnowledge:
    with DbSession.session_scope() as session:
        if with_space_knowledge_id is not None:
            space_knowledge = session.query(SpaceKnowledge).filter(
                SpaceKnowledge.space_knowledge_id == with_space_knowledge_id
            ).first()
        else:
            space_knowledge = session.query(SpaceKnowledge).filter(
                SpaceKnowledge.space_id == with_space_id
            ).first()
        if space_knowledge is None:
            return None
        else:
            # create the space_knowledge obj wrt proto contract
            space_knowledge_obj = space_knowledge_pb2.SpaceKnowledge(
                space=space,
                space_knowledge_id=space_knowledge.space_knowledge_id,
                space_knowledge_admin_account_id=space_knowledge.space_knowledge_admin_account_id,
                space_knowledge_name=space_knowledge.space_knowledge_name,
                created_at=format_datetime_to_timestamp(space_knowledge.created_at)
            )
            return space_knowledge_obj
