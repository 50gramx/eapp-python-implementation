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

from ethos.elint.entities import (
    space_knowledge_domain_file_page_pb2,
    space_knowledge_domain_file_pb2,
    space_knowledge_domain_pb2,
    space_knowledge_pb2,
    space_service_domain_pb2,
    space_service_pb2,
)
from ethos.elint.entities.generic_pb2 import PersistentSessionTokenDetails
from ethos.elint.services.product.knowledge.space_knowledge.access_space_knowledge_pb2 import (
    SpaceKnowledgeServicesAccessAuthDetails,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2 import (
    SpaceKnowledgeDomainServicesAccessAuthDetails,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file.access_space_knowledge_domain_file_pb2 import (
    SpaceKnowledgeDomainFileServicesAccessAuthDetails,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.access_space_knowledge_domain_file_page_pb2 import (
    SpaceKnowledgeDomainFilePageServicesAccessAuthDetails,
)
from ethos.elint.services.product.service.space_service.access_space_service_pb2 import (
    SpaceServiceServicesAccessAuthDetails,
)
from ethos.elint.services.product.service.space_service_domain.access_space_service_domain_pb2 import (
    SpaceServiceDomainServicesAccessAuthDetails,
)
from google.protobuf.timestamp_pb2 import Timestamp

from support.helper_functions import (
    format_iso_string_to_timestamp,
    format_timestamp_to_iso_string,
    gen_uuid,
    get_current_timestamp,
    get_future_timestamp,
)
from support.session.redis_service import lindex, lpop, rpush

# --------------------------------
# Session Management
# --------------------------------


def get_new_service_session(session_scope: str, session_identifier: str) -> []:
    session_token = gen_uuid()
    requested_at = get_current_timestamp()
    valid_till = get_future_timestamp(after_seconds=0, after_minutes=4320)
    store_session_details_in_redis_list(
        session_token=session_token,
        session_scope=session_scope,
        session_identifier=session_identifier,
        requested_at=requested_at,
        valid_till=valid_till,
    )
    return [session_token, requested_at, valid_till]


def gen_session_meta(
    session_validity_in_seconds: int, session_validity_in_minutes: int = 0
):
    session_token = gen_uuid()
    requested_at = get_current_timestamp()
    valid_till = get_future_timestamp(
        after_seconds=session_validity_in_seconds,
        after_minutes=session_validity_in_minutes,
    )
    return [session_token, requested_at, valid_till]


def store_session_details_in_redis_list(
    session_token, session_scope, session_identifier, requested_at, valid_till
):
    rpush(session_token, session_scope)
    rpush(session_token, session_identifier)
    rpush(session_token, format_timestamp_to_iso_string(requested_at))
    rpush(session_token, format_timestamp_to_iso_string(valid_till))


def is_persistent_session_valid(
    session_token, session_identifier, session_scope
) -> (bool, str):
    # validate requesting account
    if lindex(session_token, 1) == session_identifier:
        # validate the token validity
        if (
            format_iso_string_to_timestamp(lindex(session_token, 3)).seconds
            > get_current_timestamp().seconds
        ):
            # validate the session scope
            if True:  # lindex(session_token, 0) == session_scope:
                return True, "Session is valid."
            # else:
            #   return False, f"Session scope: {session_scope} not authorized. This action will be reported."
        else:
            return False, "Session has expired. Retrieve a new session."
    else:
        return False, "Unauthorized validation request. This action will be reported."


def update_persistent_session_last_requested_at(
    session_token: str, last_requested_at: Timestamp
):
    if lindex(session_token, 4) is not None:
        lpop(session_token)
    rpush(session_token, format_timestamp_to_iso_string(last_requested_at))
    return


# --------------------------------
# Knowledge Session Management
# --------------------------------


def create_space_knowledge_services_access_auth_details(
    session_scope: str, space_knowledge: space_knowledge_pb2.SpaceKnowledge
) -> SpaceKnowledgeServicesAccessAuthDetails:
    session_token, requested_at, valid_till = get_new_service_session(
        session_scope, space_knowledge.space_knowledge_id
    )
    return SpaceKnowledgeServicesAccessAuthDetails(
        space_knowledge=space_knowledge,
        space_knowledge_services_access_session_token_details=PersistentSessionTokenDetails(
            session_token=session_token,
            session_scope=session_scope,
            generated_at=requested_at,
            valid_till=valid_till,
        ),
        requested_at=requested_at,
    )


def create_space_knowledge_domain_services_access_auth_details(
    session_scope: str,
    space_knowledge_domain: space_knowledge_domain_pb2.SpaceKnowledgeDomain,
) -> SpaceKnowledgeDomainServicesAccessAuthDetails:
    session_token, requested_at, valid_till = get_new_service_session(
        session_scope, space_knowledge_domain.space_knowledge_domain_id
    )
    return SpaceKnowledgeDomainServicesAccessAuthDetails(
        space_knowledge_domain=space_knowledge_domain,
        space_knowledge_domain_services_access_session_token_details=PersistentSessionTokenDetails(
            session_token=session_token,
            session_scope=session_scope,
            generated_at=requested_at,
            valid_till=valid_till,
        ),
        requested_at=requested_at,
    )


def create_space_knowledge_domain_file_services_access_auth_details(
    session_scope: str,
    space_knowledge_domain_file: space_knowledge_domain_file_pb2.SpaceKnowledgeDomainFile,
) -> SpaceKnowledgeDomainFileServicesAccessAuthDetails:
    session_token, requested_at, valid_till = get_new_service_session(
        session_scope, space_knowledge_domain_file.space_knowledge_domain_file_id
    )
    return SpaceKnowledgeDomainFileServicesAccessAuthDetails(
        space_knowledge_domain_file=space_knowledge_domain_file,
        space_knowledge_domain_file_services_access_session_token_details=PersistentSessionTokenDetails(
            session_token=session_token,
            session_scope=session_scope,
            generated_at=requested_at,
            valid_till=valid_till,
        ),
        requested_at=requested_at,
    )


def create_space_knowledge_domain_file_page_services_access_auth_details(
    session_scope: str,
    space_knowledge_domain_file_page: space_knowledge_domain_file_page_pb2.SpaceKnowledgeDomainFilePage,
) -> SpaceKnowledgeDomainFilePageServicesAccessAuthDetails:
    session_token, requested_at, valid_till = get_new_service_session(
        session_scope,
        space_knowledge_domain_file_page.space_knowledge_domain_file_page_id,
    )
    return SpaceKnowledgeDomainFilePageServicesAccessAuthDetails(
        space_knowledge_domain_file_page=space_knowledge_domain_file_page,
        space_knowledge_domain_file_page_services_access_session_token_details=PersistentSessionTokenDetails(
            session_token=session_token,
            session_scope=session_scope,
            generated_at=requested_at,
            valid_till=valid_till,
        ),
        requested_at=requested_at,
    )


# --------------------------------
# Service Session Management
# --------------------------------


def create_space_service_services_access_auth_details(
    session_scope: str, space_service: space_service_pb2.SpaceService
) -> SpaceServiceServicesAccessAuthDetails:
    session_token, requested_at, valid_till = get_new_service_session(
        session_scope, space_service.space_service_id
    )
    return SpaceServiceServicesAccessAuthDetails(
        space_service=space_service,
        space_service_services_access_session_token_details=PersistentSessionTokenDetails(
            session_token=session_token,
            session_scope=session_scope,
            generated_at=requested_at,
            valid_till=valid_till,
        ),
        requested_at=requested_at,
    )


def create_space_service_domain_services_access_auth_details(
    session_scope: str,
    space_service_domain: space_service_domain_pb2.SpaceServiceDomain,
) -> SpaceServiceDomainServicesAccessAuthDetails:
    session_token, requested_at, valid_till = get_new_service_session(
        session_scope, space_service_domain.id
    )
    return SpaceServiceDomainServicesAccessAuthDetails(
        space_service_domain=space_service_domain,
        space_service_domain_services_access_session_token_details=PersistentSessionTokenDetails(
            session_token=session_token,
            session_scope=session_scope,
            generated_at=requested_at,
            valid_till=valid_till,
        ),
        requested_at=requested_at,
    )
