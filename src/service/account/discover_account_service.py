from ethos.elint.entities.account_assistant_pb2 import AccountAssistant
from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account.discover_account_pb2 import GetAccountByIdResponse
from ethos.elint.services.product.identity.account.discover_account_pb2_grpc import DiscoverAccountServiceServicer
from services_caller.account_assistant_service_caller import get_account_assistant_by_account_caller
from services_caller.account_service_caller import validate_account_services_caller
from support.db_service import get_account


class DiscoverAccountService(DiscoverAccountServiceServicer):
    def __init__(self):
        super(DiscoverAccountService, self).__init__()
        self.session_scope = self.__class__.__name__

    def GetAccountById(self, request, context):
        print("DiscoverAccountService:GetAccountById")
        return GetAccountByIdResponse(
            account=get_account(account_id=request.account_id),
            response_meta=ResponseMeta(meta_done=True, meta_message="Get complete.")
        )

    def GetAccountAssistant(self, request, context):
        print("DiscoverAccountService:GetAccountAssistant")
        validation_done, validation_message = validate_account_services_caller(request)
        if validation_done is False:
            return AccountAssistant()
        else:
            return get_account_assistant_by_account_caller(request.account)
