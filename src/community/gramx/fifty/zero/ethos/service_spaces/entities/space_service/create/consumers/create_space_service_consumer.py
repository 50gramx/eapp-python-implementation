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
from ethos.elint.services.product.service.space_service.create_space_service_pb2 import (
    CreateAccountSpaceServiceRequest,
)

from application_context import ApplicationContext
from support.helper_functions import get_current_timestamp


class CreateAccountSpaceServiceConsumer:

    @staticmethod
    def create_account_space_service(access_auth: SpaceServicesAccessAuthDetails):
        stub = ApplicationContext.create_space_service_service_stub()
        print(f"CreateAccountSpaceServiceConsumer: {type(stub)}")
        request = CreateAccountSpaceServiceRequest(
            space_service_access_auth_details=access_auth,
            space_service_name="My Service Space",
            requested_at=get_current_timestamp(),
        )
        return stub.CreateAccountSpaceService(request)
