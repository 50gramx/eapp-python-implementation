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
from ethos.elint.services.cognitive.assist.knowledge.reader_knowledge_pb2_grpc import (
    ReaderKnowledgeServiceStub,
)
from ethos.elint.services.cognitive.assist.knowledge.retriever_knowledge_pb2_grpc import (
    RetrieverKnowledgeServiceStub,
)
from ethos.elint.services.product.action.space_knowledge_action_pb2_grpc import (
    SpaceKnowledgeActionServiceStub,
)
from ethos.elint.services.product.conversation.message.account.receive_account_message_pb2_grpc import (
    ReceiveAccountMessageServiceStub,
)
from ethos.elint.services.product.conversation.message.account.send_account_message_pb2_grpc import (
    SendAccountMessageServiceStub,
)
from ethos.elint.services.product.conversation.message.account_assistant.receive_account_assistant_message_pb2_grpc import (
    ReceiveAccountAssistantMessageServiceStub,
)
from ethos.elint.services.product.conversation.message.account_assistant.send_account_assistant_message_pb2_grpc import (
    SendAccountAssistantMessageServiceStub,
)
from ethos.elint.services.product.conversation.message.message_conversation_pb2_grpc import (
    MessageConversationServiceStub,
)
from ethos.elint.services.product.identity.account.access_account_pb2_grpc import (
    AccessAccountServiceStub,
)
from ethos.elint.services.product.identity.account.connect_account_pb2_grpc import (
    ConnectAccountServiceStub,
)
from ethos.elint.services.product.identity.account.create_account_pb2_grpc import (
    CreateAccountServiceStub,
)
from ethos.elint.services.product.identity.account.discover_account_pb2_grpc import (
    DiscoverAccountServiceStub,
)
from ethos.elint.services.product.identity.account.notify_account_pb2_grpc import (
    NotifyAccountServiceStub,
)
from ethos.elint.services.product.identity.account.pay_in_account_pb2_grpc import (
    PayInAccountServiceStub,
)
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2_grpc import (
    AccessAccountAssistantServiceStub,
)
from ethos.elint.services.product.identity.account_assistant.action_account_assistant_pb2_grpc import (
    ActionAccountAssistantServiceStub,
)
from ethos.elint.services.product.identity.account_assistant.connect_account_assistant_pb2_grpc import (
    ConnectAccountAssistantServiceStub,
)
from ethos.elint.services.product.identity.account_assistant.create_account_assistant_pb2_grpc import (
    CreateAccountAssistantServiceStub,
)
from ethos.elint.services.product.identity.account_assistant.discover_account_assistant_pb2_grpc import (
    DiscoverAccountAssistantServiceStub,
)
from ethos.elint.services.product.identity.pods.create_pods_pb2_grpc import (
    CreatePodsServiceStub,
)
from ethos.elint.services.product.identity.space.access_space_pb2_grpc import (
    AccessSpaceServiceStub,
)
from ethos.elint.services.product.identity.space.create_space_pb2_grpc import (
    CreateSpaceServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge.access_space_knowledge_pb2_grpc import (
    AccessSpaceKnowledgeServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge.create_space_knowledge_pb2_grpc import (
    CreateSpaceKnowledgeServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge.discover_space_knowledge_pb2_grpc import (
    DiscoverSpaceKnowledgeServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2_grpc import (
    AccessSpaceKnowledgeDomainServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain.create_space_knowledge_domain_pb2_grpc import (
    CreateSpaceKnowledgeDomainServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain.discover_space_knowledge_domain_pb2_grpc import (
    DiscoverSpaceKnowledgeDomainServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file.access_space_knowledge_domain_file_pb2_grpc import (
    AccessSpaceKnowledgeDomainFileServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file.create_space_knowledge_domain_file_pb2_grpc import (
    CreateSpaceKnowledgeDomainFileServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file.delete_space_knowledge_domain_file_pb2_grpc import (
    DeleteSpaceKnowledgeDomainFileServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.access_space_knowledge_domain_file_page_pb2_grpc import (
    AccessSpaceKnowledgeDomainFilePageServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.create_space_knowledge_domain_file_page_pb2_grpc import (
    CreateSpaceKnowledgeDomainFilePageServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.delete_space_knowledge_domain_file_page_pb2_grpc import (
    DeleteSpaceKnowledgeDomainFilePageServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.discover_space_knowledge_domain_file_page_pb2_grpc import (
    DiscoverSpaceKnowledgeDomainFilePageServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page_para.access_space_knowledge_domain_file_page_para_pb2_grpc import (
    AccessSpaceKnowledgeDomainFilePageParaServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page_para.create_space_knowledge_domain_file_page_para_pb2_grpc import (
    CreateSpaceKnowledgeDomainFilePageParaServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page_para.delete_space_knowledge_domain_file_page_para_pb2_grpc import (
    DeleteSpaceKnowledgeDomainFilePageParaServiceStub,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page_para.discover_space_knowledge_domain_file_page_para_pb2_grpc import (
    DiscoverSpaceKnowledgeDomainFilePageParaServiceStub,
)

from community.gramx.fifty.zero.ethos.conversations.entities.message.capabilities.account.registry import (
    register_account_message_services,
)
from community.gramx.fifty.zero.ethos.conversations.entities.message.capabilities.account_assistant.registry import (
    register_account_assistant_message_services,
)
from community.gramx.fifty.zero.ethos.conversations.entities.message.registry import (
    register_message_conversation_services,
)
from community.gramx.fifty.zero.ethos.identity.entities.account.registry import (
    register_account_services,
)
from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.registry import (
    register_account_assistant_services,
)
from community.gramx.fifty.zero.ethos.identity.entities.machine.discover_machine_service import (
    DiscoverMachineService,
)
from community.gramx.fifty.zero.ethos.identity.entities.pods.registry import (
    register_pod_services,
)
from community.gramx.fifty.zero.ethos.identity.entities.space.registry import (
    register_space_services,
)
from community.gramx.fifty.zero.ethos.identity.entities.universe.registry import (
    register_universe_services,
)
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge.registry import (
    register_space_knowledge_services,
)
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.registry import (
    register_space_knowledge_domain_services,
)
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file.registry import (
    register_space_knowledge_domain_file_services,
)
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page.registry import (
    register_space_knowledge_domain_file_page_services,
)
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page_para.registry import (
    register_space_knowledge_domain_file_page_para_services,
)
from community.gramx.sixty.six.ethos.action.entities.space.knowledge.registry import (
    register_space_knowledge_action_services,
)
from community.gramx.sixty.six.ethos.reader.entities.knowledge.reader.registry import (
    register_knowledge_reader_services,
)
from community.gramx.sixty.six.ethos.retriever.entities.knowledge.registry import (
    register_knowledge_retriever_services,
)
from support.application.registry import Registry


class Loader(object):

    @staticmethod
    def init_multiverse_context():
        Loader.__init_service_stubs()
        return

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
    def init_multiverse_identity_context(aio: bool):
        logging.info(f"Identity context loading...")
        # Loader.__init_multiverse_identity_chain_stubs()
        register_universe_services(aio=aio)
        register_account_services(aio=aio)
        register_account_assistant_services(aio=aio)
        register_space_services(aio=aio)
        register_pod_services(aio=aio)
        logging.info("pods service registered")
        # Loader.__register_multiverse_services()
        Loader.__register_machine_services()
        logging.info(f"Identity context loaded")
        return

    @staticmethod
    def init_multiverse_conversations_context(aio: bool):
        logging.info(f"Conversations context loading...")
        register_message_conversation_services(aio=aio)
        register_account_message_services(aio=aio)
        register_account_assistant_message_services(aio=aio)
        logging.info(f"Conversations context loaded")
        return

    @staticmethod
    def init_multiverse_knowledge_spaces_context(aio: bool):
        logging.info(f"Knowledge Spaces context loading...")
        register_space_knowledge_services(aio=aio)
        register_space_knowledge_domain_services(aio=aio)
        register_space_knowledge_domain_file_services(aio=aio)
        register_space_knowledge_domain_file_page_services(aio=aio)
        register_space_knowledge_domain_file_page_para_services(aio=aio)
        logging.info(f"Knowledge Spaces context loaded")
        pass

    @staticmethod
    def init_multiverse_knowledge_retriever_context(aio: bool):
        logging.info(f"Knowledge Retriever context loading...")
        # register_knowledge_retriever_services(aio=aio)
        logging.info(f"Knowledge Retriever context loaded")
        pass

    @staticmethod
    def init_multiverse_knowledge_reader_context(aio: bool):
        logging.info(f"Knowledge Reader context loading...")
        register_knowledge_reader_services(aio=aio)
        logging.info(f"Knowledge Reader context loaded")
        pass

    @staticmethod
    def init_multiverse_space_knowledge_action_context(aio: bool):
        logging.info(f"Space Knowledge Action context loading...")
        register_space_knowledge_action_services(aio=aio)
        logging.info(f"Space Knowledge Action  context loaded")
        pass

    @staticmethod
    def __init_service_stubs():
        channels = []

        # ------------------------------------
        # IDENTITY STUBS
        # ------------------------------------
        grpc_host = os.environ["ERPC_HOST"]
        grpc_port = os.environ["ERPC_PORT"]
        # grpc_certificate_file = os.environ['EAPP_SERVICE_IDENTITY_COMMON_GRPC_EXTERNAL_CERTIFICATE_FILE']

        host_ip = "{host}:{port}".format(host=grpc_host, port=grpc_port)

        # ssl_credentials = grpc.ssl_channel_credentials(open(grpc_certificate_file, 'rb').read())
        capabilities_common_channel = grpc.insecure_channel(host_ip)

        capabilities_common_channel = grpc.intercept_channel(
            capabilities_common_channel
        )
        channels.append(capabilities_common_channel)

        access_account_service_stub = AccessAccountServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "access_account_service_stub", access_account_service_stub
        )
        create_account_service_stub = CreateAccountServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "create_account_service_stub", create_account_service_stub
        )
        discover_account_service_stub = DiscoverAccountServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "discover_account_service_stub", discover_account_service_stub
        )
        connect_account_service_stub = ConnectAccountServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "connect_account_service_stub", connect_account_service_stub
        )
        notify_account_service_stub = NotifyAccountServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "notify_account_service_stub", notify_account_service_stub
        )
        pay_in_account_service_stub = PayInAccountServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "pay_in_account_service_stub", pay_in_account_service_stub
        )

        access_space_service_stub = AccessSpaceServiceStub(capabilities_common_channel)
        Registry.register_service(
            "access_space_service_stub", access_space_service_stub
        )
        create_space_service_stub = CreateSpaceServiceStub(capabilities_common_channel)
        Registry.register_service(
            "create_space_service_stub", create_space_service_stub
        )

        access_account_assistant_service_stub = AccessAccountAssistantServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "access_account_assistant_service_stub",
            access_account_assistant_service_stub,
        )
        create_account_assistant_service_stub = CreateAccountAssistantServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "create_account_assistant_service_stub",
            create_account_assistant_service_stub,
        )
        discover_account_assistant_service_stub = DiscoverAccountAssistantServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "discover_account_assistant_service_stub",
            discover_account_assistant_service_stub,
        )
        connect_account_assistant_service_stub = ConnectAccountAssistantServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "connect_account_assistant_service_stub",
            connect_account_assistant_service_stub,
        )

        aio_grpc_host = os.environ["ERPC_AIO_HOST"]
        aio_grpc_port = os.environ["ERPC_AIO_PORT"]
        # grpc_certificate_file = os.environ['EAPP_SERVICE_IDENTITY_COMMON_GRPC_EXTERNAL_CERTIFICATE_FILE']

        aio_host_ip = "{host}:{port}".format(host=aio_grpc_host, port=aio_grpc_port)

        asynchronous_capabilities_common_channel = grpc.aio.insecure_channel(
            aio_host_ip
        )

        asynchronous_capabilities_common_channel = grpc.intercept_channel(
            asynchronous_capabilities_common_channel
        )
        channels.append(asynchronous_capabilities_common_channel)

        action_account_assistant_service_stub = ActionAccountAssistantServiceStub(
            asynchronous_capabilities_common_channel
        )
        Registry.register_service(
            "action_account_assistant_service_stub",
            action_account_assistant_service_stub,
        )

        # ------------------------------------
        # ACTION STUBS
        # ------------------------------------

        space_knowledge_action_service_stub = SpaceKnowledgeActionServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "space_knowledge_action_service_stub", space_knowledge_action_service_stub
        )

        # ------------------------------------
        # CONVERSATION STUBS
        # ------------------------------------

        # message conversation stubs
        message_conversation_service_stub = MessageConversationServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "message_conversation_service_stub", message_conversation_service_stub
        )

        # account message stubs
        send_account_message_service_stub = SendAccountMessageServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "send_account_message_service_stub", send_account_message_service_stub
        )

        receive_account_message_service_stub = ReceiveAccountMessageServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "receive_account_message_service_stub", receive_account_message_service_stub
        )

        # account assistant message stubs
        send_account_assistant_message_service_stub = (
            SendAccountAssistantMessageServiceStub(capabilities_common_channel)
        )
        Registry.register_service(
            "send_account_assistant_message_service_stub",
            send_account_assistant_message_service_stub,
        )

        receive_account_assistant_message_service_stub = (
            ReceiveAccountAssistantMessageServiceStub(capabilities_common_channel)
        )
        Registry.register_service(
            "receive_account_assistant_message_service_stub",
            receive_account_assistant_message_service_stub,
        )

        # ------------------------------------
        # KNOWLEDGE STUBS
        # ------------------------------------

        # SPACE KNOWLEDGE STUBS
        access_space_knowledge_service_stub = AccessSpaceKnowledgeServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "access_space_knowledge_service_stub", access_space_knowledge_service_stub
        )

        discover_space_knowledge_services_stub = DiscoverSpaceKnowledgeServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "discover_space_knowledge_services_stub",
            discover_space_knowledge_services_stub,
        )

        create_space_knowledge_service_stub = CreateSpaceKnowledgeServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "create_space_knowledge_service_stub", create_space_knowledge_service_stub
        )

        # DOMAIN STUBS
        create_space_knowledge_domain_service_stub = (
            CreateSpaceKnowledgeDomainServiceStub(capabilities_common_channel)
        )
        Registry.register_service(
            "create_space_knowledge_domain_service_stub",
            create_space_knowledge_domain_service_stub,
        )

        access_space_knowledge_domain_service_stub = (
            AccessSpaceKnowledgeDomainServiceStub(capabilities_common_channel)
        )
        Registry.register_service(
            "access_space_knowledge_domain_service_stub",
            access_space_knowledge_domain_service_stub,
        )

        discover_space_knowledge_domain_service_stub = (
            DiscoverSpaceKnowledgeDomainServiceStub(capabilities_common_channel)
        )
        Registry.register_service(
            "discover_space_knowledge_domain_service_stub",
            discover_space_knowledge_domain_service_stub,
        )

        # FILE STUBS
        create_space_knowledge_domain_file_service_stub = (
            CreateSpaceKnowledgeDomainFileServiceStub(capabilities_common_channel)
        )
        Registry.register_service(
            "create_space_knowledge_domain_file_service_stub",
            create_space_knowledge_domain_file_service_stub,
        )

        access_space_knowledge_domain_file_service_stub = (
            AccessSpaceKnowledgeDomainFileServiceStub(capabilities_common_channel)
        )
        Registry.register_service(
            "access_space_knowledge_domain_file_service_stub",
            access_space_knowledge_domain_file_service_stub,
        )

        delete_space_knowledge_domain_file_service_stub = (
            DeleteSpaceKnowledgeDomainFileServiceStub(capabilities_common_channel)
        )
        Registry.register_service(
            "delete_space_knowledge_domain_file_service_stub",
            delete_space_knowledge_domain_file_service_stub,
        )

        # PAGE STUBS
        create_space_knowledge_domain_file_page_service_stub = (
            CreateSpaceKnowledgeDomainFilePageServiceStub(
                asynchronous_capabilities_common_channel
            )
        )
        Registry.register_service(
            "create_space_knowledge_domain_file_page_service_stub",
            create_space_knowledge_domain_file_page_service_stub,
        )

        access_space_knowledge_domain_file_page_service_stub = (
            AccessSpaceKnowledgeDomainFilePageServiceStub(capabilities_common_channel)
        )
        Registry.register_service(
            "access_space_knowledge_domain_file_page_service_stub",
            access_space_knowledge_domain_file_page_service_stub,
        )

        discover_space_knowledge_domain_file_page_service_stub = (
            DiscoverSpaceKnowledgeDomainFilePageServiceStub(capabilities_common_channel)
        )
        Registry.register_service(
            "discover_space_knowledge_domain_file_page_service_stub",
            discover_space_knowledge_domain_file_page_service_stub,
        )

        delete_space_knowledge_domain_file_page_service_stub = (
            DeleteSpaceKnowledgeDomainFilePageServiceStub(capabilities_common_channel)
        )
        Registry.register_service(
            "delete_space_knowledge_domain_file_page_service_stub",
            delete_space_knowledge_domain_file_page_service_stub,
        )

        # PARA STUBS
        create_space_knowledge_domain_file_page_para_service_stub = (
            CreateSpaceKnowledgeDomainFilePageParaServiceStub(
                capabilities_common_channel
            )
        )
        Registry.register_service(
            "create_space_knowledge_domain_file_page_para_service_stub",
            create_space_knowledge_domain_file_page_para_service_stub,
        )

        access_space_knowledge_domain_file_page_para_service_stub = (
            AccessSpaceKnowledgeDomainFilePageParaServiceStub(
                capabilities_common_channel
            )
        )
        Registry.register_service(
            "access_space_knowledge_domain_file_page_para_service_stub",
            access_space_knowledge_domain_file_page_para_service_stub,
        )

        discover_space_knowledge_domain_file_page_para_service_stub = (
            DiscoverSpaceKnowledgeDomainFilePageParaServiceStub(
                capabilities_common_channel
            )
        )
        Registry.register_service(
            "discover_space_knowledge_domain_file_page_para_service_stub",
            discover_space_knowledge_domain_file_page_para_service_stub,
        )

        delete_space_knowledge_domain_file_page_para_service_stub = (
            DeleteSpaceKnowledgeDomainFilePageParaServiceStub(
                capabilities_common_channel
            )
        )
        Registry.register_service(
            "delete_space_knowledge_domain_file_page_para_service_stub",
            delete_space_knowledge_domain_file_page_para_service_stub,
        )

        # --------------------------------------------
        # COGNITIVE ASSIST KNOWLEDGE RETRIEVER STUBS
        # --------------------------------------------

        retriever_knowledge_service_stub = RetrieverKnowledgeServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "retriever_knowledge_service_stub", retriever_knowledge_service_stub
        )

        # --------------------------------------------
        # COGNITIVE ASSIST KNOWLEDGE READER STUBS
        # --------------------------------------------

        reader_knowledge_service_stub = ReaderKnowledgeServiceStub(
            capabilities_common_channel
        )
        Registry.register_service(
            "reader_knowledge_service_stub", reader_knowledge_service_stub
        )

        # --------------------------------------------
        # CREATE PODS STUBS
        # --------------------------------------------

        create_pod_service_stub = CreatePodsServiceStub(capabilities_common_channel)
        Registry.register_service("create_pod_service_stub", create_pod_service_stub)

        logging.info("Created pods service stub")

        # adding channels to registry
        Registry.register_service("grpc_channels", channels)
        return

    # ------------------------------------------------------
    # Identity Services
    # ------------------------------------------------------

    @staticmethod
    def __register_machine_services():
        discover_machine_service = DiscoverMachineService()
        Registry.register_service("discover_machine_service", discover_machine_service)
        return
