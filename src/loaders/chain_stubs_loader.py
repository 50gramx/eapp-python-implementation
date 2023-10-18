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

from loader import Loader
from support.application.registry import Registry


class ChainStubsLoader(Loader):

    @staticmethod
    def __init_multiverse_identity_chain_stubs():
        Loader.__init_multiverse_identity_universe_chain_stubs()
        Loader.__init_multiverse_identity_community_collaborator_chain_stubs()

    @staticmethod
    def __init_multiverse_identity_universe_chain_stubs():
        universe_chain_grpc_host = os.environ['EAPP_MULTIVERSE_IDENTITY_UNIVERSE_CHAIN_HOST']
        universe_chain_grpc_port = os.environ['EAPP_MULTIVERSE_IDENTITY_UNIVERSE_CHAIN_PORT']
        host_ip = "{host}:{port}".format(host=universe_chain_grpc_host, port=universe_chain_grpc_port)

        universe_chain_channel = grpc.insecure_channel(host_ip)

        universe_chain_services_stub = UniverseChainServicesStub(universe_chain_channel)
        Registry.register_service('universe_chain_services_stub', universe_chain_services_stub)

    @staticmethod
    def __init_multiverse_identity_community_collaborator_chain_stubs():
        community_collaborator_chain_grpc_host = os.environ[
            'EAPP_MULTIVERSE_IDENTITY_COMMUNITY_COLLABORATOR_CHAIN_HOST']
        community_collaborator_chain_grpc_port = os.environ[
            'EAPP_MULTIVERSE_IDENTITY_COMMUNITY_COLLABORATOR_CHAIN_PORT']
        host_ip = "{host}:{port}".format(host=community_collaborator_chain_grpc_host,
                                         port=community_collaborator_chain_grpc_port)

        community_collaborator_chain_channel = grpc.insecure_channel(host_ip)

        community_collaborator_chain_services_stub = CommunityCollaboratorChainServicesStub(
            community_collaborator_chain_channel)
        Registry.register_service('community_collaborator_chain_services_stub',
                                  community_collaborator_chain_services_stub)
