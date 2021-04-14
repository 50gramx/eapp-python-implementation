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
    SendAccountAssistantMessageServiceStub
from ethos.elint.services.product.conversation.message.message_conversation_pb2_grpc import \
    MessageConversationServiceStub
from ethos.elint.services.product.identity.account.access_account_pb2_grpc import AccessAccountServiceStub
from ethos.elint.services.product.identity.account.connect_account_pb2_grpc import ConnectAccountServiceStub
from ethos.elint.services.product.identity.account.discover_account_pb2_grpc import DiscoverAccountServiceStub
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
from service.account.access_account_service import AccessAccountService
from service.account.connect_account_service import ConnectAccountService
from service.account.create_account_service import CreateAccountService
from service.account.discover_account_service import DiscoverAccountService
from service.account.notify_account_service import NotifyAccountService
from service.account_assistant.access_account_assistant_service import AccessAccountAssistantService
from service.account_assistant.action_account_assistant_service import ActionAccountAssistantService
from service.account_assistant.connect_account_assistant_service import ConnectAccountAssistantService
from service.account_assistant.create_account_assistant_service import CreateAccountAssistantService
from service.account_assistant.discover_account_assistant_service import DiscoverAccountAssistantService
from service.space.access_space_service import AccessSpaceService
from service.space.create_space_service import CreateSpaceService
from support.application.registry import Registry


class Loader(object):

    @staticmethod
    def init_identity_context(app_root_path: str):
        Loader.__init_service_stubs()
        Loader.__init_services(app_root_path)
        return

    @staticmethod
    def __init_service_stubs():
        channels = []

        # ------------------------------------
        # IDENTITY STUBS
        # ------------------------------------
        # grpc_secured = os.environ["EAPP_SERVICE_PRODUCT_COMMON_GRPC_EXTERNAL_SECURE"]
        grpc_host = os.environ['EAPP_SERVICE_IDENTITY_HOST']
        grpc_port = os.environ['EAPP_SERVICE_IDENTITY_PORT']
        # grpc_certificate_file = os.environ['EAPP_SERVICE_PRODUCT_COMMON_GRPC_EXTERNAL_CERTIFICATE_FILE']

        host_ip = "{host}:{port}".format(host=grpc_host, port=grpc_port)

        # if grpc_secured == "true":
        #     # ssl_credentials = grpc.ssl_channel_credentials(open(grpc_certificate_file, 'rb').read())
        #     # product_common_channel = grpc.secure_channel(host_ip, ssl_credentials)
        #     pass
        # else:
        identity_common_channel = grpc.insecure_channel(host_ip)

        identity_common_channel = grpc.intercept_channel(identity_common_channel)
        channels.append(identity_common_channel)

        access_account_service_stub = AccessAccountServiceStub(identity_common_channel)
        Registry.register_service('access_account_service_stub', access_account_service_stub)
        discover_account_service_stub = DiscoverAccountServiceStub(identity_common_channel)
        Registry.register_service('discover_account_service_stub', discover_account_service_stub)
        connect_account_service_stub = ConnectAccountServiceStub(identity_common_channel)
        Registry.register_service('connect_account_service_stub', connect_account_service_stub)

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

        action_host_ip = "{host}:{port}".format(host=action_grpc_host, port=action_grpc_port)
        action_common_channel = grpc.insecure_channel(action_host_ip)
        action_common_channel = grpc.intercept_channel(action_common_channel)
        channels.append(action_common_channel)

        space_knowledge_action_service_stub = SpaceKnowledgeActionServiceStub(action_common_channel)
        Registry.register_service('space_knowledge_action_service_stub', space_knowledge_action_service_stub)

        # ------------------------------------
        # CONVERSATION STUBS
        # ------------------------------------
        conversation_grpc_host = os.environ['EAPP_SERVICE_CONVERSATION_HOST']
        conversation_grpc_port = os.environ['EAPP_SERVICE_CONVERSATION_PORT']

        conversation_host_ip = "{host}:{port}".format(host=conversation_grpc_host, port=conversation_grpc_port)
        conversation_common_channel = grpc.insecure_channel(conversation_host_ip)
        conversation_common_channel = grpc.intercept_channel(conversation_common_channel)
        channels.append(conversation_common_channel)

        # message conversation stubs
        message_conversation_service_stub = MessageConversationServiceStub(conversation_common_channel)
        Registry.register_service('message_conversation_service_stub', message_conversation_service_stub)

        send_account_assistant_message_service_stub = SendAccountAssistantMessageServiceStub(
            conversation_common_channel)
        Registry.register_service('send_account_assistant_message_service_stub',
                                  send_account_assistant_message_service_stub)

        Registry.register_service('grpc_channels', channels)
        return

    @staticmethod
    def __init_services(app_root_path: str):
        create_account_service = CreateAccountService()
        Registry.register_service('create_account_service', create_account_service)
        access_account_service = AccessAccountService()
        Registry.register_service('access_account_service', access_account_service)
        connect_account_service = ConnectAccountService()
        Registry.register_service('connect_account_service', connect_account_service)
        discover_account_service = DiscoverAccountService()
        Registry.register_service('discover_account_service', discover_account_service)

        access_space_service = AccessSpaceService()
        Registry.register_service('access_space_service', access_space_service)
        create_space_service = CreateSpaceService()
        Registry.register_service('create_space_service', create_space_service)

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

        notify_account_service = NotifyAccountService()
        Registry.register_service('notify_account_service', notify_account_service)
