from ethos.elint.services.product.identity.account_assistant.discover_account_assistant_pb2_grpc import \
    DiscoverAccountAssistantServiceServicer
from support.db_service import get_account_assistant


class DiscoverAccountAssistantService(DiscoverAccountAssistantServiceServicer):
    def __init__(self):
        super(DiscoverAccountAssistantService, self).__init__()
        self.session_scope = self.__class__.__name__

    def GetAccountAssistantByAccount(self, request, context):
        print("DiscoverAccountAssistantService:GetAccountAssistantByAccount")
        return get_account_assistant(account=request)
