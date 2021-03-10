from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account_assistant.connect_account_assistant_pb2_grpc import \
    ConnectAccountAssistantServiceServicer
from models.account_assistant_connection_models import AccountAssistantConnections


class ConnectAccountAssistantService(ConnectAccountAssistantServiceServicer):
    def __init__(self):
        super(ConnectAccountAssistantService, self).__init__()
        self.session_scope = self.__class__.__name__

    def IsAccountConnected(self, request, context):
        print("ConnectAccountAssistantService:IsAccountConnected")
        account_assistant_connections = AccountAssistantConnections(account_assistant_id=request.account_assistant_id)
        account_connected = account_assistant_connections.is_account_connected(
            account_connection_id=request.connected_account.account_connection_id,
            account_id=request.connected_account.account_id
        )
        if account_connected is False:
            return ResponseMeta(meta_done=account_connected, meta_message="Account not connected.")
        else:
            return ResponseMeta(meta_done=account_connected, meta_message="Account connected.")
