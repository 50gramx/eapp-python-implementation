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
from ethos.elint.services.product.service.space_service.discover_space_service_pb2 import (
    GetSpaceServiceDomainByIdResponse,
    GetSpaceServiceDomainsResponse,
)
from ethos.elint.services.product.service.space_service.discover_space_service_pb2_grpc import (
    DiscoverSpaceServiceServiceServicer,
)

from community.gramx.fifty.zero.ethos.service_spaces.models.service_space_models import (
    ServiceSpace,
)
from src.community.gramx.fifty.zero.ethos.service_spaces.entities.space_service.access.consumers.access_space_service_consumer import (
    AccessSpaceServiceConsumer,
)


class DiscoverSpaceServiceService(DiscoverSpaceServiceServiceServicer):
    def __init__(self):
        super(DiscoverSpaceServiceService, self).__init__()
        self.session_scope = self.__class__.__name__

    def GetSpaceServiceDomains(self, request, context):
        logging.info("DiscoverSpaceServiceService:GetSpaceServiceDomains")
        validation_done, validation_message = (
            AccessSpaceServiceConsumer.validate_space_service_services(
                access_auth_details=request
            )
        )
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetSpaceServiceDomainsResponse(response_meta=meta)
        else:
            # get all domains
            service_space = ServiceSpace(
                space_service_id=request.space_service.space_service_id
            )
            space_service_domains = service_space.get_domain_all(
                space_service=request.space_service
            )
            return GetSpaceServiceDomainsResponse(
                space_service_domains=space_service_domains, response_meta=meta
            )

    def GetSpaceServiceDomainById(self, request, context):
        validation_done, validation_message = (
            AccessSpaceServiceConsumer.validate_space_service_services(
                access_auth_details=request.access_auth
            )
        )
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetSpaceServiceDomainByIdResponse(response_meta=meta)
        else:
            space_service = request.access_auth.space_service
            service_space = ServiceSpace(
                space_service_id=space_service.space_service_id
            )
            space_service_domain = service_space.get_domain_with_id(
                space_service=space_service, domain_id=request.space_service_domain_id
            )
            return GetSpaceServiceDomainByIdResponse(
                space_service_domain=space_service_domain, response_meta=meta
            )
        
    def GetDomainsByCollarCode(self, request, context):
        validation_done, validation_message = (
            AccessSpaceServiceConsumer.validate_space_service_services(
                access_auth_details=request.access_auth
            )
        )
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetDomainsByCollarCodeResponse(response_meta=meta)
        else:
            space_service = request.access_auth.space_service
            service_space = ServiceSpace(
                space_service_id=space_service.space_service_id
            )
            space_service_domain = service_space.get_domain_with_id(
                space_service=space_service, domain_id=request.space_service_domain_id
            )
            return GetSpaceServiceDomainByIdResponse(
                space_service_domain=space_service_domain, response_meta=meta
            )
