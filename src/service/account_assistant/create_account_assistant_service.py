import logging

from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account_assistant.create_account_assistant_pb2 import \
    CreateAccountAssistantResponse, GetAccountAssistantNameCodeResponse
from ethos.elint.services.product.identity.account_assistant.create_account_assistant_pb2_grpc import \
    CreateAccountAssistantServiceServicer
from models.account_assistant_connection_models import AccountAssistantConnections
from models.account_connection_models import AccountConnections
from services_caller.account_assistant_service_caller import account_assistant_access_token_caller
from services_caller.account_service_caller import validate_account_services_caller
from services_caller.message_conversation_service_caller import setup_account_assistant_conversations_caller
from support.db_service import add_new_account_assistant, get_account_assistant_name_code
from support.helper_functions import gen_uuid


class CreateAccountAssistantService(CreateAccountAssistantServiceServicer):
    def __init__(self):
        super(CreateAccountAssistantService, self).__init__()
        self.session_scope = self.__class__.__name__

    def CreateAccountAssistant(self, request, context):
        logging.info("CreateAccountAssistantService:CreateAccountAssistant")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return CreateAccountAssistantResponse(response_meta=response_meta)
        else:
            new_account_assistant_id = add_new_account_assistant(account_id=request.account.account_id)
            # setup account assistant connections
            account_assistant_connections = AccountAssistantConnections(account_assistant_id=new_account_assistant_id)
            account_assistant_connections.setup_account_assistant_connections()
            # add new account assistant to account connections
            account_connections = AccountConnections(account_id=request.account.account_id)
            new_connection_id = gen_uuid()
            account_assistant_connections.add_new_account_connection(
                account_connection_id=new_connection_id,
                account_id=request.account.account_id)
            account_connections.add_new_account_assistant_connection(
                account_assistant_connection_id=new_connection_id,
                account_assistant_id=new_account_assistant_id
            )
            access_done, access_message, access_auth_details = account_assistant_access_token_caller(request)
            # setup account assistant conversation
            _, _ = setup_account_assistant_conversations_caller(access_auth_details=access_auth_details)
            if access_done is False:
                return CreateAccountAssistantResponse(
                    response_meta=ResponseMeta(meta_done=access_done, meta_message=access_message))
            else:
                return CreateAccountAssistantResponse(
                    account_assistant_services_access_auth_details=access_auth_details, response_meta=response_meta)

    def GetAccountAssistantNameCode(self, request, context):
        logging.info("CreateAccountAssistantService:GetAccountAssistantNameCode")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetAccountAssistantNameCodeResponse(response_meta=response_meta)
        else:
            return GetAccountAssistantNameCodeResponse(
                account_assistant_name_code=get_account_assistant_name_code(
                    account_assistant_name=request.account_assistant_name),
                response_meta=response_meta)
