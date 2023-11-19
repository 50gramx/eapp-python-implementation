from google.protobuf.any_pb2 import Any
from google.protobuf.timestamp_pb2 import Timestamp

from application_context import ApplicationContext
from ethos.elint.entities.account_assistant_pb2 import AccountAssistantConnectedAccount
from ethos.elint.entities.space_knowledge_pb2 import SpaceKnowledgeAction
from ethos.elint.services.product.conversation.message.account_assistant.receive_account_assistant_message_pb2 import \
    MessageFromAccount
from ethos.elint.services.product.conversation.message.account_assistant.send_account_assistant_message_pb2 import \
    MessageForAccount
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails


def receive_message_from_account_caller(
        account_assistant_id: str, connected_account: AccountAssistantConnectedAccount,
        space_knowledge_action: SpaceKnowledgeAction, message: str, account_received_message_id: str) -> (
        bool, Timestamp):
    stub = ApplicationContext.receive_account_assistant_message_service_stub()
    response = stub.ReceiveMessageFromAccount(MessageFromAccount(
        account_assistant_id=account_assistant_id, connected_account=connected_account,
        space_knowledge_action=space_knowledge_action, message=message,
        account_received_message_id=account_received_message_id))
    return response.is_received, response.received_at


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
