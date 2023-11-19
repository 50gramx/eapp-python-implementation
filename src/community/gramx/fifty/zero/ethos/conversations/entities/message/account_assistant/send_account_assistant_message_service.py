import logging

from ethos.elint.entities.account_pb2 import AccountConnectedAccountAssistant
from ethos.elint.services.product.conversation.message.account_assistant.send_account_assistant_message_pb2 import \
    MessageForAccountSent
from ethos.elint.services.product.conversation.message.account_assistant.send_account_assistant_message_pb2_grpc import \
    SendAccountAssistantMessageServiceServicer

from community.gramx.fifty.zero.ethos.conversations.models.account_assistant_conversation_models import \
    AccountAssistantConversations
from community.gramx.fifty.zero.ethos.conversations.services_caller.account_message_service_caller import \
    receive_message_from_account_assistant_caller
from community.gramx.fifty.zero.ethos.identity.services_caller.account_assistant_service_caller import \
    validate_account_assistant_services_caller, is_account_connected_caller
from support.helper_functions import format_timestamp_to_datetime


class SendAccountAssistantMessageService(SendAccountAssistantMessageServiceServicer):
    def __init__(self):
        super(SendAccountAssistantMessageService, self).__init__()
        self.session_scope = self.__class__.__name__

    def SendMessageToAccount(self, request, context):
        logging.info("SendAccountAssistantMessageService:SendMessageToAccount")
        validation_done, validation_message = validate_account_assistant_services_caller(request.access_auth_details)
        if validation_done is False:
            return MessageForAccountSent(is_sent=validation_done)
        else:
            is_connected, connection_message = is_account_connected_caller(
                account_assistant_id=request.access_auth_details.account_assistant.account_assistant_id,
                connected_account=request.connected_account)
            if is_connected is False:
                return MessageForAccountSent(is_sent=False)
            else:
                account_assistant_conversations = AccountAssistantConversations(
                    account_assistant_id=request.access_auth_details.account_assistant.account_assistant_id)
                account_sent_message_id = account_assistant_conversations.add_account_sent_message(
                    account_id=request.connected_account.account_id,
                    account_connection_id=request.connected_account.account_connection_id,
                    message=request.message,
                    message_source_space_id=request.message_source_space_id,
                    message_source_space_type_id=request.message_source_space_type_id,
                    message_source_space_domain_id=request.message_source_space_domain_id,
                    message_source_space_domain_action=request.message_source_space_domain_action,
                    message_source_space_domain_action_context_id=request.message_source_space_domain_action_context_id,
                    sent_at=format_timestamp_to_datetime(request.access_auth_details.requested_at)
                )
                is_received, received_at = receive_message_from_account_assistant_caller(
                    account_id=request.connected_account.account_id,
                    connected_account_assistant=AccountConnectedAccountAssistant(
                        account_assistant_connection_id=request.connected_account.account_connection_id,
                        account_assistant_id=request.access_auth_details.account_assistant.account_assistant_id,
                        connected_at=request.connected_account.connected_at
                    ),
                    message=request.message,
                    message_source_space_id=request.message_source_space_id,
                    message_source_space_type_id=request.message_source_space_type_id,
                    message_source_space_domain_id=request.message_source_space_domain_id,
                    message_source_space_domain_action=request.message_source_space_domain_action,
                    message_source_space_domain_action_context_id=request.message_source_space_domain_action_context_id,
                    message_source=request.message_source,
                    account_assistant_received_message_id=account_sent_message_id
                )
                if is_received is False:
                    return MessageForAccountSent(is_sent=False)
                else:
                    account_assistant_conversations.update_account_sent_message_received_at(
                        account_sent_message_id=account_sent_message_id,
                        received_at=format_timestamp_to_datetime(received_at))
                    return MessageForAccountSent(is_sent=is_received,
                                                 sent_at=request.access_auth_details.requested_at,
                                                 received_at=received_at)
