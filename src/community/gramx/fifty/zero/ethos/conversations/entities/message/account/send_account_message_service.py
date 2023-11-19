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

from ethos.elint.entities.account_assistant_pb2 import AccountAssistantConnectedAccount
from ethos.elint.entities.account_pb2 import AccountConnectedAccount
from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.conversation.message.account.send_account_message_pb2 import \
    MessageForAccountAssistantSent, MessageForAccountSent, SyncAccountSentMessagesResponse, FullMessageForAccountSent, \
    SyncAccountConnectedAccountSentMessagesResponse, AccountSentMessage, \
    SyncAccountConnectedAccountAssistantSentMessagesResponse, AccountAssistantSentMessage, \
    GetLast24ProductNSentMessagesResponse, AccountSentMessagesCountResponse, AccountAssistantSentMessagesCountResponse, \
    GetAccountLastSentMessageResponse, GetAccountAssistantLastSentMessageResponse, \
    GetSentMessagesAccountAssistantsResponse, GetSentMessagesAccountsResponse
from ethos.elint.services.product.conversation.message.account.send_account_message_pb2_grpc import \
    SendAccountMessageServiceServicer
from ethos.elint.services.product.identity.account.discover_account_pb2 import GetAccountByIdRequest
from ethos.elint.services.product.identity.account_assistant.discover_account_assistant_pb2 import \
    GetAccountAssistantByIdRequest

from application_context import ApplicationContext
from community.gramx.fifty.zero.ethos.conversations.models.account_conversation_models import AccountConversations
from community.gramx.fifty.zero.ethos.conversations.models.base_models import AccountSpeedMessaging
from community.gramx.fifty.zero.ethos.conversations.services_caller import account_assistant_message_service_caller, \
    account_message_service_caller
from community.gramx.fifty.zero.ethos.conversations.services_caller.account_service_caller import \
    validate_account_services_caller, is_account_assistant_connected_caller, is_account_connected_caller
from support.helper_functions import format_timestamp_to_datetime
from support.session.redis_service import set_kv


