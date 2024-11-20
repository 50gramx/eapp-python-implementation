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


from ethos.elint.collars.DC499999999_caps_pb2 import AuthWithDeployment
from ethos.elint.entities.generic_pb2 import ResponseMeta

from src.application_context import ApplicationContext


class DC499999999EPME5000Consumer:

    @staticmethod
    def create(request: AuthWithDeployment) -> ResponseMeta:
        stub = ApplicationContext.dc499999999_epme5000_capabilities_stub()
        response = stub.Create(request)
        return response
