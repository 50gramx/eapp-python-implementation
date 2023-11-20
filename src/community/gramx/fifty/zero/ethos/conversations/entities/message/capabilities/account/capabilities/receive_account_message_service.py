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

import datetime
import logging

from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.conversation.message.account.receive_account_message_pb2 import \
    MessageFromAccountAssistantReceived, ListenForReceivedAccountAssistantMessagesResponse, \
    ListenForReceivedAccountMessagesResponse, MessageFromAccount, SyncAccountReceivedMessagesResponse, \
    ListenForReceivedAccountSpeedMessagesResponse, SyncAccountConnectedAccountReceivedMessagesResponse, \
    AccountReceivedMessage, SyncAccountConnectedAccountAssistantReceivedMessagesResponse, \
    AccountAssistantReceivedMessage, GetLast24ProductNReceivedMessagesResponse, MessageFromAccountReceived, \
    AccountAssistantReceivedMessagesCountResponse, AccountReceivedMessagesCountResponse, \
    GetAccountLastReceivedMessageResponse, GetAccountAssistantLastReceivedMessageResponse, \
    GetReceivedMessagesAccountsResponse, GetReceivedMessagesAccountAssistantsResponse, MessageFromAccountAssistant
from ethos.elint.services.product.conversation.message.account.receive_account_message_pb2_grpc import \
    ReceiveAccountMessageServiceServicer
from ethos.elint.services.product.identity.account.discover_account_pb2 import GetAccountByIdRequest
from ethos.elint.services.product.identity.account_assistant.discover_account_assistant_pb2 import \
    GetAccountAssistantByIdRequest
from google.protobuf.text_format import MessageToString, Parse

from application_context import ApplicationContext
from community.gramx.fifty.zero.ethos.conversations.models.account_conversation_models import AccountConversations
from community.gramx.fifty.zero.ethos.conversations.models.base_models import AccountSpeedMessaging
from community.gramx.fifty.zero.ethos.conversations.services_caller.account_service_caller import \
    is_account_assistant_connected_caller, new_received_message_from_account_assistant_caller, \
    is_account_connected_caller, new_received_message_from_account_caller, validate_account_services_caller
from support.application.tracing import trace_rpc
from support.helper_functions import get_current_timestamp, format_timestamp_to_datetime
from support.session.redis_service import get_kv, set_kv, rpush, quick_store_list_pop_all_items, quick_store_list_length


