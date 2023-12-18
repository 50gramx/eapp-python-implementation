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

import collections
import logging

from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.conversation.message.account.receive_account_message_pb2 import \
    SyncAccountConnectedAccountAssistantReceivedMessagesRequest, SyncAccountConnectedAccountReceivedMessagesRequest, \
    GetLast24ProductNReceivedMessagesRequest, GetAccountLastReceivedMessageRequest, \
    GetAccountAssistantLastReceivedMessageRequest
from ethos.elint.services.product.conversation.message.account.send_account_message_pb2 import \
    SyncAccountConnectedAccountSentMessagesRequest, SyncAccountConnectedAccountAssistantSentMessagesRequest, \
    GetLast24ProductNSentMessagesRequest, GetAccountLastSentMessageRequest, GetAccountAssistantLastSentMessageRequest
from ethos.elint.services.product.conversation.message.message_conversation_pb2 import \
    AccountAndAssistantConversationsMessages, GetAccountAndAssistantConversationsResponse, \
    GetLast24ProductNConversationMessagesResponse, ConversationMessage, GetAccountLastMessageResponse, \
    GetAccountAssistantLastMessageResponse, GetConversedAccountsResponse, GetConversedAccountAssistantsResponse, \
    GetConversedAccountAndAssistantsResponse, GetAccountLastMessageRequest, GetAccountAssistantLastMessageRequest, \
    ConversedEntityWithLastConversationMessage
from ethos.elint.services.product.conversation.message.message_conversation_pb2_grpc import \
    MessageConversationServiceServicer

from application_context import ApplicationContext
from community.gramx.fifty.zero.ethos.conversations.models.account_assistant_conversation_models import \
    AccountAssistantConversations
from community.gramx.fifty.zero.ethos.conversations.models.account_conversation_models import AccountConversations
from community.gramx.fifty.zero.ethos.conversations.models.base_models import add_account_messages_in_speed
from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.access.consumers.access_account_assistant_consumer import \
    AccessAccountAssistantConsumer
from community.gramx.fifty.zero.ethos.identity.services_caller.account_service_caller import \
    validate_account_services_caller
from support.application.tracing import trace_rpc


