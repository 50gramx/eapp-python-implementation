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
from ethos.elint.services.product.identity.account_assistant.discover_account_assistant_pb2 import \
    GetAccountAssistantMetaByAccountIdResponse, GetAccountAssistantMetaByAccountAssistantIdResponse, \
    GetAccountAssistantByIdResponse, GetAccountAssistantNameCodeByIdResponse
from ethos.elint.services.product.identity.account_assistant.discover_account_assistant_pb2_grpc import \
    DiscoverAccountAssistantServiceServicer

from community.gramx.fifty.zero.ethos.identity.services_caller import validate_account_services_caller
from support.database.account_assistant_services import get_account_assistant, get_account_assistant_meta, \
    get_account_assistant_by_id


class DiscoverAccountAssistantService(DiscoverAccountAssistantServiceServicer):
    def __init__(self):
        super(DiscoverAccountAssistantService, self).__init__()
        self.session_scope = self.__class__.__name__

    def GetAccountAssistantByAccount(self, request, context):
        logging.info("DiscoverAccountAssistantService:GetAccountAssistantByAccount")
        return get_account_assistant(account=request)

    def GetAccountAssistantMetaByAccountId(self, request, context):
        logging.info("DiscoverAccountAssistantService:GetAccountAssistantMetaByAccountId")
        validation_done, validate_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validate_message)
        if validation_done is False:
            return GetAccountAssistantMetaByAccountIdResponse(response_meta=response_meta)
        else:
            account_assistant_meta = get_account_assistant_meta(
                account_id=request.account_id)
            return GetAccountAssistantMetaByAccountIdResponse(
                account_assistant_meta=account_assistant_meta,
                response_meta=response_meta
            )

    def GetAccountAssistantMetaByAccountAssistantId(self, request, context):
        logging.info("DiscoverAccountAssistantService:GetAccountAssistantMetaByAccountId")
        validation_done, validate_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validate_message)
        if validation_done is False:
            return GetAccountAssistantMetaByAccountAssistantIdResponse(response_meta=response_meta)
        else:
            account_assistant_meta = get_account_assistant_meta(
                account_assistant_id=request.account_assistant_id)
            return GetAccountAssistantMetaByAccountIdResponse(
                account_assistant_meta=account_assistant_meta,
                response_meta=response_meta
            )

    def GetAccountAssistantById(self, request, context):
        logging.info("DiscoverAccountAssistantService:GetAccountAssistantById")
        validation_done, validate_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validate_message)
        if validation_done is False:
            return GetAccountAssistantByIdResponse(response_meta=response_meta)
        else:
            account_assistant = get_account_assistant_by_id(account_assistant_id=request.account_assistant_id)
            return GetAccountAssistantByIdResponse(account_assistant=account_assistant, response_meta=response_meta)

    def GetAccountAssistantNameCodeById(self, request, context):
        logging.info("DiscoverAccountAssistantService:GetAccountAssistantNameCodeById")
        account_assistant = get_account_assistant_by_id(account_assistant_id=request.account_assistant_id)
        return GetAccountAssistantNameCodeByIdResponse(
            account_assistant_name_code=account_assistant.account_assistant_name_code,
            account_assistant_name=account_assistant.account_assistant_name
        )
