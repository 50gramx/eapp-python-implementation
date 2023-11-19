from application_context import ApplicationContext
from ethos.elint.services.product.identity.account.access_account_pb2 import AccountServicesAccessAuthDetails
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails


def setup_account_conversations_caller(access_auth_details: AccountServicesAccessAuthDetails):
    stub = ApplicationContext.message_conversation_service_stub()
    response = stub.SetupAccountConversations(access_auth_details)
    return response.meta_done, response.meta_message


def setup_account_assistant_conversations_caller(access_auth_details: AccountAssistantServicesAccessAuthDetails):
    stub = ApplicationContext.message_conversation_service_stub()
    response = stub.SetupAccountAssistantConversations(access_auth_details)
    return response.meta_done, response.meta_message
