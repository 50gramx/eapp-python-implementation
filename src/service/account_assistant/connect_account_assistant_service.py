from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account_assistant.connect_account_assistant_pb2 import ConnectAccountResponse
from ethos.elint.services.product.identity.account_assistant.connect_account_assistant_pb2_grpc import \
    ConnectAccountAssistantServiceServicer
from models.account_assistant_connection_models import AccountAssistantConnections
from models.account_connection_models import AccountConnections
from services_caller.account_assistant_service_caller import validate_account_assistant_services_caller
from support.helper_functions import gen_uuid


class ConnectAccountAssistantService(ConnectAccountAssistantServiceServicer):
    def __init__(self):
        super(ConnectAccountAssistantService, self).__init__()
        self.session_scope = self.__class__.__name__

    def IsAccountConnected(self, request, context):
        print("ConnectAccountAssistantService:IsAccountConnected")
        account_assistant_connections = AccountAssistantConnections(account_assistant_id=request.account_assistant_id)
        account_connected = account_assistant_connections.is_account_connected(
            account_id=request.connected_account.account_id)
        if account_connected is False:
            return ResponseMeta(meta_done=account_connected, meta_message="Account not connected.")
        else:
            return ResponseMeta(meta_done=account_connected, meta_message="Account connected.")

    def ConnectAccount(self, request, context):
        print("ConnectAccountAssistantService:ConnectAccount")
        validation_done, validation_message = validate_account_assistant_services_caller(
            access_auth_details=request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return ConnectAccountResponse(response_meta=response_meta)
        else:
            account_assistant_connections = AccountAssistantConnections(
                account_assistant_id=request.access_auth_details.account_assistant.account_assistant_id)
            is_account_connection_exists = account_assistant_connections.is_account_connected(
                account_id=request.connecting_account_id)
            if is_account_connection_exists is False:
                new_connection_id = gen_uuid()
                connecting_account_connections = AccountConnections(account_id=request.connecting_account_id)
                account_assistant_connections.add_new_account_connection(
                    account_connection_id=new_connection_id,
                    account_id=request.connecting_account_id
                )
                connecting_account_connections.add_new_account_assistant_connection(
                    account_assistant_connection_id=new_connection_id,
                    account_assistant_id=request.access_auth_details.account_assistant.account_assistant_id
                )
                connected_account = account_assistant_connections.get_connected_account(
                    account_id=request.connecting_account_id)
                return ConnectAccountResponse(
                    connected_account=connected_account,
                    response_meta=ResponseMeta(meta_done=True, meta_message="Account Connected.")
                )
            else:
                connected_account = account_assistant_connections.get_connected_account(
                    account_id=request.connecting_account_id)
                return ConnectAccountResponse(
                    connected_account=connected_account,
                    response_meta=ResponseMeta(meta_done=True, meta_message="Account already connected.")
                )