class SendAccountMessageService(SendAccountMessageServiceServicer):
    def __init__(self):
        super(SendAccountMessageService, self).__init__()
        self.session_scope = self.__class__.__name__

    def SendMessageToAccountAssistant(self, request, context):
        logging.info("SendAccountMessageService:SendMessageToAccountAssistant")
        validation_done, validate_message = validate_account_services_caller(request.access_auth_details)
        if validation_done is False:
            return MessageForAccountAssistantSent(is_sent=False)
        else:
            is_connected, connection_message = is_account_assistant_connected_caller(
                account_id=request.access_auth_details.account.account_id,
                connected_account_assistant=request.connected_account_assistant)
            if is_connected is False:
                return MessageForAccountAssistantSent(is_sent=False)
            else:
                account_conversations = AccountConversations(account_id=request.access_auth_details.account.account_id)
                account_assistant_sent_message_id = account_conversations.add_account_assistant_sent_message(
                    account_assistant_id=request.connected_account_assistant.account_assistant_id,
                    account_assistant_connection_id=request.connected_account_assistant.account_assistant_connection_id,
                    message=request.message,
                    message_space=1,
                    message_space_action=request.space_knowledge_action,
                    sent_at=format_timestamp_to_datetime(request.access_auth_details.requested_at)
                )
                is_received, received_at = account_assistant_message_service_caller.receive_message_from_account_caller(
                    account_assistant_id=request.connected_account_assistant.account_assistant_id,
                    connected_account=AccountAssistantConnectedAccount(
                        account_connection_id=request.connected_account_assistant.account_assistant_connection_id,
                        account_id=request.access_auth_details.account.account_id,
                        connected_at=request.connected_account_assistant.connected_at
                    ),
                    space_knowledge_action=request.space_knowledge_action,
                    message=request.message,
                    account_received_message_id=account_assistant_sent_message_id
                )
                if is_received is False:
                    return MessageForAccountAssistantSent(is_sent=False)
                else:
                    account_conversations.update_account_assistant_sent_message_received_at(
                        account_assistant_sent_message_id=account_assistant_sent_message_id,
                        received_at=format_timestamp_to_datetime(received_at)
                    )
                    return MessageForAccountAssistantSent(
                        account_assistant_sent_message_id=account_assistant_sent_message_id,
                        is_sent=is_received, sent_at=request.access_auth_details.requested_at, received_at=received_at
                    )

    def SendMessageToAccount(self, request, context):
        logging.info("SendAccountMessageService:SendMessageToAccount")
        is_connected, connection_message = is_account_connected_caller(
            account_id=request.access_auth_details.account.account_id,
            connected_account=request.connected_account)
        if is_connected is False:
            return MessageForAccountSent(is_sent=False)
        else:
            account_conversations = AccountConversations(account_id=request.access_auth_details.account.account_id)
            account_sent_message_id = account_conversations.add_account_sent_message(
                account_id=request.connected_account.account_id,
                account_connection_id=request.connected_account.account_connection_id,
                message=request.message,
                sent_at=format_timestamp_to_datetime(request.access_auth_details.requested_at)
            )
            is_received, received_at = account_message_service_caller.receive_message_from_account_caller(
                account_id=request.connected_account.account_id,
                connected_account=AccountConnectedAccount(
                    account_connection_id=request.connected_account.account_connection_id,
                    account_id=request.access_auth_details.account.account_id,
                    connected_at=request.connected_account.connected_at
                ),
                message=request.message,
                account_received_message_id=account_sent_message_id
            )
            if is_received is False:
                return MessageForAccountSent(is_sent=False)
            else:
                account_conversations.update_account_sent_message_received_at(
                    account_sent_message_id=account_sent_message_id,
                    received_at=format_timestamp_to_datetime(received_at)
                )
                set_kv(key=f"rm_{request.connected_account.account_id}_pending", value=str(1))
                return MessageForAccountSent(
                    account_sent_message_id=account_sent_message_id,
                    is_sent=True, sent_at=request.access_auth_details.requested_at, received_at=received_at)

    def SendSpeedMessageToAccount(self, request_iterator, context):
        logging.info("SendAccountMessageService:SendSpeedMessageToAccount")
        account_id = ""
        for metadata in context.invocation_metadata():
            if metadata[0] == "account-id":
                account_id = metadata[1]
                break
        account_speed_messaging = AccountSpeedMessaging(account_id=account_id)
        account_speed_messaging.account_speed_message_sending_on()
        context.add_callback(lambda: account_speed_messaging.account_speed_message_sending_off())
        for request in request_iterator:
            response = ApplicationContext.send_account_message_service_stub().SendMessageToAccount(request)
            yield FullMessageForAccountSent(
                message_for_account_sent=response,
                connected_account=request.connected_account,
                message=request.message,
            )

    def SyncAccountSentMessages(self, request, context):
        logging.info("SendAccountMessageService:SyncAccountSentMessages")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return SyncAccountSentMessagesResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.account.account_id)
            for account_sent_message in account_conversations.get_all_account_sent_messages():
                yield SyncAccountSentMessagesResponse(
                    account_sent_message=account_sent_message,
                    response_meta=response_meta
                )

    def SyncAccountConnectedAccountSentMessages(self, request, context):
        logging.info("SendAccountMessageService:SyncAccountConnectedAccountSentMessages")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return SyncAccountConnectedAccountSentMessagesResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.access_auth_details.account.account_id)
            for account_sent_message_dict in account_conversations.get_all_account_connected_account_sent_messages(
                    account_id=request.connected_account.account_id):
                yield SyncAccountConnectedAccountSentMessagesResponse(
                    account_sent_message=account_sent_message_dict.get('message', AccountSentMessage()),
                    response_meta=response_meta,
                    sync_progress=account_sent_message_dict.get('progress', 0.0)
                )

    def SyncAccountConnectedAccountAssistantSentMessages(self, request, context):
        logging.info("SendAccountMessageService:SyncAccountConnectedAccountAssistantSentMessages")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return SyncAccountConnectedAccountAssistantSentMessagesResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.access_auth_details.account.account_id)
            for account_assistant_sent_message_dict in account_conversations.get_all_account_connected_account_assistant_sent_messages(
                    account_assistant_id=request.connected_account_assistant.account_assistant_id):
                yield SyncAccountConnectedAccountAssistantSentMessagesResponse(
                    account_assistant_sent_message=account_assistant_sent_message_dict.get(
                        'message',
                        AccountAssistantSentMessage()),
                    response_meta=response_meta,
                    sync_progress=account_assistant_sent_message_dict.get('progress', 0.0)
                )

    def GetLast24ProductNSentMessages(self, request, context):
        logging.info("SendAccountMessageService:GetLast24ProductNSentMessages")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetLast24ProductNSentMessagesResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.access_auth_details.account.account_id)
            time_24_hours_product_n_ago = datetime.datetime.now() - datetime.timedelta(days=request.product_n)
            if request.message_entity_enum == 0:
                # get sent messages for both account and assistant
                account_sent_messages = []
                account_assistant_sent_messages = []
                for account_sent_message_dict in account_conversations.get_all_account_connected_account_sent_messages(
                        account_id=request.connected_account.account_id, filter_from_datetime=True,
                        from_datetime=time_24_hours_product_n_ago):
                    account_sent_messages.append(account_sent_message_dict.get('message', AccountSentMessage()))
                for account_assistant_sent_message_dict in account_conversations.get_all_account_connected_account_assistant_sent_messages(
                        account_assistant_id=request.connected_account_assistant.account_assistant_id,
                        filter_from_datetime=True,
                        from_datetime=time_24_hours_product_n_ago):
                    account_assistant_sent_messages.append(account_assistant_sent_message_dict.get('message',
                                                                                                   AccountAssistantSentMessage()))
                # closing the stream
                return GetLast24ProductNSentMessagesResponse(response_meta=response_meta,
                                                             account_sent_messages=account_sent_messages,
                                                             account_assistant_sent_messages=account_assistant_sent_messages)
            elif request.message_entity_enum == 1:
                # get sent messages for account
                account_sent_messages = []
                for account_sent_message_dict in account_conversations.get_all_account_connected_account_sent_messages(
                        account_id=request.connected_account.account_id, filter_from_datetime=True,
                        from_datetime=time_24_hours_product_n_ago):
                    account_sent_messages.append(account_sent_message_dict.get('message', AccountSentMessage()))
                # closing the stream
                return GetLast24ProductNSentMessagesResponse(response_meta=response_meta,
                                                             account_sent_messages=account_sent_messages)
            elif request.message_entity_enum == 2:
                # get sent messages for account assistant
                account_assistant_sent_messages = []
                for account_assistant_sent_message_dict in account_conversations.get_all_account_connected_account_assistant_sent_messages(
                        account_assistant_id=request.connected_account_assistant.account_assistant_id,
                        filter_from_datetime=True,
                        from_datetime=time_24_hours_product_n_ago):
                    account_assistant_sent_messages.append(account_assistant_sent_message_dict.get('message',
                                                                                                   AccountAssistantSentMessage()))
                # closing the stream
                return GetLast24ProductNSentMessagesResponse(response_meta=response_meta,
                                                             account_assistant_sent_messages=account_assistant_sent_messages)

    def GetAccountSentMessagesCount(self, request, context):
        logging.info("SendAccountMessageService:GetAccountSentMessagesCount")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return AccountSentMessagesCountResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.account.account_id)
            return AccountSentMessagesCountResponse(
                account_sent_messages_count=account_conversations.get_account_sent_messages_count(),
                response_meta=response_meta
            )

    def GetAccountAssistantSentMessagesCount(self, request, context):
        logging.info("SendAccountMessageService:GetAccountAssistantSentMessagesCount")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return AccountAssistantSentMessagesCountResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.account.account_id)
            return AccountAssistantSentMessagesCountResponse(
                account_assistant_sent_messages_count=account_conversations.get_account_assistant_sent_messages_count(),
                response_meta=response_meta
            )

    # LAST MESSAGES

    def GetAccountLastSentMessage(self, request, context):
        logging.info("SendAccountMessageService:GetAccountLastSentMessage")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetAccountLastSentMessageResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.access_auth_details.account.account_id)
            last_sent_message = account_conversations.get_account_last_sent_message(
                account_id=request.connected_account_id)
            return GetAccountLastSentMessageResponse(response_meta=response_meta,
                                                     last_sent_message=last_sent_message)

    def GetAccountAssistantLastSentMessage(self, request, context):
        logging.info("SendAccountMessageService:GetAccountLastSentMessage")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetAccountAssistantLastSentMessageResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.access_auth_details.account.account_id)
            last_sent_message = account_conversations.get_account_assistant_last_sent_message(
                account_assistant_id=request.connected_account_assistant_id)
            return GetAccountAssistantLastSentMessageResponse(response_meta=response_meta,
                                                              last_sent_message=last_sent_message)

    def GetSentMessagesAccounts(self, request, context):
        logging.info("SendAccountMessageService:GetSentMessagesAccounts")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetSentMessagesAccountsResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.account.account_id)
            sent_messages_account_ids = account_conversations.get_sent_messages_account_ids()
            sent_messages_accounts = []
            for sent_messages_account_id in sent_messages_account_ids:
                sent_messages_accounts.append(
                    ApplicationContext.discover_account_service_stub().GetAccountById(
                        GetAccountByIdRequest(account_id=sent_messages_account_id)).account
                )
            return GetSentMessagesAccountsResponse(
                sent_messages_accounts=sent_messages_accounts,
                response_meta=response_meta
            )

    def GetSentMessagesAccountAssistants(self, request, context):
        logging.info("SendAccountMessageService:GetSentMessagesAccountAssistants")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetSentMessagesAccountAssistantsResponse(response_meta=response_meta)
        else:
            account_conversations = AccountConversations(account_id=request.account.account_id)
            sent_messages_account_assistant_ids = account_conversations.get_sent_messages_account_assistant_ids()
            sent_messages_account_assistants = []
            for sent_messages_account_assistant_id in sent_messages_account_assistant_ids:
                sent_messages_account_assistants.append(
                    ApplicationContext.discover_account_assistant_service_stub().GetAccountAssistantById(
                        GetAccountAssistantByIdRequest(
                            access_auth_details=request,
                            account_assistant_id=sent_messages_account_assistant_id
                        )
                    ).account_assistant
                )
            return GetSentMessagesAccountAssistantsResponse(
                sent_messages_account_assistants=sent_messages_account_assistants,
                response_meta=response_meta
            )
