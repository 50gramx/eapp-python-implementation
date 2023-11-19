import logging

from ethos.elint.entities.generic_pb2 import PersistentSessionTokenDetails

from support.helper_functions import format_timestamp_to_iso_string, gen_uuid, get_current_timestamp, \
    get_future_timestamp
from support.session.redis_service import rpush

GENERAL_SESSION_VALIDITY_IN_SECONDS = 0
GENERAL_SESSION_VALIDITY_IN_MINUTES = 30


class BaseAccessAuthentication:
    def __init__(self, session_scope: str, validity_in_seconds: int = GENERAL_SESSION_VALIDITY_IN_SECONDS,
                 validity_in_minutes: int = GENERAL_SESSION_VALIDITY_IN_MINUTES):
        self.session_token = gen_uuid()
        self.requested_at = get_current_timestamp()
        self.valid_till = get_future_timestamp(after_seconds=validity_in_seconds,
                                               after_minutes=validity_in_minutes)
        self.session_scope = session_scope

        logging.info(f"BaseAccessAuthentication initialized with session_token: {self.session_token}, "
                     f"session_scope: {self.session_scope}, requested_at: {self.requested_at}, "
                     f"valid_till: {self.valid_till}")

    def _store_session_details_in_redis_list(self, account_identifier: str):
        rpush(self.session_token, self.session_scope)
        rpush(self.session_token, account_identifier)
        rpush(self.session_token, format_timestamp_to_iso_string(self.requested_at))
        rpush(self.session_token, format_timestamp_to_iso_string(self.valid_till))

        logging.info(f"Session details stored in Redis for session_token: {self.session_token}")

    def _get_persistent_session_token(self):
        return PersistentSessionTokenDetails(
            session_token=self.session_token,
            session_scope=self.session_scope,
            generated_at=self.requested_at,
            valid_till=self.valid_till
        )

    def _create_persistent_session_token_details(self, account_identifier: str):
        self._store_session_details_in_redis_list(account_identifier=account_identifier)
        persistent_session_token = self._get_persistent_session_token()
        logging.info(f"Persistent session token details created: {persistent_session_token}")
        return persistent_session_token
