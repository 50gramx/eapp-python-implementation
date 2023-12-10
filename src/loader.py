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
import os

import grpc
from ethos.elint.services.product.action.space_knowledge_action_pb2_grpc import SpaceKnowledgeActionServiceStub
from ethos.elint.services.product.conversation.message.account.receive_account_message_pb2_grpc import \
    ReceiveAccountMessageServiceStub
from ethos.elint.services.product.conversation.message.account.send_account_message_pb2_grpc import \
    SendAccountMessageServiceStub
from ethos.elint.services.product.conversation.message.account_assistant.receive_account_assistant_message_pb2_grpc import \
    ReceiveAccountAssistantMessageServiceStub
from ethos.elint.services.product.conversation.message.account_assistant.send_account_assistant_message_pb2_grpc import \
    SendAccountAssistantMessageServiceStub
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

from community.gramx.fifty.zero.ethos.conversations.entities.message.capabilities.account.registry import \
    register_account_message_services
from community.gramx.fifty.zero.ethos.conversations.entities.message.capabilities.account_assistant.registry import \
    register_account_assistant_message_services
from community.gramx.fifty.zero.ethos.conversations.entities.message.registry import \
    register_message_conversation_services
from community.gramx.fifty.zero.ethos.identity.entities.account.registry import register_account_services
from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.registry import \
    register_account_assistant_services
from community.gramx.fifty.zero.ethos.identity.entities.machine.discover_machine_service import DiscoverMachineService
from community.gramx.fifty.zero.ethos.identity.entities.space.registry import register_space_services
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge.registry import \
    register_space_knowledge_services
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.registry import \
    register_space_knowledge_domain_services
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file.registry import \
    register_space_knowledge_domain_file_services
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page.registry import \
    register_space_knowledge_domain_file_page_services
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page_para.registry import \
    register_space_knowledge_domain_file_page_para_services
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
        register_account_services()
        register_account_assistant_services()
        register_space_services()
        # Loader.__register_multiverse_services()
        Loader.__register_machine_services()
        logging.info(f'Identity context loaded')
        return

    @staticmethod
    def init_multiverse_conversations_context():
        register_message_conversation_services()
        register_account_message_services()
        register_account_assistant_message_services()
        logging.info(f'Conversations context loaded')
        return

    @staticmethod
    def init_multiverse_knowledge_spaces_context():
        register_space_knowledge_services()
        register_space_knowledge_domain_services()
        register_space_knowledge_domain_file_services()
        register_space_knowledge_domain_file_page_services()
        register_space_knowledge_domain_file_page_para_services()
        logging.info(f'Knowledge Spaces context loaded')
        pass

    @staticmethod
    def __init_service_stubs():
        channels = []

        # ------------------------------------
        # IDENTITY STUBS
        # ------------------------------------
        grpc_host = os.environ['ERPC_HOST']
        grpc_port = os.environ['ERPC_PORT']
        # grpc_certificate_file = os.environ['EAPP_SERVICE_IDENTITY_COMMON_GRPC_EXTERNAL_CERTIFICATE_FILE']

        host_ip = "{host}:{port}".format(host=grpc_host, port=grpc_port)

        # ssl_credentials = grpc.ssl_channel_credentials(open(grpc_certificate_file, 'rb').read())
        capabilities_common_channel = grpc.insecure_channel(host_ip)

        capabilities_common_channel = grpc.intercept_channel(capabilities_common_channel)
        channels.append(capabilities_common_channel)

        access_account_service_stub = AccessAccountServiceStub(capabilities_common_channel)
        Registry.register_service('access_account_service_stub', access_account_service_stub)
        create_account_service_stub = CreateAccountServiceStub(capabilities_common_channel)
        Registry.register_service('create_account_service_stub', create_account_service_stub)
        discover_account_service_stub = DiscoverAccountServiceStub(capabilities_common_channel)
        Registry.register_service('discover_account_service_stub', discover_account_service_stub)
        connect_account_service_stub = ConnectAccountServiceStub(capabilities_common_channel)
        Registry.register_service('connect_account_service_stub', connect_account_service_stub)
        notify_account_service_stub = NotifyAccountServiceStub(capabilities_common_channel)
        Registry.register_service('notify_account_service_stub', notify_account_service_stub)
        pay_in_account_service_stub = PayInAccountServiceStub(capabilities_common_channel)
        Registry.register_service('pay_in_account_service_stub', pay_in_account_service_stub)

        access_space_service_stub = AccessSpaceServiceStub(capabilities_common_channel)
        Registry.register_service('access_space_service_stub', access_space_service_stub)
        create_space_service_stub = CreateSpaceServiceStub(capabilities_common_channel)
        Registry.register_service('create_space_service_stub', create_space_service_stub)

        access_account_assistant_service_stub = AccessAccountAssistantServiceStub(capabilities_common_channel)
        Registry.register_service('access_account_assistant_service_stub', access_account_assistant_service_stub)
        create_account_assistant_service_stub = CreateAccountAssistantServiceStub(capabilities_common_channel)
        Registry.register_service('create_account_assistant_service_stub', create_account_assistant_service_stub)
        discover_account_assistant_service_stub = DiscoverAccountAssistantServiceStub(capabilities_common_channel)
        Registry.register_service('discover_account_assistant_service_stub', discover_account_assistant_service_stub)
        connect_account_assistant_service_stub = ConnectAccountAssistantServiceStub(capabilities_common_channel)
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

        # message conversation stubs
        message_conversation_service_stub = MessageConversationServiceStub(capabilities_common_channel)
        Registry.register_service('message_conversation_service_stub', message_conversation_service_stub)

        # account message stubs
        send_account_message_service_stub = SendAccountMessageServiceStub(capabilities_common_channel)
        Registry.register_service('send_account_message_service_stub', send_account_message_service_stub)

        receive_account_message_service_stub = ReceiveAccountMessageServiceStub(capabilities_common_channel)
        Registry.register_service('receive_account_message_service_stub', receive_account_message_service_stub)

        # account assistant message stubs
        send_account_assistant_message_service_stub = SendAccountAssistantMessageServiceStub(
            capabilities_common_channel)
        Registry.register_service(
            'send_account_assistant_message_service_stub', send_account_assistant_message_service_stub)

        receive_account_assistant_message_service_stub = ReceiveAccountAssistantMessageServiceStub(
            capabilities_common_channel)
        Registry.register_service(
            'receive_account_assistant_message_service_stub', receive_account_assistant_message_service_stub)

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
    def __register_machine_services():
        discover_machine_service = DiscoverMachineService()
        Registry.register_service('discover_machine_service', discover_machine_service)
        return
