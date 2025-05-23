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


from ethos.elint.collars.DC499999998_pb2 import LaunchVMRequest, LaunchVMResponse

from src.application_context import ApplicationContext


class DC499999998EPME5000Consumer:

    @staticmethod
    def launch_vm() -> LaunchVMResponse:
        stub = ApplicationContext.dc499999998_epme5000_capabilities_stub()
        response = stub.LaunchVM(LaunchVMRequest())
        return response
