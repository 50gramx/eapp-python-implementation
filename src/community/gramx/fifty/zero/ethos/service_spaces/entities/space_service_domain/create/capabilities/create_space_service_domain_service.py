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

import ethos.elint.collars.DC499999999_pb2 as DC499999999_pb2
from ethos.elint.collars.DC499999998_pb2 import LaunchVMResponse
from ethos.elint.collars.DC499999998_pb2_grpc import (
    DC499999998EPME5000CapabilitiesServicer,
)
from ethos.elint.collars.DC499999999_caps_pb2 import AuthWithDeployment
from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.service.space_service_domain.create_space_service_domain_pb2_grpc import (
    CreateSpaceServiceDomainServiceServicer,
)

from application_context import ApplicationContext
from src.community.gramx.collars.DC499999998.epme5000_consumer import (
    DC499999998EPME5000Consumer,
)
from src.community.gramx.collars.DC499999999.epme5000_consumer import (
    DC499999999EPME5000Consumer,
)
from src.community.gramx.fifty.zero.ethos.service_spaces.entities.space_service.access.consumers.access_space_service_consumer import (
    AccessSpaceServiceConsumer,
)
from src.community.gramx.fifty.zero.ethos.service_spaces.entities.space_service.discover.consumers.discover_space_service_consumer import (
    DiscoverSpaceServiceConsumer,
)
from src.community.gramx.fifty.zero.ethos.service_spaces.entities.space_service_domain.access.consumers.access_space_service_domain_consumer import (
    AccessSpaceServiceDomainConsumer,
)
from src.community.gramx.fifty.zero.ethos.service_spaces.models.service_space_models import (
    ServiceSpace,
)


class CreateSpaceServiceDomainService(CreateSpaceServiceDomainServiceServicer):
    def __init__(self):
        super(CreateSpaceServiceDomainService, self).__init__()
        self.session_scope = self.__class__.__name__

    def CreateDC499999998(self, request, context):
        logging.info("CreateSpaceServiceDomainService:CreateDC499999998.")
        is_valid, valid_message = (
            AccessSpaceServiceConsumer.validate_space_service_services(
                access_auth_details=request.auth
            )
        )
        meta = ResponseMeta(meta_done=is_valid, meta_message=valid_message)
        if is_valid is False:
            return meta
        else:
            # TODO: pay for the service
            pay_in_stub = ApplicationContext.pay_in_account_service_stub()
            charge_for_closed_domain_launch_response = (
                pay_in_stub.ChargeForClosedDomainLaunch(request)
            )
            if charge_for_closed_domain_launch_response.meta_done is False:
                return ResponseMeta(
                    meta_done=False,
                    meta_message=charge_for_closed_domain_launch_response.meta_message,
                )
            else:
                space_service = request.auth.space_service
                service_space = ServiceSpace(
                    space_service_id=space_service.space_service_id
                )
                collar_code = "DC499999998"
                domains_with_collar = service_space.get_domains_with_collar_code(
                    collar_code=collar_code
                )
                domain_id = ""
                if len(domains_with_collar) == 0:
                    domain_id = service_space.add_new_domain(
                        domain_name=request.name,
                        domain_description=request.description,
                        domain_collar_code=collar_code,
                        domain_isolate=request.is_isolated,
                    )
                    # Empty domain created, now the deployment of the pod should be initiated
                else:
                    domain_id = domains_with_collar[0].id

                DC499999998EPME5000Consumer.launch_vm()
                _, _, space_service_domain = (
                    DiscoverSpaceServiceConsumer.get_space_service_domain_by_id(
                        request.auth,
                        domain_id,
                    )
                )
                domain_access_auth_details, _, _ = (
                    AccessSpaceServiceDomainConsumer.space_service_domain_access_token(
                        request.auth,
                        space_service_domain,
                    )
                )
                return meta

    def CreateDC499999999(self, request, context):
        logging.info("CreateSpaceServiceDomainService:CreateDC499999999.")
        is_valid, valid_message = (
            AccessSpaceServiceConsumer.validate_space_service_services(
                access_auth_details=request.auth
            )
        )
        meta = ResponseMeta(meta_done=is_valid, meta_message=valid_message)
        if is_valid is False:
            return meta
        else:
            # generic validation stuff
            # TODO: pay for the service

            space_service = request.auth.space_service
            service_space = ServiceSpace(
                space_service_id=space_service.space_service_id
            )
            collar_code = "DC499999999"
            domain_id = service_space.add_new_domain(
                domain_name=request.name,
                domain_description=request.description,
                domain_collar_code=collar_code,
                domain_isolate=request.is_isolated,
            )

            _, _, space_service_domain = (
                DiscoverSpaceServiceConsumer.get_space_service_domain_by_id(
                    request.auth,
                    domain_id,
                )
            )
            domain_access_auth_details, _, _ = (
                AccessSpaceServiceDomainConsumer.space_service_domain_access_token(
                    request.auth,
                    space_service_domain,
                )
            )

            deployment = request.dc499999999.deployment
            req = AuthWithDeployment(
                auth=domain_access_auth_details,
                deployment=deployment,
            )
            DC499999999EPME5000Consumer.create(request=req)

            return meta
