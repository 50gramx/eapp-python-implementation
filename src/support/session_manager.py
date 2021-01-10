# --------------------------------
# Session Management
# --------------------------------
from google.protobuf.timestamp_pb2 import Timestamp

from ethos.elint.entities.generic_pb2 import PersistentSessionTokenDetails
from ethos.elint.services.product.identity.account.access_account_pb2 import AccountServicesAccessAuthDetails, \
    AccountAccessAuthDetails
from ethos.elint.services.product.identity.account.create_account_pb2 import AccountCreationAuthDetails
from support.db_service import get_account
from support.helper_functions import gen_uuid, get_current_timestamp, get_future_timestamp
from support.redis_service import rpush, lindex, lpop


def gen_session_meta(session_validity_in_seconds: int, session_validity_in_minutes: int = 0):
    session_token = gen_uuid()
    requested_at = get_current_timestamp()
    valid_till = get_future_timestamp(after_seconds=session_validity_in_seconds,
                                      after_minutes=session_validity_in_minutes)
    return [session_token, requested_at, valid_till]


def store_session_details_in_redis_list(session_token, session_scope, account_identifier, requested_at, valid_till):
    rpush(session_token, session_scope)
    rpush(session_token, account_identifier)
    rpush(session_token, requested_at)
    rpush(session_token, valid_till)


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
    rpush(session_token, str(last_requested_at.seconds))
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


def create_account_service_access_auth_details(account_id: str, session_scope: str):
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
        account_access_session_token_details=persistent_session_token_details,
        requested_at=requested_at
    )
    return account_service_access_auth_details
