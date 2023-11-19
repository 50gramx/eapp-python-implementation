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

import os

import grpc
from ethos.elint.services.product.action.space_knowledge_action_pb2_grpc import SpaceKnowledgeActionServiceStub
from ethos.elint.services.product.conversation.message.account_assistant.send_account_assistant_message_pb2_grpc import \
    SendAccountAssistantMessageServiceStub, SendAccountAssistantMessageService
from ethos.elint.services.product.conversation.message.message_conversation_pb2_grpc import \
    MessageConversationServiceStub
from ethos.elint.services.product.identity.account.access_account_pb2_grpc import AccessAccountServiceStub
from ethos.elint.services.product.identity.account.connect_account_pb2_grpc import ConnectAccountServiceStub
from ethos.elint.services.product.identity.account.create_account_pb2_grpc import CreateAccountServiceStub
from ethos.elint.services.product.identity.account.discover_account_pb2_grpc import DiscoverAccountServiceStub
from ethos.elint.services.product.identity.account.notify_account_pb2_grpc import NotifyAccountServiceStub
from ethos.elint.services.product.identity.account.pay_in_account_pb2_grpc import PayInAccountServiceStub
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2_grpc import \
    AccessAccountAssistantServiceStub
from ethos.elint.services.product.identity.account_assistant.connect_account_assistant_pb2_grpc import \
    ConnectAccountAssistantServiceStub
from ethos.elint.services.product.identity.account_assistant.create_account_assistant_pb2_grpc import \
    CreateAccountAssistantServiceStub
from ethos.elint.services.product.identity.account_assistant.discover_account_assistant_pb2_grpc import \
    DiscoverAccountAssistantServiceStub
from ethos.elint.services.product.identity.space.access_space_pb2_grpc import AccessSpaceServiceStub
from ethos.elint.services.product.identity.space.create_space_pb2_grpc import CreateSpaceServiceStub
from ethos.elint.services.product.knowledge.space_knowledge.access_space_knowledge_pb2_grpc import \
    AccessSpaceKnowledgeServiceStub

from community.gramx.fifty.zero.ethos.conversations.entities.message.account.receive_account_message_service import \
    ReceiveAccountMessageService
from community.gramx.fifty.zero.ethos.conversations.entities.message.account.send_account_message_service import \
    SendAccountMessageService
from community.gramx.fifty.zero.ethos.conversations.entities.message.account_assistant.receive_account_assistant_message_service import \
    ReceiveAccountAssistantMessageService
from community.gramx.fifty.zero.ethos.conversations.entities.message.message_conversation_service import \
    MessageConversationService
from community.gramx.fifty.zero.ethos.identity.entities.account.capabilities.access_account_service import \
    AccessAccountService
from community.gramx.fifty.zero.ethos.identity.entities.account.capabilities.connect_account_service import \
    ConnectAccountService
from community.gramx.fifty.zero.ethos.identity.entities.account.capabilities.create_account_service import \
    CreateAccountService
from community.gramx.fifty.zero.ethos.identity.entities.account.capabilities.discover_account_service import \
    DiscoverAccountService
from community.gramx.fifty.zero.ethos.identity.entities.account.capabilities.notify_account_service import \
    NotifyAccountService
from community.gramx.fifty.zero.ethos.identity.entities.account.capabilities.pay_in_account_service import \
    PayInAccountService
from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.capabilities.access_account_assistant_service import \
    AccessAccountAssistantService
from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.capabilities.action_account_assistant_service import \
    ActionAccountAssistantService
from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.capabilities.connect_account_assistant_service import \
    ConnectAccountAssistantService
from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.capabilities.create_account_assistant_service import \
    CreateAccountAssistantService
from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.capabilities.discover_account_assistant_service import \
    DiscoverAccountAssistantService
from community.gramx.fifty.zero.ethos.identity.entities.machine.discover_machine_service import DiscoverMachineService
from community.gramx.fifty.zero.ethos.identity.entities.space.capabilities.access_space_service import \
    AccessSpaceService
from community.gramx.fifty.zero.ethos.identity.entities.space.capabilities.create_space_service import \
    CreateSpaceService
from support.application.registry import Registry


