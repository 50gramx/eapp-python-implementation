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
from concurrent import futures

from eapp_python_domain.gramx.fifty.zero.ethos.identity.multiverse.core.entity.epme_1005.capability.discover_epme_1005_pb2_grpc import \
    DiscoverEPME1005Servicer
from google.auth.transport import grpc


class DiscoverEPME1005Provider(DiscoverEPME1005Servicer):
    def __init__(self):
        super(DiscoverEPME1005Provider, self).__init__()
        self.session_scope = self.__class__.__name__

    def host_provider(self):
        # Bind ThreadPoolExecutor and Services to server
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=1)
        )
        pass

    def EPMCC2101(self, request_iterator, context):
        logging.info("DiscoverEPME1005EPMCC2101Provider")
