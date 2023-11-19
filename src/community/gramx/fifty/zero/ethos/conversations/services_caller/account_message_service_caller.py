from google.protobuf.any_pb2 import Any
from google.protobuf.timestamp_pb2 import Timestamp

from application_context import ApplicationContext
from ethos.elint.entities.account_pb2 import AccountConnectedAccountAssistant, AccountConnectedAccount
from ethos.elint.services.product.conversation.message.account.receive_account_message_pb2 import \
    MessageFromAccountAssistant, MessageFromAccount


def receive_message_from_account_assistant_caller(
        account_id: str, connected_account_assistant: AccountConnectedAccountAssistant,
        message: str, message_source_space_id: str, message_source_space_type_id: str,
        message_source_space_domain_id: str, message_source_space_domain_action: int,
        message_source_space_domain_action_context_id: str, message_source: Any,
        account_assistant_received_message_id: str) -> (
        bool, Timestamp):
    stub = ApplicationContext.receive_account_message_service_stub()
    response = stub.ReceiveMessageFromAccountAssistant(MessageFromAccountAssistant(
        account_id=account_id, connected_account_assistant=connected_account_assistant,
        message=message, message_source_space_id=message_source_space_id,
        message_source_space_type_id=message_source_space_type_id,
        message_source_space_domain_id=message_source_space_domain_id,
        message_source_space_domain_action=message_source_space_domain_action,
        message_source_space_domain_action_context_id=message_source_space_domain_action_context_id,
        message_source=message_source,
        account_assistant_received_message_id=account_assistant_received_message_id))
    return response.is_received, response.received_at


def receive_message_from_account_caller(
        account_id: str, connected_account: AccountConnectedAccount,
        message: str, account_received_message_id: str) -> (bool, Timestamp):
    stub = ApplicationContext.receive_account_message_service_stub()
    response = stub.ReceiveMessageFromAccount(MessageFromAccount(
        account_id=account_id, connected_account=connected_account,
        message=message, account_received_message_id=account_received_message_id
    ))
    return response.is_received, response.received_at
