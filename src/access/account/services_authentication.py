from access.base_access_authentication import BaseAccessAuthentication
from ethos.elint.services.product.identity.account.access_account_pb2 import AccountServicesAccessAuthDetails
from support.db_service import get_account


class AccessAccountServicesAuthentication(BaseAccessAuthentication):

    def __init__(self, session_scope: str, account_id: str):
        self.account_id = account_id
        super(AccessAccountServicesAuthentication, self).__init__(session_scope=session_scope)

    def create_authentication_details(self) -> AccountServicesAccessAuthDetails:
        return AccountServicesAccessAuthDetails(
            account=get_account(account_id=self.account_id),
            account_services_access_session_token_details=self._create_persistent_session_token_details(
                account_identifier=self.account_id
            ),
            requested_at=self.requested_at
        )
