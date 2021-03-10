from google.protobuf.any_pb2 import Any

from application_context import ApplicationContext
from ethos.elint.entities.account_assistant_pb2 import AccountAssistantConnectedAccount
from ethos.elint.services.product.conversation.message.account_assistant.send_account_assistant_message_pb2 import \
    MessageForAccount
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails


def send_message_to_account(access_auth_details: AccountAssistantServicesAccessAuthDetails,
                            connected_account: AccountAssistantConnectedAccount, message: str, message_source: [Any]):
    stub = ApplicationContext.send_account_assistant_message_service_stub()
    response = stub.SendMessageToAccount(MessageForAccount(
        access_auth_details=access_auth_details,
        connected_account=connected_account,
        message=message,
        message_source=message_source
    ))
    return response
