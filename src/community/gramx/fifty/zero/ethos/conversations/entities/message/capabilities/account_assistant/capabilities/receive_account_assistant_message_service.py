#   /*************************************************************************
#   *
#   * AMIT KUMAR KHETAN CONFIDENTIAL
#   * __________________
#   *
#   *  [2017] - [2021] Amit Kumar Khetan
#   *  All Rights Reserved.
#   *
#   * NOTICE:  All information contained herein is, and remains
#   * the property of Amit Kumar Khetan and its suppliers,
#   * if any.  The intellectual and technical concepts contained
#   * herein are proprietary to Amit Kumar Khetan
#   * and its suppliers and may be covered by U.S. and Foreign Patents,
#   * patents in process, and are protected by trade secret or copyright law.
#   * Dissemination of this information or reproduction of this material
#   * is strictly forbidden unless prior written permission is obtained
#   * from Amit Kumar Khetan.
#   */

import logging

from ethos.elint.services.product.conversation.message.account_assistant.receive_account_assistant_message_pb2 import \
    MessageFromAccountReceived
from ethos.elint.services.product.conversation.message.account_assistant.receive_account_assistant_message_pb2_grpc import \
    ReceiveAccountAssistantMessageServiceServicer
from google.protobuf.json_format import MessageToJson

from community.gramx.fifty.zero.ethos.conversations.entities.message.capabilities import act_on_account_message
from community.gramx.fifty.zero.ethos.conversations.models.account_assistant_conversation_models import \
    AccountAssistantConversations
from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.access.consumers.access_account_assistant_consumer import \
    AccessAccountAssistantConsumer
from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.connect.consumers.connect_account_assistant_consumer import \
    ConnectAccountAssistantConsumer
from support.application.tracing import trace_rpc
from support.helper_functions import get_current_timestamp, format_timestamp_to_datetime


class ReceiveAccountAssistantMessageService(ReceiveAccountAssistantMessageServiceServicer):
    def __init__(self):
        super(ReceiveAccountAssistantMessageService, self).__init__()
        self.session_scope = self.__class__.__name__

    @trace_rpc()
    def ReceiveMessageFromAccount(self, request, context):
        logging.info("ReceiveAccountAssistantMessageService:ReceiveMessageFromAccount")
        connect_consumer = ConnectAccountAssistantConsumer
        is_connected, connection_message = connect_consumer.is_account_connected(
            account_assistant_id=request.account_assistant_id,
            connected_account=request.connected_account
        )
        if is_connected is False:
            return MessageFromAccountReceived(is_received=is_connected)
        else:
            received_at = get_current_timestamp()
            account_assistant_conversations = AccountAssistantConversations(
                account_assistant_id=request.account_assistant_id)
            account_assistant_conversations.add_account_received_message(
                account_received_message_id=request.account_received_message_id,
                account_id=request.connected_account.account_id,
                account_connection_id=request.connected_account.account_connection_id,
                message=request.message,
                message_space=1,
                message_space_action=request.space_knowledge_action,
                received_at=format_timestamp_to_datetime(received_at)
            )
            # pass the message to action based on action
            access_consumer = AccessAccountAssistantConsumer
            access_done, access_message, access_auth_details = access_consumer.account_assistant_access_token_with_master_connection(
                account_assistant_id=request.account_assistant_id,
                connected_account=request.connected_account
            )
            if access_done is False:
                return MessageFromAccountReceived(is_received=access_done)
            else:
                act_on_account_message.apply_async((MessageToJson(access_auth_details),
                                                    MessageToJson(request.connected_account),
                                                    request.space_knowledge_action,
                                                    request.message
                                                    ), queue="eapp_conversation_queue")
                return MessageFromAccountReceived(is_received=access_done, received_at=get_current_timestamp())
