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

from support.application.registry import Registry


class ApplicationContext(object):

    # ----------  Chain Stubs ---------
    @staticmethod
    def universe_chain_services_stub():
        return Registry.get_service('universe_chain_services_stub')

    @staticmethod
    def community_collaborator_chain_services_stub():
        return Registry.get_service('community_collaborator_chain_services_stub')

    # ----------  Stubs ---------
    @staticmethod
    def create_account_service_stub():
        """
        :rtype: ethos.elint.services.product.identity.account.create_account_pb2_grpc
        """
        return Registry.get_service('create_account_service_stub')

    @staticmethod
    def access_account_service_stub():
        """
        :rtype: ethos.elint.services.product.identity.account.access_account_pb2_grpc
        """
        return Registry.get_service('access_account_service_stub')

    @staticmethod
    def discover_account_service_stub():
        """
        :rtype: ethos.elint.services.product.identity.account.discover_account_pb2_grpc
        """
        return Registry.get_service('discover_account_service_stub')

    @staticmethod
    def connect_account_service_stub():
        return Registry.get_service('connect_account_service_stub')

    @staticmethod
    def notify_account_service_stub():
        return Registry.get_service('notify_account_service_stub')

    @staticmethod
    def pay_in_account_service_stub():
        return Registry.get_service('pay_in_account_service_stub')

    @staticmethod
    def create_space_service_stub():
        """
        :return: ethos.elint.services.product.identity.space.create_space_pb2_grpc
        """
        return Registry.get_service('create_space_service_stub')

    @staticmethod
    def access_space_service_stub():
        """
        :return: ethos.elint.services.product.identity.space.access_space_pb2_grpc
        """
        return Registry.get_service('access_space_service_stub')

    @staticmethod
    def access_account_assistant_service_stub():
        """
        :return: ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2_grpc
        """
        return Registry.get_service('access_account_assistant_service_stub')

    @staticmethod
    def create_account_assistant_service_stub():
        """
        :return: ethos.elint.services.product.identity.account_assistant.create_account_assistant_pb2_grpc
        """
        return Registry.get_service('create_account_assistant_service_stub')

    @staticmethod
    def discover_account_assistant_service_stub():
        """
        :rtype: ethos.elint.services.product.identity.account_assistant.discover_assistant_account_pb2_grpc
        """
        return Registry.get_service('discover_account_assistant_service_stub')

    @staticmethod
    def connect_account_assistant_service_stub():
        """
        :rtype: ethos.elint.services.product.identity.account_assistant.connect_assistant_account_pb2_grpc
        """
        return Registry.get_service('connect_account_assistant_service_stub')

    @staticmethod
    def action_account_assistant_service_stub():
        """
        :rtype: ethos.elint.services.product.identity.account_assistant.action_assistant_account_pb2_grpc
        """
        return Registry.get_service('action_account_assistant_service_stub')

    # --------------------------------
    # Action Stubs
    # --------------------------------
    @staticmethod
    def space_knowledge_action_service_stub():
        return Registry.get_service('space_knowledge_action_service_stub')

    # --------------------------------
    # Conversation Stubs
    # --------------------------------
    @staticmethod
    def message_conversation_service_stub():
        return Registry.get_service('message_conversation_service_stub')

    @staticmethod
    def send_account_message_service_stub():
        return Registry.get_service('send_account_message_service_stub')

    @staticmethod
    def receive_account_message_service_stub():
        return Registry.get_service('receive_account_message_service_stub')

    @staticmethod
    def send_account_assistant_message_service_stub():
        return Registry.get_service('send_account_assistant_message_service_stub')

    @staticmethod
    def receive_account_assistant_message_service_stub():
        return Registry.get_service('receive_account_assistant_message_service_stub')

    # -----------------------------------------
    # Space Knowledge Service Stubs
    # -----------------------------------------
    @staticmethod
    def create_space_knowledge_service_stub():
        """
        :rtype: proto.ethos.elint.services.product.knowledge.space_knowledge.create_space_knowledge_pb2_grpc
        """
        return Registry.get_service('create_space_knowledge_service_stub')

    @staticmethod
    def access_space_knowledge_service_stub():
        """
        :rtype: proto.ethos.elint.services.product.knowledge.space_knowledge.access_space_knowledge_pb2_grpc
        """
        return Registry.get_service('access_space_knowledge_service_stub')

    @staticmethod
    def discover_space_knowledge_services_stub():
        return Registry.get_service('discover_space_knowledge_services_stub')

    # -----------------------------------------
    # Space Knowledge Domain Service Stubs
    # -----------------------------------------
    @staticmethod
    def create_space_knowledge_domain_service_stub():
        """
        :rtype: proto.ethos.elint.services.product.knowledge.space_knowledge_domain.create_space_knowledge_domain_pb2_grpc
        """
        return Registry.get_service('create_space_knowledge_domain_service_stub')

    @staticmethod
    def access_space_knowledge_domain_service_stub():
        """
        :rtype: proto.ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2_grpc
        """
        return Registry.get_service('access_space_knowledge_domain_service_stub')

    @staticmethod
    def discover_space_knowledge_domain_service_stub():
        """
        :rtype: proto.ethos.elint.services.product.knowledge.space_knowledge_domain.discover_space_knowledge_domain_pb2_grpc
        """
        return Registry.get_service('discover_space_knowledge_domain_service_stub')

    # --------------------------------------------------
    # Space Knowledge Domain File Service Stubs
    # --------------------------------------------------
    @staticmethod
    def create_space_knowledge_domain_file_service_stub():
        """
        :rtype: proto.ethos.elint.services.product.knowledge.space_knowledge_domain_file.create_space_knowledge_domain_file_pb2_grpc
        """
        return Registry.get_service('create_space_knowledge_domain_file_service_stub')

    @staticmethod
    def access_space_knowledge_domain_file_service_stub():
        """
        :rtype: proto.ethos.elint.services.product.knowledge.space_knowledge_domain_file.access_space_knowledge_domain_file_pb2_grpc
        """
        return Registry.get_service('access_space_knowledge_domain_file_service_stub')

    @staticmethod
    def delete_space_knowledge_domain_file_service_stub():
        """
        :rtype: proto.ethos.elint.services.product.knowledge.space_knowledge_domain_file.delete_space_knowledge_domain_file_pb2_grpc
        """
        return Registry.get_service('delete_space_knowledge_domain_file_service_stub')

    # --------------------------------------------------
    # Space Knowledge Domain File Page Service Stubs
    # --------------------------------------------------
    @staticmethod
    def create_space_knowledge_domain_file_page_service_stub():
        """
        :rtype: proto.ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.create_space_knowledge_domain_file_page_pb2_grpc
        """
        return Registry.get_service('create_space_knowledge_domain_file_page_service_stub')

    @staticmethod
    def access_space_knowledge_domain_file_page_service_stub():
        """
        :rtype: proto.ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.access_space_knowledge_domain_file_page_pb2_grpc
        """
        return Registry.get_service('access_space_knowledge_domain_file_page_service_stub')

    @staticmethod
    def discover_space_knowledge_domain_file_page_service_stub():
        return Registry.get_service('discover_space_knowledge_domain_file_page_service_stub')

    @staticmethod
    def delete_space_knowledge_domain_file_page_service_stub():
        return Registry.get_service('delete_space_knowledge_domain_file_page_service_stub')

    # ----------------------------------------------------
    # Space Knowledge Domain File Page Para Service Stubs
    # ----------------------------------------------------
    @staticmethod
    def create_space_knowledge_domain_file_page_para_service_stub():
        return Registry.get_service('create_space_knowledge_domain_file_page_para_service_stub')

    @staticmethod
    def access_space_knowledge_domain_file_page_para_service_stub():
        return Registry.get_service('access_space_knowledge_domain_file_page_para_service_stub')

    @staticmethod
    def discover_space_knowledge_domain_file_page_para_service_stub():
        return Registry.get_service('discover_space_knowledge_domain_file_page_para_service_stub')

    @staticmethod
    def delete_space_knowledge_domain_file_page_para_service_stub():
        return Registry.get_service('delete_space_knowledge_domain_file_page_para_service_stub')

    # ----------------------------------------------------
    # Knowledge Retriever Service Stubs
    # ----------------------------------------------------
    @staticmethod
    def retriever_knowledge_service_stub():
        return Registry.get_service('retriever_knowledge_service_stub')

    # ----------  Services ---------
    @staticmethod
    def get_create_account_service():
        """
        :rtype: src.service.onboard_organization_space_service.OnboardOrganizationSpaceService
        """
        return Registry.get_service('create_account_service')

    @staticmethod
    def get_access_account_service():
        """
        :rtype: src.service.onboard_account_service.OnboardAccountService
        """
        return Registry.get_service('access_account_service')

    @staticmethod
    def get_connect_account_service():
        """
        :rtype: src.service.onboard_account_service.OnboardAccountService
        """
        return Registry.get_service('connect_account_service')

    @staticmethod
    def get_discover_account_service():
        return Registry.get_service('discover_account_service')

    @staticmethod
    def get_pay_in_account_service():
        return Registry.get_service('pay_in_account_service')

    @staticmethod
    def get_access_space_service():
        """
        :rtype:
        """
        return Registry.get_service('access_space_service')

    @staticmethod
    def get_create_space_service():
        """
        :rtype: src.service.onboard_account_service.OnboardAccountService
        """
        return Registry.get_service('create_space_service')

    @staticmethod
    def get_access_account_assistant_service():
        """
        :rtype:
        """
        return Registry.get_service('access_account_assistant_service')

    @staticmethod
    def get_create_account_assistant_service():
        """
        :rtype:
        """
        return Registry.get_service('create_account_assistant_service')

    @staticmethod
    def get_connect_account_assistant_service():
        """
        :rtype: src.service.onboard_account_service.OnboardAccountService
        """
        return Registry.get_service('connect_account_assistant_service')

    @staticmethod
    def get_discover_account_assistant_service():
        return Registry.get_service('discover_account_assistant_service')

    @staticmethod
    def get_action_account_assistant_service():
        return Registry.get_service('action_account_assistant_service')

    @staticmethod
    def get_discover_machine_service():
        return Registry.get_service('discover_machine_service')

    @staticmethod
    def get_notify_account_service():
        return Registry.get_service('notify_account_service')

    # ----------------------------------------------------------------
    # Conversations Services
    # ----------------------------------------------------------------

    @staticmethod
    def get_message_conversation_service():
        return Registry.get_service('message_conversation_service')

    @staticmethod
    def get_send_account_message_service():
        return Registry.get_service('send_account_message_service')

    @staticmethod
    def get_receive_account_message_service():
        return Registry.get_service('receive_account_message_service')

    @staticmethod
    def get_send_account_assistant_message_service():
        return Registry.get_service('send_account_assistant_message_service')

    @staticmethod
    def get_receive_account_assistant_message_service():
        return Registry.get_service('receive_account_assistant_message_service')

    # ------------------------------
    # Space Knowledge Services
    # ------------------------------
    @staticmethod
    def get_create_space_knowledge_service():
        """
        :rtype: src.service.space_knowledge.CreateSpaceKnowledgeService
        """
        return Registry.get_service('create_space_knowledge_service')

    @staticmethod
    def get_access_space_knowledge_service():
        """
        :rtype: src.service.space_knowledge.AccessSpaceKnowledgeService
        """
        return Registry.get_service('access_space_knowledge_service')

    @staticmethod
    def get_discover_space_knowledge_service():
        """
        :rtype: src.service.space_knowledge.DiscoverSpaceKnowledgeService
        """
        return Registry.get_service('discover_space_knowledge_service')

    # -------------------------------------
    # Space Knowledge Domain Services
    # -------------------------------------
    @staticmethod
    def get_create_space_knowledge_domain_service():
        """
        :rtype: src.service.space_knowledge_domain.CreateSpaceKnowledgeDomainService
        """
        return Registry.get_service('create_space_knowledge_domain_service')

    @staticmethod
    def get_access_space_knowledge_domain_service():
        """
        :rtype: src.service.space_knowledge_domain.AccessSpaceKnowledgeDomainService
        """
        return Registry.get_service('access_space_knowledge_domain_service')

    @staticmethod
    def get_discover_space_knowledge_domain_service():
        """
        :rtype: src.service.space_knowledge_domain.DiscoverSpaceKnowledgeDomainService
        """
        return Registry.get_service('discover_space_knowledge_domain_service')

    # --------------------------------------------
    # Space Knowledge Domain File Services
    # --------------------------------------------
    @staticmethod
    def get_create_space_knowledge_domain_file_service():
        """
        :rtype: src.service.space_knowledge_domain_file.CreateSpaceKnowledgeDomainFileService
        """
        return Registry.get_service('create_space_knowledge_domain_file_service')

    @staticmethod
    def get_access_space_knowledge_domain_file_service():
        """
        :rtype: src.service.space_knowledge_domain_file.AccessSpaceKnowledgeDomainFileService
        """
        return Registry.get_service('access_space_knowledge_domain_file_service')

    @staticmethod
    def get_delete_space_knowledge_domain_file_service():
        """
        :rtype: src.service.space_knowledge_domain_file.DeleteSpaceKnowledgeDomainFileService
        """
        return Registry.get_service('delete_space_knowledge_domain_file_service')

    # --------------------------------------------
    # Space Knowledge Domain File Page Services
    # --------------------------------------------
    @staticmethod
    def get_create_space_knowledge_domain_file_page_service():
        """
        :rtype: src.service.space_knowledge_domain_file_page.CreateSpaceKnowledgeDomainFilePageService
        """
        return Registry.get_service('create_space_knowledge_domain_file_page_service')

    @staticmethod
    def get_access_space_knowledge_domain_file_page_service():
        """
        :rtype: src.service.space_knowledge_domain_file_page.AccessSpaceKnowledgeDomainFilePageService
        """
        return Registry.get_service('access_space_knowledge_domain_file_page_service')

    @staticmethod
    def get_discover_space_knowledge_domain_file_page_service():
        return Registry.get_service('discover_space_knowledge_domain_file_page_service')

    @staticmethod
    def get_delete_space_knowledge_domain_file_page_service():
        return Registry.get_service('delete_space_knowledge_domain_file_page_service')

    # ---------------------------------------------------
    # Space Knowledge Domain File Page Para Services
    # ---------------------------------------------------
    @staticmethod
    def get_access_space_knowledge_domain_file_page_para_service():
        return Registry.get_service('access_space_knowledge_domain_file_page_para_service')

    @staticmethod
    def get_create_space_knowledge_domain_file_page_para_service():
        return Registry.get_service('create_space_knowledge_domain_file_page_para_service')

    @staticmethod
    def get_discover_space_knowledge_domain_file_page_para_service():
        return Registry.get_service('discover_space_knowledge_domain_file_page_para_service')

    @staticmethod
    def get_delete_space_knowledge_domain_file_page_para_service():
        return Registry.get_service('delete_space_knowledge_domain_file_page_para_service')