class MessageConversationService(MessageConversationServiceServicer):
    def __init__(self):
        super(MessageConversationService, self).__init__()
        self.session_scope = self.__class__.__name__

    @trace_rpc()
    def SetupAccountConversations(self, request, context):
        logging.info("MessageConversationService:SetupAccountConversations")
        validation_done, validation_message = validate_account_services_caller(request)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return meta
        else:
            account_conversations = AccountConversations(account_id=request.account.account_id)
            account_conversations.setup_account_conversations()
            add_account_messages_in_speed(account_id=request.account.account_id)
            return meta

    @trace_rpc()
    def SetupAccountAssistantConversations(self, request, context):
        logging.info("MessageConversationService:SetupAccountAssistantConversations")
        access_consumer = AccessAccountAssistantConsumer
        validation_done, validation_message = access_consumer.validate_account_assistant_services(request)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return meta
        else:
            account_assistant_conversations = AccountAssistantConversations(
                account_assistant_id=request.account_assistant.account_assistant_id)
            account_assistant_conversations.setup_account_conversations()
            return meta

    @trace_rpc()
    def GetAccountAndAssistantConversations(self, request, context):
        logging.info("MessageConversationService:GetAccountAndAssistantConversations")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetAccountAndAssistantConversationsResponse(response_meta=response_meta)
        else:
            account_and_assistant_conversations_messages_ordered_dict = collections.OrderedDict()
            # get account assistant sent messages
            for assistant_sent_messages_response in ApplicationContext.send_account_message_service_stub().SyncAccountConnectedAccountAssistantSentMessages(
                    SyncAccountConnectedAccountAssistantSentMessagesRequest(
                        access_auth_details=request.access_auth_details,
                        connected_account_assistant=request.connected_account_assistant
                    )
            ):
                sent_message = assistant_sent_messages_response.account_assistant_sent_message
                account_and_assistant_conversations_messages_ordered_dict[
                    sent_message.sent_at.ToDatetime()] = AccountAndAssistantConversationsMessages(
                    is_message_entity_account_assistant=True,
                    is_message_sent=True,
                    account_assistant_sent_message=sent_message
                )
                # this is not as complicated as it looks
                # we are storing the messages in a dict with the key as the timestamp of the message in a ordered dict
                # we are yielding the values of the dict as a list (sorted)
                yield GetAccountAndAssistantConversationsResponse(
                    account_and_assistant_conversations_messages=list(collections.OrderedDict(
                        sorted(account_and_assistant_conversations_messages_ordered_dict.items(),
                               reverse=True)).values()),
                    response_meta=response_meta
                )
            # get account assistant received messages
            for assistant_received_messages_response in ApplicationContext.receive_account_message_service_stub().SyncAccountConnectedAccountAssistantReceivedMessages(
                    SyncAccountConnectedAccountAssistantReceivedMessagesRequest(
                        access_auth_details=request.access_auth_details,
                        connected_account_assistant=request.connected_account_assistant
                    )
            ):
                received_message = assistant_received_messages_response.account_assistant_received_message
                account_and_assistant_conversations_messages_ordered_dict[
                    received_message.received_at.ToDatetime()] = AccountAndAssistantConversationsMessages(
                    is_message_entity_account_assistant=True,
                    is_message_sent=False,
                    account_assistant_received_message=received_message
                )
                # this is not as complicated as it looks
                # we are storing the messages in a dict with the key as the timestamp of the message in a ordered dict
                # we are yielding the values of the dict as a list (sorted)
                yield GetAccountAndAssistantConversationsResponse(
                    account_and_assistant_conversations_messages=list(collections.OrderedDict(
                        sorted(account_and_assistant_conversations_messages_ordered_dict.items(),
                               reverse=True)).values()),
                    response_meta=response_meta
                )

            if request.is_account_connected:
                # get account sent messages
                for account_sent_messages_response in ApplicationContext.send_account_message_service_stub().SyncAccountConnectedAccountSentMessages(
                        SyncAccountConnectedAccountSentMessagesRequest(
                            access_auth_details=request.access_auth_details,
                            connected_account=request.connected_account
                        )
                ):
                    sent_message = account_sent_messages_response.account_sent_message
                    account_and_assistant_conversations_messages_ordered_dict[
                        sent_message.sent_at.ToDatetime()] = AccountAndAssistantConversationsMessages(
                        is_message_entity_account_assistant=False,
                        is_message_sent=True,
                        account_sent_message=sent_message
                    )
                    # this is not as complicated as it looks
                    # we are storing the messages in a dict with the key as the timestamp of the message in a ordered dict
                    # we are yielding the values of the dict as a list (sorted)
                    yield GetAccountAndAssistantConversationsResponse(
                        account_and_assistant_conversations_messages=list(collections.OrderedDict(
                            sorted(account_and_assistant_conversations_messages_ordered_dict.items(),
                                   reverse=True)).values()),
                        response_meta=response_meta
                    )
                # get account received messages
                for account_received_messages_response in ApplicationContext.receive_account_message_service_stub().SyncAccountConnectedAccountReceivedMessages(
                        SyncAccountConnectedAccountReceivedMessagesRequest(
                            access_auth_details=request.access_auth_details,
                            connected_account=request.connected_account
                        )
                ):
                    received_message = account_received_messages_response.account_received_message
                    account_and_assistant_conversations_messages_ordered_dict[
                        received_message.received_at.ToDatetime()] = AccountAndAssistantConversationsMessages(
                        is_message_entity_account_assistant=False,
                        is_message_sent=False,
                        account_received_message=received_message
                    )
                    # this is not as complicated as it looks
                    # we are storing the messages in a dict with the key as the timestamp of the message in a ordered dict
                    # we are yielding the values of the dict as a list (sorted)
                    yield GetAccountAndAssistantConversationsResponse(
                        account_and_assistant_conversations_messages=list(collections.OrderedDict(
                            sorted(account_and_assistant_conversations_messages_ordered_dict.items(),
                                   reverse=True)).values()),
                        response_meta=response_meta
                    )
            return GetAccountAndAssistantConversationsResponse(response_meta=response_meta)

    @trace_rpc()
    def GetLast24ProductNConversationMessages(self, request, context):
        logging.info("MessageConversationService:GetLast24ProductNConversationMessages")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetLast24ProductNConversationMessagesResponse(response_meta=response_meta)
        else:
            conversations_messages_ordered_dict = collections.OrderedDict()
            # stream all the received messages
            get_last_24_product_n_received_messages_request = GetLast24ProductNReceivedMessagesRequest(
                access_auth_details=request.access_auth_details,
                product_n=request.product_n,
                message_entity_enum=request.message_entity_enum,
                connected_account_assistant=request.connected_account_assistant,
                connected_account=request.connected_account
            )
            get_last_24_product_n_received_messages_response = ApplicationContext.receive_account_message_service_stub().GetLast24ProductNReceivedMessages(
                get_last_24_product_n_received_messages_request)
            for account_received_message in get_last_24_product_n_received_messages_response.account_received_messages:
                # this is the value of our ordered dict
                conversation_message = ConversationMessage(
                    is_message_entity_account_assistant=False, is_message_sent=False,
                    account_received_message=account_received_message)
                # this is the key of our ordered dict
                conversation_message_time = account_received_message.received_at.ToDatetime()
                # we create our ordered dict to sort message
                # in order with latest message first
                conversations_messages_ordered_dict[conversation_message_time] = conversation_message
            for account_assistant_received_message in get_last_24_product_n_received_messages_response.account_assistant_received_messages:
                # this is the value of our ordered dict
                conversation_message = ConversationMessage(
                    is_message_entity_account_assistant=True, is_message_sent=False,
                    account_assistant_received_message=account_assistant_received_message)
                # this is the key of our ordered dict
                conversation_message_time = account_assistant_received_message.received_at.ToDatetime()
                # we create our ordered dict to sort message
                # in order with latest message first
                conversations_messages_ordered_dict[conversation_message_time] = conversation_message
            # stream all the sent messages
            get_last_24_product_n_sent_messages_request = GetLast24ProductNSentMessagesRequest(
                access_auth_details=request.access_auth_details,
                product_n=request.product_n,
                message_entity_enum=request.message_entity_enum,
                connected_account_assistant=request.connected_account_assistant,
                connected_account=request.connected_account
            )
            get_last_24_product_n_sent_messages_response = ApplicationContext.send_account_message_service_stub().GetLast24ProductNSentMessages(
                get_last_24_product_n_sent_messages_request)
            for account_sent_message in get_last_24_product_n_sent_messages_response.account_sent_messages:
                # this is the value of our ordered dict
                conversation_message = ConversationMessage(
                    is_message_entity_account_assistant=False, is_message_sent=True,
                    account_sent_message=account_sent_message)
                # this is the key of our ordered dict
                conversation_message_time = account_sent_message.sent_at.ToDatetime()
                # we create our ordered dict to sort message
                # in order with latest message first
                conversations_messages_ordered_dict[conversation_message_time] = conversation_message
            for account_assistant_sent_message in get_last_24_product_n_sent_messages_response.account_assistant_sent_messages:
                # this is the value of our ordered dict
                conversation_message = ConversationMessage(
                    is_message_entity_account_assistant=True, is_message_sent=True,
                    account_assistant_sent_message=account_assistant_sent_message)
                # this is the key of our ordered dict
                conversation_message_time = account_assistant_sent_message.sent_at.ToDatetime()
                # we create our ordered dict to sort message
                # in order with latest message first
                conversations_messages_ordered_dict[conversation_message_time] = conversation_message
            return GetLast24ProductNConversationMessagesResponse(
                response_meta=response_meta,
                conversation_messages=list(collections.OrderedDict(
                    sorted(conversations_messages_ordered_dict.items(), reverse=True)).values())
            )

    @trace_rpc()
    def GetAccountLastMessage(self, request, context):
        logging.info("MessageConversationService:GetAccountLastMessage")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetAccountLastMessageResponse(response_meta=response_meta)
        else:
            last_account_received_message = ApplicationContext.receive_account_message_service_stub().GetAccountLastReceivedMessage(
                GetAccountLastReceivedMessageRequest(
                    access_auth_details=request.access_auth_details,
                    connected_account_id=request.connected_account_id,
                )
            ).last_received_message
            last_account_sent_message = ApplicationContext.send_account_message_service_stub().GetAccountLastSentMessage(
                GetAccountLastSentMessageRequest(
                    access_auth_details=request.access_auth_details,
                    connected_account_id=request.connected_account_id,
                )
            ).last_sent_message
            if last_account_received_message.received_at.seconds > last_account_sent_message.sent_at.seconds:
                return GetAccountLastMessageResponse(
                    response_meta=response_meta,
                    is_message_sent=False,
                    account_received_message=last_account_received_message
                )
            else:
                return GetAccountLastMessageResponse(
                    response_meta=response_meta,
                    is_message_sent=True,
                    account_sent_message=last_account_sent_message
                )

    @trace_rpc()
    def GetAccountAssistantLastMessage(self, request, context):
        logging.info("MessageConversationService:GetAccountAssistantLastMessage")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetAccountAssistantLastMessageResponse(response_meta=response_meta)
        else:
            last_account_assistant_received_message = ApplicationContext.receive_account_message_service_stub().GetAccountAssistantLastReceivedMessage(
                GetAccountAssistantLastReceivedMessageRequest(
                    access_auth_details=request.access_auth_details,
                    connected_account_assistant_id=request.connected_account_assistant_id,
                )
            ).last_received_message
            last_account_assistant_sent_message = ApplicationContext.send_account_message_service_stub().GetAccountAssistantLastSentMessage(
                GetAccountAssistantLastSentMessageRequest(
                    access_auth_details=request.access_auth_details,
                    connected_account_assistant_id=request.connected_account_assistant_id,
                )
            ).last_sent_message
            if last_account_assistant_received_message.received_at.seconds > last_account_assistant_sent_message.sent_at.seconds:
                return GetAccountAssistantLastMessageResponse(
                    response_meta=response_meta,
                    is_message_sent=False,
                    account_assistant_received_message=last_account_assistant_received_message
                )
            else:
                return GetAccountAssistantLastMessageResponse(
                    response_meta=response_meta,
                    is_message_sent=True,
                    account_assistant_sent_message=last_account_assistant_sent_message
                )

    @trace_rpc()
    def GetConversedAccounts(self, request, context):
        logging.info("MessageConversationService:GetConversedAccounts")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetConversedAccountsResponse(response_meta=response_meta)
        else:
            received_messages_accounts = ApplicationContext.receive_account_message_service_stub(
            ).GetReceivedMessagesAccounts(request).received_messages_accounts
            sent_messages_accounts = ApplicationContext.send_account_message_service_stub(
            ).GetSentMessagesAccounts(request).sent_messages_accounts
            list_of_accounts = []
            list_of_account_ids = []
            for received_messages_account in received_messages_accounts:
                if received_messages_account.account_id not in list_of_account_ids:
                    list_of_account_ids.append(received_messages_account.account_id)
                    list_of_accounts.append(received_messages_account)
            for sent_messages_account in sent_messages_accounts:
                if sent_messages_account.account_id not in list_of_account_ids:
                    list_of_account_ids.append(sent_messages_account.account_id)
                    list_of_accounts.append(sent_messages_account)
            return GetConversedAccountsResponse(response_meta=response_meta, conversed_accounts=list_of_accounts)

    @trace_rpc()
    def GetConversedAccountAssistants(self, request, context):
        logging.info("MessageConversationService:GetConversedAccountAssistants")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetConversedAccountAssistantsResponse(response_meta=response_meta)
        else:
            received_messages_account_assistants = ApplicationContext.receive_account_message_service_stub(
            ).GetReceivedMessagesAccountAssistants(request).received_messages_account_assistants
            sent_messages_account_assistants = ApplicationContext.send_account_message_service_stub(
            ).GetSentMessagesAccountAssistants(request).sent_messages_account_assistants
            list_of_account_assistants = []
            list_of_account_assistant_ids = []
            for received_messages_account_assistant in received_messages_account_assistants:
                if received_messages_account_assistant.account_assistant_id not in list_of_account_assistant_ids:
                    list_of_account_assistant_ids.append(received_messages_account_assistant.account_assistant_id)
                    list_of_account_assistants.append(received_messages_account_assistant)
            for sent_messages_account_assistant in sent_messages_account_assistants:
                if sent_messages_account_assistant.account_assistant_id not in list_of_account_assistant_ids:
                    list_of_account_assistant_ids.append(sent_messages_account_assistant.account_assistant_id)
                    list_of_account_assistants.append(sent_messages_account_assistant)
            return GetConversedAccountAssistantsResponse(response_meta=response_meta,
                                                         conversed_account_assistants=list_of_account_assistants)

    @trace_rpc()
    def GetConversedAccountAndAssistants(self, request, context):
        logging.info("MessageConversationService:GetConversedAccountAndAssistants")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetConversedAccountAndAssistantsResponse(response_meta=response_meta)
        else:
            # Get all the conversed entities
            conversed_accounts = ApplicationContext.message_conversation_service_stub().GetConversedAccounts(
                request).conversed_accounts
            conversed_account_assistants = ApplicationContext.message_conversation_service_stub().GetConversedAccountAssistants(
                request).conversed_account_assistants
            list_of_conversed_entity_with_last_conversation_message = []
            # Get last message for all conversed accounts
            for conversed_account in conversed_accounts:
                response = ApplicationContext.message_conversation_service_stub().GetAccountLastMessage(
                    GetAccountLastMessageRequest(
                        access_auth_details=request,
                        connected_account_id=conversed_account.account_id
                    ))
                # Add dict of params to list
                list_of_conversed_entity_with_last_conversation_message.append({
                    "entity_type": "account",
                    "entity": conversed_account,
                    "is_message_sent": response.is_message_sent,
                    "last_conversed_message": response.account_sent_message if response.is_message_sent else response.account_received_message,
                    "last_conversed_time": response.account_sent_message.sent_at if response.is_message_sent else response.account_received_message.received_at,
                })
            # Get last message for all conversed account assistants
            for conversed_account_assistant in conversed_account_assistants:
                response = ApplicationContext.message_conversation_service_stub().GetAccountAssistantLastMessage(
                    GetAccountAssistantLastMessageRequest(
                        access_auth_details=request,
                        connected_account_assistant_id=conversed_account_assistant.account_assistant_id
                    )
                )
                # Add dict of params to list
                list_of_conversed_entity_with_last_conversation_message.append({
                    "entity_type": "account_assistant",
                    "entity": conversed_account_assistant,
                    "is_message_sent": response.is_message_sent,
                    "last_conversed_message": response.account_assistant_sent_message if response.is_message_sent else response.account_assistant_received_message,
                    "last_conversed_time": response.account_assistant_sent_message.sent_at if response.is_message_sent else response.account_assistant_received_message.received_at,
                })
            # Sort the list
            sorted_list_of_conversed_entity_with_last_conversation_message = sorted(
                list_of_conversed_entity_with_last_conversation_message,
                key=lambda conversed_entity_with_last_conversation_message:
                conversed_entity_with_last_conversation_message['last_conversed_time'].seconds, reverse=True)
            # create the response messages
            conversed_entity_with_last_conversation_messages = []
            for conversed_entity_with_last_conversation_message in sorted_list_of_conversed_entity_with_last_conversation_message:
                if conversed_entity_with_last_conversation_message['entity_type'] == "account":
                    if conversed_entity_with_last_conversation_message["is_message_sent"]:
                        conversed_entity_with_last_conversation_messages.append(
                            ConversedEntityWithLastConversationMessage(
                                conversed_account=conversed_entity_with_last_conversation_message["entity"],
                                last_conversation_message=ConversationMessage(
                                    is_message_entity_account_assistant=False,
                                    is_message_sent=True,
                                    account_sent_message=conversed_entity_with_last_conversation_message[
                                        "last_conversed_message"]
                                )
                            ))
                    else:
                        conversed_entity_with_last_conversation_messages.append(
                            ConversedEntityWithLastConversationMessage(
                                conversed_account=conversed_entity_with_last_conversation_message["entity"],
                                last_conversation_message=ConversationMessage(
                                    is_message_entity_account_assistant=False,
                                    is_message_sent=False,
                                    account_received_message=conversed_entity_with_last_conversation_message[
                                        "last_conversed_message"]
                                )
                            ))
                else:
                    if conversed_entity_with_last_conversation_message["is_message_sent"]:
                        conversed_entity_with_last_conversation_messages.append(
                            ConversedEntityWithLastConversationMessage(
                                conversed_account_assistant=conversed_entity_with_last_conversation_message["entity"],
                                last_conversation_message=ConversationMessage(
                                    is_message_entity_account_assistant=True,
                                    is_message_sent=True,
                                    account_assistant_sent_message=conversed_entity_with_last_conversation_message[
                                        "last_conversed_message"]
                                )
                            ))
                    else:
                        conversed_entity_with_last_conversation_messages.append(
                            ConversedEntityWithLastConversationMessage(
                                conversed_account_assistant=conversed_entity_with_last_conversation_message["entity"],
                                last_conversation_message=ConversationMessage(
                                    is_message_entity_account_assistant=True,
                                    is_message_sent=False,
                                    account_assistant_received_message=conversed_entity_with_last_conversation_message[
                                        "last_conversed_message"]
                                )
                            ))

            return GetConversedAccountAndAssistantsResponse(
                response_meta=response_meta,
                conversed_entity_with_last_conversation_message=conversed_entity_with_last_conversation_messages
            )
