from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account.connect_account_pb2 import ConnectedAccountAssistants, \
    ConnectedAccounts
from ethos.elint.services.product.identity.account.connect_account_pb2_grpc import ConnectAccountServiceServicer
from models.account_connection_models import AccountConnections
from services_caller.account_service_caller import validate_account_services_caller


class ConnectAccountService(ConnectAccountServiceServicer):
    def __init__(self):
        super(ConnectAccountService, self).__init__()
        self.session_scope = self.__class__.__name__

    def GetAllConnectedAccountAssistants(self, request, context):
        print("ConnectAccountService:GetAllConnectedAccountAssistants")
        access_done, access_message = validate_account_services_caller(request)
        meta = ResponseMeta(meta_done=access_done, meta_message=access_message)
        if access_done is False:
            return ConnectedAccountAssistants(response_meta=meta)
        else:
            account_connections = AccountConnections(account_id=request.account.account_id)
            list_of_connected_account_assistants = account_connections.get_connected_account_assistants()
            return ConnectedAccountAssistants(
                connected_account_assistants=list_of_connected_account_assistants, response_meta=meta)

    def IsAccountAssistantConnected(self, request, context):
        print("ConnectAccountService:IsAccountAssistantConnected")
        account_connections = AccountConnections(account_id=request.account_id)
        account_assistant_connected = account_connections.is_account_assistant_connected(
            account_assistant_connection_id=request.connected_account_assistant.account_assistant_connection_id,
            account_assistant_id=request.connected_account_assistant.account_assistant_id
        )
        if account_assistant_connected is False:
            return ResponseMeta(meta_done=account_assistant_connected, meta_message="Account Assistant not connected.")
        else:
            return ResponseMeta(meta_done=account_assistant_connected, meta_message="Account Assistant connected.")

    def GetAllConnectedAccounts(self, request, context):
        print("ConnectAccountService:GetAllConnectedAccounts")
        access_done, access_message = validate_account_services_caller(request)
        if access_done is False:
            return ConnectedAccounts(
                response_meta=ResponseMeta(meta_done=access_done, meta_message=access_message))
        else:
            account_connections = AccountConnections(account_id=request.account.account_id)
            list_of_connected_accounts = account_connections.get_connected_accounts()
            return ConnectedAccounts(
                connected_accounts=list_of_connected_accounts,
                response_meta=ResponseMeta(meta_done=access_done, meta_message=access_message))
