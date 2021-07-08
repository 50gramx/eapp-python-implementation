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

from ethos.elint.entities.account_assistant_pb2 import AccountAssistant
from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account.discover_account_pb2 import GetAccountByIdResponse, \
    AreAccountsExistingWithMobileResponse
from ethos.elint.services.product.identity.account.discover_account_pb2_grpc import DiscoverAccountServiceServicer
from services_caller.account_assistant_service_caller import get_account_assistant_by_account_caller
from services_caller.account_service_caller import validate_account_services_caller
from support.db_service import get_account, is_existing_account_mobile, is_account_billing_active


class DiscoverAccountService(DiscoverAccountServiceServicer):
    def __init__(self):
        super(DiscoverAccountService, self).__init__()
        self.session_scope = self.__class__.__name__

    def GetAccountById(self, request, context):
        logging.info("DiscoverAccountService:GetAccountById")
        return GetAccountByIdResponse(
            account=get_account(account_id=request.account_id),
            response_meta=ResponseMeta(meta_done=True, meta_message="Get complete.")
        )

    # TODO: Complete this service implementation
    # def GetAccountProfilePicture(self, request, context):
    #     logging.info("DiscoverAccountService:GetAccountProfilePicture")
    #     validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
    #     response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
    #     if validation_done is False:
    #         return response_meta
    #     else:
    #         pass

    def GetAccountAssistant(self, request, context):
        logging.info("DiscoverAccountService:GetAccountAssistant")
        validation_done, validation_message = validate_account_services_caller(request)
        if validation_done is False:
            return AccountAssistant()
        else:
            return get_account_assistant_by_account_caller(request.account)

    def IsAccountExistsWithMobile(self, request, context):
        logging.info("DiscoverAccountService:IsAccountExistsWithMobile")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return response_meta
        else:
            is_existing_account = is_existing_account_mobile(account_country_code=request.account_country_code,
                                                             account_mobile_number=request.account_mobile_number)
            if is_existing_account:
                return ResponseMeta(meta_done=True, meta_message="Account exists.")
            else:
                return ResponseMeta(meta_done=False, meta_message="Account doesn't exists.")

    def AreAccountsExistingWithMobile(self, request, context):
        logging.info("DiscoverAccountService:AreAccountsExistingWithMobile")
        # TODO: Optimise this service
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return AreAccountsExistingWithMobileResponse(response_meta=response_meta)
        else:
            for account_mobile in request.account_mobiles:
                yield AreAccountsExistingWithMobileResponse(
                    account_mobiles_exists=AreAccountsExistingWithMobileResponse.AccountMobileExists(
                        account_country_code=account_mobile.account_country_code,
                        account_mobile_number=account_mobile.account_mobile_number,
                        account_exists=is_existing_account_mobile(
                            account_country_code=account_mobile.account_country_code,
                            account_mobile_number=account_mobile.account_mobile_number)
                    ),
                    response_meta=response_meta
                )

    def IsAccountBillingActive(self, request, context):
        logging.info("DiscoverAccountService:IsAccountBillingActive")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return response_meta
        else:
            return ResponseMeta(
                meta_done=is_account_billing_active(account_id=request.account.account_id),
                meta_message="Please check the meta_done for boolean billing status"
            )
