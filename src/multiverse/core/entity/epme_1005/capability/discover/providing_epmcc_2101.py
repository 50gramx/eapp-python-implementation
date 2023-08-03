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

import eapp_python_domain.gramx.seventy.zero.ethos.gramxpro.multiverse.core.entity.epe_1001.contract_pb2 as EPE1001

from multiverse.core.entity.epme_1005.capability.discover.discover_epme_1005_provider import DiscoverEPME1005Provider


def new_fun(a) -> bool:
    return a


class Consumer:
    EPMC = new_fun


class ProvidingEPMCC2101(DiscoverEPME1005Provider):
    def __init__(self):
        super(ProvidingEPMCC2101, self).__init__()
        self.session_scope = self.__class__.__name__
        self.consumer = Consumer

    def providers_context(self):
        # provide this capability
        pass

    def EPMCC2101(self, request_iterator, context):
        logging.info("DiscoverEPME1005EPMCC2101Provider")
        for request in request_iterator:
            if self.consumer.EPMC(request.account_assistant_id) is not None:
                yield EPE1001
        return EPE1001
