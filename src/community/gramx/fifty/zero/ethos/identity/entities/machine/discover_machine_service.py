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

from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.machine.discover_machine_pb2 import ListAllMachinesResponse
from ethos.elint.services.product.identity.machine.discover_machine_pb2_grpc import DiscoverMachineServiceServicer
from community.gramx.fifty.zero.ethos.identity.entities.machine.machine_data_dump import get_all_machines
from community.gramx.fifty.zero.ethos.identity.services_caller import validate_account_services_caller


class DiscoverMachineService(DiscoverMachineServiceServicer):
    def __init__(self):
        super(DiscoverMachineService, self).__init__()
        self.session_scope = self.__class__.__name__

    def ListAllMachines(self, request, context):
        logging.info("DiscoverMachineService:ListAllMachines")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return ListAllMachinesResponse(response_meta=response_meta)
        else:
            return ListAllMachinesResponse(
                machines=get_all_machines(),
                response_meta=response_meta
            )
