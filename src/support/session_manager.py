# --------------------------------
# Session Management
# --------------------------------
from google.protobuf.timestamp_pb2 import Timestamp

from ethos.elint.entities import account_assistant_pb2, space_pb2
from ethos.elint.entities.generic_pb2 import PersistentSessionTokenDetails
from ethos.elint.services.product.identity.account.access_account_pb2 import AccountServicesAccessAuthDetails, \
    AccountAccessAuthDetails
from ethos.elint.services.product.identity.account.create_account_pb2 import AccountCreationAuthDetails
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails
from ethos.elint.services.product.identity.space.access_space_pb2 import SpaceServicesAccessAuthDetails
from support.db_service import get_account
from support.helper_functions import gen_uuid, get_current_timestamp, get_future_timestamp, \
    format_timestamp_to_iso_string, format_iso_string_to_timestamp
from support.redis_service import rpush, lindex, lpop


def get_new_service_session(session_scope: str, account_identifier: str) -> []:
    session_token = gen_uuid()
    requested_at = get_current_timestamp()
    valid_till = get_future_timestamp(after_seconds=0,
                                      after_minutes=4320)
    store_session_details_in_redis_list(session_token=session_token, session_scope=session_scope,
                                        account_identifier=account_identifier, requested_at=requested_at,
                                        valid_till=valid_till)
    return [session_token, requested_at, valid_till]


def gen_session_meta(session_validity_in_seconds: int, session_validity_in_minutes: int = 0):
    session_token = gen_uuid()
    requested_at = get_current_timestamp()
    valid_till = get_future_timestamp(after_seconds=session_validity_in_seconds,
                                      after_minutes=session_validity_in_minutes)
    return [session_token, requested_at, valid_till]


def store_session_details_in_redis_list(session_token, session_scope, account_identifier, requested_at, valid_till):
    rpush(session_token, session_scope)
    rpush(session_token, account_identifier)
    rpush(session_token, format_timestamp_to_iso_string(requested_at))
    rpush(session_token, format_timestamp_to_iso_string(valid_till))


def is_persistent_session_valid(session_token, account_identifier, session_scope) -> (bool, str):
    # validate requesting account
    if lindex(session_token, 1) == account_identifier:
        # validate the token validity
        if format_iso_string_to_timestamp(lindex(session_token, 3)).seconds > get_current_timestamp().seconds:
            # validate the session scope
            if True:  # lindex(session_token, 0) == session_scope:
                return True, "Session is valid."
            # else:
            #   return False, f"Session scope: {session_scope} not authorized. This action will be reported."
        else:
            return False, "Session has expired. Retrieve a new session."
    else:
        return False, "Unauthorized validation request. This action will be reported."


def create_account_creation_auth_details(account_mobile_number: str, session_scope: str):
    # Message Parameters
    session_token, requested_at, valid_till = gen_session_meta(session_validity_in_seconds=600)
    # Add the session meta to redis
    store_session_details_in_redis_list(session_token=session_token, session_scope=session_scope,
                                        account_identifier=account_mobile_number, requested_at=requested_at,
                                        valid_till=valid_till)
    # Build Messages
    persistent_session_token_details = PersistentSessionTokenDetails(
        session_token=session_token,
        session_scope=session_scope,
        generated_at=requested_at,
        valid_till=valid_till
    )
    account_creation_auth_details = AccountCreationAuthDetails(
        account_mobile_number=account_mobile_number,
        account_creation_session_token_details=persistent_session_token_details,
        requested_at=requested_at
    )
    return account_creation_auth_details


def update_persistent_session_last_requested_at(session_token: str, last_requested_at: Timestamp):
    if lindex(session_token, 4) is not None:
        lpop(session_token)
    rpush(session_token, format_timestamp_to_iso_string(last_requested_at))
    return


def create_account_access_auth_details(account_mobile_number: str, session_scope: str):
    # Message Parameters
    session_token, requested_at, valid_till = gen_session_meta(session_validity_in_seconds=600)
    # Add the session meta to redis
    store_session_details_in_redis_list(session_token=session_token, session_scope=session_scope,
                                        account_identifier=account_mobile_number, requested_at=requested_at,
                                        valid_till=valid_till)
    # Build Messages
    persistent_session_token_details = PersistentSessionTokenDetails(
        session_token=session_token,
        session_scope=session_scope,
        generated_at=requested_at,
        valid_till=valid_till
    )
    account_access_auth_details = AccountAccessAuthDetails(
        account_mobile_number=account_mobile_number,
        account_access_auth_session_token_details=persistent_session_token_details
    )
    return account_access_auth_details


def create_account_services_access_auth_details(account_id: str, session_scope: str):
    # Message Parameters
    session_token, requested_at, valid_till = gen_session_meta(session_validity_in_seconds=0,
                                                               session_validity_in_minutes=30)
    account = get_account(account_id=account_id)
    # Add the session meta to redis
    store_session_details_in_redis_list(session_token=session_token, session_scope=session_scope,
                                        account_identifier=account_id, requested_at=requested_at,
                                        valid_till=valid_till)
    # create the account_service_access_auth_details_here
    persistent_session_token_details = PersistentSessionTokenDetails(
        session_token=session_token,
        session_scope=session_scope,
        generated_at=requested_at,
        valid_till=valid_till
    )
    account_service_access_auth_details = AccountServicesAccessAuthDetails(
        account=account,
        account_services_access_session_token_details=persistent_session_token_details,
        requested_at=requested_at
    )
    return account_service_access_auth_details


def create_space_services_access_auth_details(
        session_scope: str,
        space: space_pb2.Space
) -> SpaceServicesAccessAuthDetails:
    session_token, requested_at, valid_till = get_new_service_session(
        session_scope, space.space_id)
    return SpaceServicesAccessAuthDetails(
        space=space,
        space_services_access_session_token_details=PersistentSessionTokenDetails(
            session_token=session_token, session_scope=session_scope, generated_at=requested_at, valid_till=valid_till),
        requested_at=requested_at
    )


def create_account_assistant_services_access_auth_details(
        session_scope: str,
        account_assistant: account_assistant_pb2.AccountAssistant
) -> AccountAssistantServicesAccessAuthDetails:
    session_token, requested_at, valid_till = get_new_service_session(
        session_scope, account_assistant.account_assistant_id)
    return AccountAssistantServicesAccessAuthDetails(
        account_assistant=account_assistant,
        account_assistant_services_access_session_token_details=PersistentSessionTokenDetails(
            session_token=session_token, session_scope=session_scope, generated_at=requested_at, valid_till=valid_till),
        requested_at=requested_at
    )