class Loader(object):

    @staticmethod
    def init_universe_context(universe_id: str):
        Loader.__init_service_stubs()
        return

    @staticmethod
    def init_galaxy_context(galaxy_id: str):
        Loader.__init_service_stubs()
        Loader.__register_space_services()
        return

    @staticmethod
    def init_multiverse_identity_context():
        # Loader.__init_multiverse_identity_chain_stubs()
        Loader.__init_service_stubs()
        Loader.__register_account_services()
        Loader.__register_account_assistant_services()
        Loader.__register_space_services()  # for now, change later
        # Loader.__register_multiverse_services()
        Loader.__register_machine_services()
        return

    @staticmethod
    def init_multiverse_conversations_context():
        Loader.__register_message_conversation_services()
        Loader.__register_account_message_services()
        Loader.__register_account_assistant_message_services()
        return

    @staticmethod
    def __init_service_stubs():
        channels = []

        # ------------------------------------
        # IDENTITY STUBS
        # ------------------------------------
        grpc_host = os.environ['EAPP_SERVICE_IDENTITY_HOST']
        grpc_port = os.environ['EAPP_SERVICE_IDENTITY_PORT']
        grpc_certificate_file = os.environ['EAPP_SERVICE_IDENTITY_COMMON_GRPC_EXTERNAL_CERTIFICATE_FILE']

        host_ip = "{host}:{port}".format(host=grpc_host, port=grpc_port)

        ssl_credentials = grpc.ssl_channel_credentials(open(grpc_certificate_file, 'rb').read())
        identity_common_channel = grpc.secure_channel(host_ip, ssl_credentials)

        identity_common_channel = grpc.intercept_channel(identity_common_channel)
        channels.append(identity_common_channel)

        access_account_service_stub = AccessAccountServiceStub(identity_common_channel)
        Registry.register_service('access_account_service_stub', access_account_service_stub)
        create_account_service_stub = CreateAccountServiceStub(identity_common_channel)
        Registry.register_service('create_account_service_stub', create_account_service_stub)
        discover_account_service_stub = DiscoverAccountServiceStub(identity_common_channel)
        Registry.register_service('discover_account_service_stub', discover_account_service_stub)
        connect_account_service_stub = ConnectAccountServiceStub(identity_common_channel)
        Registry.register_service('connect_account_service_stub', connect_account_service_stub)
        notify_account_service_stub = NotifyAccountServiceStub(identity_common_channel)
        Registry.register_service('notify_account_service_stub', notify_account_service_stub)
        pay_in_account_service_stub = PayInAccountServiceStub(identity_common_channel)
        Registry.register_service('pay_in_account_service_stub', pay_in_account_service_stub)

        access_space_service_stub = AccessSpaceServiceStub(identity_common_channel)
        Registry.register_service('access_space_service_stub', access_space_service_stub)
        create_space_service_stub = CreateSpaceServiceStub(identity_common_channel)
        Registry.register_service('create_space_service_stub', create_space_service_stub)

        access_account_assistant_service_stub = AccessAccountAssistantServiceStub(identity_common_channel)
        Registry.register_service('access_account_assistant_service_stub', access_account_assistant_service_stub)
        create_account_assistant_service_stub = CreateAccountAssistantServiceStub(identity_common_channel)
        Registry.register_service('create_account_assistant_service_stub', create_account_assistant_service_stub)
        discover_account_assistant_service_stub = DiscoverAccountAssistantServiceStub(identity_common_channel)
        Registry.register_service('discover_account_assistant_service_stub', discover_account_assistant_service_stub)
        connect_account_assistant_service_stub = ConnectAccountAssistantServiceStub(identity_common_channel)
        Registry.register_service('connect_account_assistant_service_stub', connect_account_assistant_service_stub)

        # ------------------------------------
        # ACTION STUBS
        # ------------------------------------
        action_grpc_host = os.environ['EAPP_SERVICE_ACTION_HOST']
        action_grpc_port = os.environ['EAPP_SERVICE_ACTION_PORT']
        action_grpc_certificate_file = os.environ[
            'EAPP_SERVICE_ACTION_COMMON_GRPC_EXTERNAL_CERTIFICATE_FILE']

        action_host_ip = "{host}:{port}".format(host=action_grpc_host, port=action_grpc_port)

        action_ssl_credentials = grpc.ssl_channel_credentials(
            open(action_grpc_certificate_file, 'rb').read())
        action_common_channel = grpc.secure_channel(action_host_ip, action_ssl_credentials)

        # action_common_channel = grpc.insecure_channel(action_host_ip)
        action_common_channel = grpc.intercept_channel(action_common_channel)
        channels.append(action_common_channel)

        space_knowledge_action_service_stub = SpaceKnowledgeActionServiceStub(action_common_channel)
        Registry.register_service('space_knowledge_action_service_stub', space_knowledge_action_service_stub)

        # ------------------------------------
        # CONVERSATION STUBS
        # ------------------------------------
        conversation_grpc_host = os.environ['EAPP_SERVICE_CONVERSATION_HOST']
        conversation_grpc_port = os.environ['EAPP_SERVICE_CONVERSATION_PORT']
        conversation_grpc_certificate_file = os.environ[
            'EAPP_SERVICE_CONVERSATION_COMMON_GRPC_EXTERNAL_CERTIFICATE_FILE']

        conversation_host_ip = "{host}:{port}".format(host=conversation_grpc_host, port=conversation_grpc_port)

        conversation_ssl_credentials = grpc.ssl_channel_credentials(
            open(conversation_grpc_certificate_file, 'rb').read())
        conversation_common_channel = grpc.secure_channel(conversation_host_ip, conversation_ssl_credentials)

        conversation_common_channel = grpc.intercept_channel(conversation_common_channel)
        channels.append(conversation_common_channel)

        # message conversation stubs
        message_conversation_service_stub = MessageConversationServiceStub(conversation_common_channel)
        Registry.register_service('message_conversation_service_stub', message_conversation_service_stub)

        send_account_assistant_message_service_stub = SendAccountAssistantMessageServiceStub(
            conversation_common_channel)
        Registry.register_service('send_account_assistant_message_service_stub',
                                  send_account_assistant_message_service_stub)

        # ------------------------------------
        # KNOWLEDGE STUBS
        # ------------------------------------
        knowledge_grpc_host = os.environ['EAPP_SERVICE_KNOWLEDGE_HOST']
        knowledge_grpc_port = os.environ['EAPP_SERVICE_KNOWLEDGE_PORT']
        knowledge_grpc_certificate_file = os.environ[
            'EAPP_SERVICE_KNOWLEDGE_COMMON_GRPC_EXTERNAL_CERTIFICATE_FILE']

        knowledge_host_ip = "{host}:{port}".format(host=knowledge_grpc_host, port=knowledge_grpc_port)

        knowledge_ssl_credentials = grpc.ssl_channel_credentials(
            open(knowledge_grpc_certificate_file, 'rb').read())
        knowledge_common_channel = grpc.secure_channel(knowledge_host_ip, knowledge_ssl_credentials)

        knowledge_common_channel = grpc.intercept_channel(knowledge_common_channel)
        channels.append(knowledge_common_channel)

        # knowledge stubs
        access_space_knowledge_service_stub = AccessSpaceKnowledgeServiceStub(knowledge_common_channel)
        Registry.register_service('access_space_knowledge_service_stub', access_space_knowledge_service_stub)

        # adding channels to registry
        Registry.register_service('grpc_channels', channels)
        return

    # ------------------------------------------------------
    # Identity Services
    # ------------------------------------------------------

    @staticmethod
    def __register_account_services():
        create_account_service = CreateAccountService()
        Registry.register_service('create_account_service', create_account_service)
        access_account_service = AccessAccountService()
        Registry.register_service('access_account_service', access_account_service)
        connect_account_service = ConnectAccountService()
        Registry.register_service('connect_account_service', connect_account_service)
        discover_account_service = DiscoverAccountService()
        Registry.register_service('discover_account_service', discover_account_service)
        pay_in_account_service = PayInAccountService()
        Registry.register_service('pay_in_account_service', pay_in_account_service)
        notify_account_service = NotifyAccountService()
        Registry.register_service('notify_account_service', notify_account_service)
        return

    @staticmethod
    def __register_account_assistant_services():
        access_account_assistant_service = AccessAccountAssistantService()
        Registry.register_service('access_account_assistant_service', access_account_assistant_service)
        create_account_assistant_service = CreateAccountAssistantService()
        Registry.register_service('create_account_assistant_service', create_account_assistant_service)
        connect_account_assistant_service = ConnectAccountAssistantService()
        Registry.register_service('connect_account_assistant_service', connect_account_assistant_service)
        discover_account_assistant_service = DiscoverAccountAssistantService()
        Registry.register_service('discover_account_assistant_service', discover_account_assistant_service)
        action_account_assistant_service = ActionAccountAssistantService()
        Registry.register_service('action_account_assistant_service', action_account_assistant_service)
        return

    @staticmethod
    def __register_space_services():
        access_space_service = AccessSpaceService()
        Registry.register_service('access_space_service', access_space_service)
        create_space_service = CreateSpaceService()
        Registry.register_service('create_space_service', create_space_service)
        return

    @staticmethod
    def __register_machine_services():
        discover_machine_service = DiscoverMachineService()
        Registry.register_service('discover_machine_service', discover_machine_service)
        return

    # ------------------------------------------------------
    # Conversations Services
    # ------------------------------------------------------

    @staticmethod
    def __register_message_conversation_services():
        message_conversation_service = MessageConversationService()
        Registry.register_service('message_conversation_service', message_conversation_service)

    @staticmethod
    def __register_account_message_services():
        send_account_message_service = SendAccountMessageService()
        Registry.register_service('send_account_message_service', send_account_message_service)
        receive_account_message_service = ReceiveAccountMessageService()
        Registry.register_service('receive_account_message_service', receive_account_message_service)

    @staticmethod
    def __register_account_assistant_message_services():
        send_account_assistant_message_service = SendAccountAssistantMessageService()
        Registry.register_service('send_account_assistant_message_service', send_account_assistant_message_service)
        receive_account_assistant_message_service = ReceiveAccountAssistantMessageService()
        Registry.register_service('receive_account_assistant_message_service',
                                  receive_account_assistant_message_service)
