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
from ethos.elint.services.product.identity.space.access_space_pb2 import (
    SpaceServicesAccessAuthDetails,
)
from ethos.elint.services.product.product.space_product.create_space_product_pb2 import (
    CreateAccountSpaceProductRequest,
)

from application_context import ApplicationContext
from support.helper_functions import get_current_timestamp


class CreateAccountSpaceProductConsumer:

    @staticmethod
    def create_account_space_product(access_auth: SpaceServicesAccessAuthDetails):
        stub = ApplicationContext.create_space_product_service_stub()
        print(f"CreateAccountSpaceProductConsumer: {type(stub)}")
        request = CreateAccountSpaceProductRequest(
            space_services_access_auth_details=access_auth,
            space_product_name="My Product Space",
            requested_at=get_current_timestamp(),
        )
        return stub.CreateAccountSpaceProduct(request)
