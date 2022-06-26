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

from access.account_assistant.service_authentication import AccessAccountAssistantServicesAuthentication
from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantAccessTokenResponse, ValidateAccessMeta
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2_grpc import \
    AccessAccountAssistantServiceServicer
from services_caller.account_assistant_service_caller import get_account_assistant_by_account_caller
from services_caller.account_service_caller import validate_account_services_caller, get_account_by_id_caller
from support.db_service import get_account_assistant
from support.session_manager import is_persistent_session_valid


class AccessAccountAssistantService(AccessAccountAssistantServiceServicer):
    def __init__(self):
        super(AccessAccountAssistantService, self).__init__()
        self.session_scope = self.__class__.__name__

    def AccountAssistantAccessToken(self, request, context):
        logging.info("AccessAccountAssistantService:AccountAssistantAccessToken")
        validation_done, validate_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validate_message)
        if validation_done is False:
            return AccountAssistantAccessTokenResponse(meta=response_meta)
        else:
            return AccountAssistantAccessTokenResponse(
                account_assistant_services_access_auth_details=AccessAccountAssistantServicesAuthentication(
                    session_scope=self.session_scope,
                    account_assistant=get_account_assistant(account=request.account)
                ).create_authentication_details(),
                meta=response_meta
            )

    def AccountAssistantAccessTokenWithMasterConnection(self, request, context):
        logging.info("AccessAccountAssistantService:AccountAssistantAccessTokenWithMasterConnection")
        account, _, _ = get_account_by_id_caller(account_id=request.connected_account.account_id)
        account_assistant = get_account_assistant_by_account_caller(account=account)
        if account_assistant.account_assistant_id != request.account_assistant_id:
            return AccountAssistantAccessTokenResponse(meta=ResponseMeta(
                meta_done=False,
                meta_message="Connecting account is not the master account of the assistant"))
        else:
            return AccountAssistantAccessTokenResponse(
                account_assistant_services_access_auth_details=AccessAccountAssistantServicesAuthentication(
                    session_scope=self.session_scope,
                    account_assistant=account_assistant
                ).create_authentication_details(),
                meta=ResponseMeta(
                    meta_done=True,
                    meta_message="Access given.")
            )

    def ValidateAccountAssistantServices(self, request, context):
        logging.info("AccessAccountAssistantService:AccountAssistantAccessToken")
        session_valid, session_valid_message = is_persistent_session_valid(
            session_token=request.account_assistant_services_access_session_token_details.session_token,
            account_identifier=request.account_assistant.account_assistant_id,
            session_scope=self.session_scope
        )
        return ValidateAccessMeta(
            validation_done=session_valid,
            validation_message=session_valid_message
        )
