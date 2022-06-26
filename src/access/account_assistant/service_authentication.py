from access.base_access_authentication import BaseAccessAuthentication
from ethos.elint.entities import account_assistant_pb2
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails


class AccessAccountAssistantServicesAuthentication(BaseAccessAuthentication):

    def __init__(self, session_scope: str, account_assistant: account_assistant_pb2.AccountAssistant):
        self.account_assistant = account_assistant
        super(AccessAccountAssistantServicesAuthentication, self).__init__(session_scope=session_scope)

    def create_authentication_details(self) -> AccountAssistantServicesAccessAuthDetails:
        return AccountAssistantServicesAccessAuthDetails(
            account_assistant=self.account_assistant,
            account_assistant_services_access_session_token_details=self._create_persistent_session_token_details(
                account_identifier=self.account_assistant.account_assistant_id
            ),
            requested_at=self.requested_at
        )
