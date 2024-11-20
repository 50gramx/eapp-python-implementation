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


from ethos.elint.services.product.service.space_service_domain.discover_space_service_domain_pb2_grpc import (
    DiscoverSpaceServiceDomainServiceServicer,
)


class DiscoverSpaceServiceDomainService(DiscoverSpaceServiceDomainServiceServicer):
    def __init__(self):
        super(DiscoverSpaceServiceDomainService, self).__init__()
        self.session_scope = self.__class__.__name__
