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


from src.community.gramx.collars.DC499999998.epme5000_capabilities import (
    DC499999998EPME5000Capabilities,
)
from support.application.registry import Registry


def register_DC499999998_services(aio: bool):
    if aio:
        pass
    else:
        dc499999998_epme5000_capabilities = DC499999998EPME5000Capabilities()
        Registry.register_service(
            "dc499999998_epme5000_capabilities", dc499999998_epme5000_capabilities
        )
    return
