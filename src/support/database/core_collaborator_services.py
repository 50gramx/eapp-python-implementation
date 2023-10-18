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


from ethos.elint.entities import community_pb2
from ethos.elint.entities.community_collaborator_pb2 import CollaboratorName

from db_session import DbSession
from models.base_models import CoreCollaborator


def is_existing_core_collaborator(collaborator_first_name: str, collaborator_last_name: str,
                                  collaborator_community_code: int) -> bool:
    """
    check for the existence of account_mobile_number in account table as a account_mobile_number
    :param collaborator_first_name:
    :param collaborator_last_name:
    :param collaborator_community_code:
    :return:
    """
    with DbSession.session_scope() as session:
        q = session.query(CoreCollaborator.user_name).filter(
            CoreCollaborator.collaborator_first_name == collaborator_first_name,
            CoreCollaborator.collaborator_last_name == collaborator_last_name,
            CoreCollaborator.collaborator_community_code == collaborator_community_code,
        )
        core_developer_exists = session.query(q.exists()).scalar()
        return core_developer_exists


def get_core_collaborator(collaborator_first_name: str, collaborator_last_name: str,
                          collaborator_community_code: int) -> community_pb2.CommunityCollaborator:
    with DbSession.session_scope() as session:
        core_collaborator = session.query(CoreCollaborator).filter(
            CoreCollaborator.collaborator_first_name == collaborator_first_name,
            CoreCollaborator.collaborator_last_name == collaborator_last_name,
            CoreCollaborator.collaborator_community_code == collaborator_community_code,
        ).first()
        collaborator_name = CollaboratorName(
            first_name=core_collaborator.collaborator_first_name,
            last_name=core_collaborator.collaborator_last_name,
        )
        # TODO: update with contact
        core_collaborator_obj = community_pb2.CommunityCollaborator(
            collaborator_name=collaborator_name,
            community_domain_code=core_collaborator.collaborator_community_code,
            is_core_collaborator=True
        )
    return core_collaborator_obj