class ReceiveAccountMessageService(ReceiveAccountMessageServiceServicer):
    def __init__(self):
        super(ReceiveAccountMessageService, self).__init__()
        self.session_scope = self.__class__.__name__

    @trace_rpc()
    def ReceiveMessageFromAccountAssistant(self, request, context):
        logging.info("ReceiveAccountMessageService:ReceiveMessageFromAccountAssistant")
        logging.info(f"request:{request}")
        is_connected, connection_message = is_account_assistant_connected_caller(
            account_id=request.account_id,
            connected_account_assistant=request.connected_account_assistant
        )
        if is_connected is False:
            return MessageFromAccountAssistantReceived(is_received=is_connected)
        else:
            received_at = get_current_timestamp()
            account_conversations = AccountConversations(account_id=request.account_id)
            account_conversations.add_account_assistant_received_message(
                account_assistant_received_message_id=request.account_assistant_received_message_id,
                account_assistant_id=request.connected_account_assistant.account_assistant_id,
                account_assistant_connection_id=request.connected_account_assistant.account_assistant_connection_id,
                message=request.message,
                message_source_space_id=request.message_source_space_id,
                message_source_space_type_id=request.message_source_space_type_id,
                message_source_space_domain_id=request.message_source_space_domain_id,
                message_source_space_domain_action=request.message_source_space_domain_action,
                message_source_space_domain_action_context_id=request.message_source_space_domain_action_context_id,
                received_at=format_timestamp_to_datetime(received_at)
            )
            message_from_account_assistant = MessageFromAccountAssistant(
                account_id=request.account_id,
                connected_account_assistant=request.connected_account_assistant,
                message=request.message,
                message_source_space_id=request.message_source_space_id,
                message_source_space_type_id=request.message_source_space_type_id,
                message_source_space_domain_id=request.message_source_space_domain_id,
                message_source_space_domain_action=request.message_source_space_domain_action,
                message_source_space_domain_action_context_id=request.message_source_space_domain_action_context_id,
                message_source=request.message_source,
                account_assistant_received_message_id=request.account_assistant_received_message_id
            )
            rpush(list_key=f"raam_{request.account_id}",
                  item=MessageToString(message_from_account_assistant, as_one_line=True))
            logging.info(f"request.connected_account_assistant.account_assistant_id"
                         f":{request.connected_account_assistant.account_assistant_id}")
            _, _ = new_received_message_from_account_assistant_caller(
                account_id=request.account_id,
                connecting_account_assistant_id=request.connected_account_assistant.account_assistant_id,
                message=request.message
            )
            return MessageFromAccountAssistantReceived(is_received=True, received_at=received_at)

    @trace_rpc()
    def ReceiveMessageFromAccount(self, request, context):
        logging.info("ReceiveAccountMessageService:ReceiveMessageFromAccount")
        is_connected, connection_message = is_account_connected_caller(
            account_id=request.account_id,
            connected_account=request.connected_account
        )
        if is_connected is False:
            return MessageFromAccountReceived(is_received=is_connected)
        else:
            received_at = get_current_timestamp()
            account_conversations = AccountConversations(account_id=request.account_id)
            account_conversations.add_account_received_message(
                account_received_message_id=request.account_received_message_id,
                account_id=request.connected_account.account_id,
                account_connection_id=request.connected_account.account_connection_id,
                message=request.message,
                received_at=format_timestamp_to_datetime(received_at)
            )
            rpush(list_key=f"rm_{request.account_id}",
                  item=MessageToString(request, as_one_line=True))
            _, _ = new_received_message_from_account_caller(
                account_id=request.account_id,
                connecting_account_id=request.connected_account.account_id,
                message=request.message
            )
            return MessageFromAccountReceived(is_received=True, received_at=received_at)

    @trace_rpc()
    def SyncAccountReceivedMessages(self, request, context):
        logging.info("ReceiveAccountMessageService:SyncAccountReceivedMessages")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return SyncAccountReceivedMessagesResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.account.account_id)
            for account_received_message in account_conversations.get_all_account_received_messages():
                yield SyncAccountReceivedMessagesResponse(
                    account_received_message=account_received_message,
                    response_meta=response_meta
                )

    @trace_rpc()
    def SyncAccountConnectedAccountReceivedMessages(self, request, context):
        logging.info("ReceiveAccountMessageService:SyncAccountConnectedAccountReceivedMessages")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return SyncAccountConnectedAccountReceivedMessagesResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.access_auth_details.account.account_id)
            for account_received_message_dict in account_conversations.get_all_account_connected_account_received_messages(
                    account_id=request.connected_account.account_id):
                yield SyncAccountConnectedAccountReceivedMessagesResponse(
                    account_received_message=account_received_message_dict.get('message', AccountReceivedMessage()),
                    response_meta=response_meta,
                    sync_progress=account_received_message_dict.get('progress', 0.0)
                )

    @trace_rpc()
    def SyncAccountConnectedAccountAssistantReceivedMessages(self, request, context):
        logging.info("ReceiveAccountMessageService:SyncAccountConnectedAccountAssistantReceivedMessages")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return SyncAccountConnectedAccountAssistantReceivedMessagesResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.access_auth_details.account.account_id)
            for account_assistant_received_message_dict in account_conversations.get_all_account_connected_account_assistant_received_messages(
                    account_assistant_id=request.connected_account_assistant.account_assistant_id):
                yield SyncAccountConnectedAccountAssistantReceivedMessagesResponse(
                    account_assistant_received_message=account_assistant_received_message_dict.get(
                        'message',
                        AccountAssistantReceivedMessage()),
                    response_meta=response_meta,
                    sync_progress=account_assistant_received_message_dict.get('progress', 0.0)
                )

    @trace_rpc()
    def ListenForReceivedAccountAssistantMessages(self, request, context):
        logging.info("ReceiveAccountMessageService:ListenForReceivedAccountAssistantMessages")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return ListenForReceivedAccountAssistantMessagesResponse(response_meta=response_meta)
        else:
            message_from_account_assistant_list = []
            received_message_from_account_assistant_list = quick_store_list_pop_all_items(
                list_key=f"raam_{request.access_auth_details.account.account_id}")
            for message in received_message_from_account_assistant_list:
                message_from_account_assistant_list.append(
                    Parse(text=message, message=MessageFromAccountAssistant()))
            return ListenForReceivedAccountAssistantMessagesResponse(
                messages_from_account_assistant=message_from_account_assistant_list,
                response_meta=response_meta
            )

    @trace_rpc()
    def ListenForReceivedAccountMessages(self, request, context):
        logging.info("ReceiveAccountMessageService:ListenForReceivedAccountMessages")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return ListenForReceivedAccountMessagesResponse(response_meta=response_meta)
        else:
            list_of_received_messages = []
            received_message_from_account_list = quick_store_list_pop_all_items(
                list_key=f"rm_{request.access_auth_details.account.account_id}")
            for message in received_message_from_account_list:
                list_of_received_messages.append(Parse(text=message, message=MessageFromAccount()))
            return ListenForReceivedAccountMessagesResponse(
                messages_from_account=list_of_received_messages,
                response_meta=response_meta
            )

    @trace_rpc()
    def ListenForReceivedAccountSpeedMessages(self, request, context):
        logging.info("ReceiveAccountMessageService:ListenForReceivedAccountSpeedMessages")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return ListenForReceivedAccountSpeedMessagesResponse(response_meta=response_meta)
        else:
            account_id = request.account.account_id
            account_speed_messaging = AccountSpeedMessaging(account_id=account_id)
            account_speed_messaging.account_speed_message_listening_on()
            context.add_callback(lambda: account_speed_messaging.account_speed_message_listening_off())
            while True:
                PENDING_MESSAGE = get_kv(key=f"rm_{account_id}_pending")
                if PENDING_MESSAGE is not None and int(PENDING_MESSAGE) == 1:
                    received_message_from_account_list = quick_store_list_pop_all_items(
                        list_key=f"rm_{account_id}")
                    for message in received_message_from_account_list:
                        yield ListenForReceivedAccountSpeedMessagesResponse(
                            messages_from_account=Parse(text=message, message=MessageFromAccount()),
                            response_meta=response_meta
                        )
                    # check if there is no more pending messages before updating the pending status
                    if quick_store_list_length(list_key=f"rm_{account_id}") is 0:
                        set_kv(key=f"rm_{account_id}_pending", value=str(0))
                else:
                    pass

    @trace_rpc()
    def GetLast24ProductNReceivedMessages(self, request, context):
        logging.info("ReceiveAccountMessageService:GetLast24ProductNReceivedMessages")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetLast24ProductNReceivedMessagesResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.access_auth_details.account.account_id)
            time_24_hours_product_n_ago = datetime.datetime.now() - datetime.timedelta(days=request.product_n)
            if request.message_entity_enum == 0:
                # get received messages for both account and assistant
                account_received_messages = []
                account_assistant_received_messages = []
                for account_received_message_dict in account_conversations.get_all_account_connected_account_received_messages(
                        account_id=request.connected_account.account_id, filter_from_datetime=True,
                        from_datetime=time_24_hours_product_n_ago):
                    account_received_messages.append(
                        account_received_message_dict.get('message', AccountReceivedMessage())
                    )
                for account_assistant_received_message_dict in account_conversations.get_all_account_connected_account_assistant_received_messages(
                        account_assistant_id=request.connected_account_assistant.account_assistant_id,
                        filter_from_datetime=True,
                        from_datetime=time_24_hours_product_n_ago):
                    account_assistant_received_messages.append(account_assistant_received_message_dict.get('message',
                                                                                                           AccountAssistantReceivedMessage()))
                return GetLast24ProductNReceivedMessagesResponse(
                    response_meta=response_meta,
                    account_received_messages=account_received_messages,
                    account_assistant_received_messages=account_assistant_received_messages
                )
            elif request.message_entity_enum == 1:
                # get received messages for account
                account_received_messages = []
                for account_received_message_dict in account_conversations.get_all_account_connected_account_received_messages(
                        account_id=request.connected_account.account_id, filter_from_datetime=True,
                        from_datetime=time_24_hours_product_n_ago):
                    account_received_messages.append(
                        account_received_message_dict.get('message', AccountReceivedMessage()))
                # closing the stream
                return GetLast24ProductNReceivedMessagesResponse(
                    response_meta=response_meta,
                    account_received_messages=account_received_messages
                )
            elif request.message_entity_enum == 2:
                # get received messages for account assistant
                account_assistant_received_messages = []
                for account_assistant_received_message_dict in account_conversations.get_all_account_connected_account_assistant_received_messages(
                        account_assistant_id=request.connected_account_assistant.account_assistant_id,
                        filter_from_datetime=True,
                        from_datetime=time_24_hours_product_n_ago):
                    account_assistant_received_messages.append(account_assistant_received_message_dict.get('message',
                                                                                                           AccountAssistantReceivedMessage()))
                # closing the stream
                return GetLast24ProductNReceivedMessagesResponse(
                    response_meta=response_meta,
                    account_assistant_received_messages=account_assistant_received_messages)

    # MESSAGES COUNT

    @trace_rpc()
    def GetAccountReceivedMessagesCount(self, request, context):
        logging.info("SendAccountMessageService:GetAccountReceivedMessagesCount")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return AccountReceivedMessagesCountResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.account.account_id)
            return AccountReceivedMessagesCountResponse(
                account_received_messages_count=account_conversations.get_account_received_messages_count(),
                response_meta=response_meta
            )

    @trace_rpc()
    def GetAccountAssistantReceivedMessagesCount(self, request, context):
        logging.info("SendAccountMessageService:GetAccountAssistantReceivedMessagesCount")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return AccountAssistantReceivedMessagesCountResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.account.account_id)
            return AccountAssistantReceivedMessagesCountResponse(
                account_assistant_received_messages_count=account_conversations.get_account_assistant_received_messages_count(),
                response_meta=response_meta
            )

    # LAST MESSAGES

    @trace_rpc()
    def GetAccountLastReceivedMessage(self, request, context):
        logging.info("SendAccountMessageService:GetAccountLastReceivedMessage")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetAccountLastReceivedMessageResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.access_auth_details.account.account_id)
            last_received_message = account_conversations.get_account_last_received_message(
                account_id=request.connected_account_id)
            return GetAccountLastReceivedMessageResponse(response_meta=response_meta,
                                                         last_received_message=last_received_message)

    @trace_rpc()
    def GetAccountAssistantLastReceivedMessage(self, request, context):
        logging.info("SendAccountMessageService:GetAccountLastReceivedMessage")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetAccountAssistantLastReceivedMessageResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.access_auth_details.account.account_id)
            last_received_message = account_conversations.get_account_assistant_last_received_message(
                account_assistant_id=request.connected_account_assistant_id)
            return GetAccountAssistantLastReceivedMessageResponse(response_meta=response_meta,
                                                                  last_received_message=last_received_message)

    @trace_rpc()
    def GetReceivedMessagesAccounts(self, request, context):
        logging.info("SendAccountMessageService:GetReceivedMessagesAccounts")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetReceivedMessagesAccountsResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.account.account_id)
            received_messages_account_ids = account_conversations.get_received_messages_account_ids()
            received_messages_accounts = []
            for received_messages_account_id in received_messages_account_ids:
                received_messages_accounts.append(
                    ApplicationContext.discover_account_service_stub().GetAccountById(
                        GetAccountByIdRequest(account_id=received_messages_account_id)).account
                )
            return GetReceivedMessagesAccountsResponse(
                received_messages_accounts=received_messages_accounts,
                response_meta=response_meta
            )

    @trace_rpc()
    def GetReceivedMessagesAccountAssistants(self, request, context):
        logging.info("SendAccountMessageService:GetReceivedMessagesAccountAssistants")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetReceivedMessagesAccountAssistantsResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.account.account_id)
            received_messages_account_assistant_ids = account_conversations.get_received_messages_account_assistant_ids()
            received_messages_account_assistants = []
            for received_messages_account_assistant_id in received_messages_account_assistant_ids:
                received_messages_account_assistants.append(
                    ApplicationContext.discover_account_assistant_service_stub().GetAccountAssistantById(
                        GetAccountAssistantByIdRequest(
                            access_auth_details=request,
                            account_assistant_id=received_messages_account_assistant_id
                        )
                    ).account_assistant
                )
            return GetReceivedMessagesAccountAssistantsResponse(
                received_messages_account_assistants=received_messages_account_assistants,
                response_meta=response_meta
            )
