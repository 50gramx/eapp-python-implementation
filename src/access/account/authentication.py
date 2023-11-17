import logging

from ethos.elint.services.product.identity.account.access_account_pb2 import AccountAccessAuthDetails
from ethos.elint.services.product.identity.account.create_account_pb2 import AccountCreationAuthDetails

from access.base_access_authentication import BaseAccessAuthentication


class AccessAccountAuthentication(BaseAccessAuthentication):

    def __init__(self, session_scope: str, account_mobile_country_code: str, account_mobile_number: str):
        logging.info("Initializing AccessAccountAuthentication instance.")
        self.account_mobile_country_code = account_mobile_country_code
        self.account_mobile_number = account_mobile_number
        super(AccessAccountAuthentication, self).__init__(session_scope=session_scope, validity_in_minutes=10)

    def create_authentication_details(self):
        logging.info("Creating authentication details for account access.")
        return AccountAccessAuthDetails(
            account_mobile_number=self.account_mobile_number,
            account_access_auth_session_token_details=self._create_persistent_session_token_details(
                account_identifier=self.account_mobile_number
            )
        )

    def create_creation_authentication_details(self):
        logging.info("Creating authentication details for account creation.")
        return AccountCreationAuthDetails(
            account_mobile_country_code=self.account_mobile_country_code,
            account_mobile_number=self.account_mobile_number,
            account_creation_session_token_details=self._create_persistent_session_token_details(
                account_identifier=self.account_mobile_number
            ),
            requested_at=self.requested_at
        )
