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

from ethos.elint.services.product.identity.account.access_account_pb2 import (
    AccountServicesAccessAuthDetails,
    ValidateAccountServicesResponse,
)

from support.database.account_services import get_account
from support.session_manager import is_persistent_session_valid


def validate_account_services_impl(
    request: AccountServicesAccessAuthDetails, session_scope: str
):
    if request.account.account_id == "":
        logging.info("account id is null, returning")
        return ValidateAccountServicesResponse(
            account_service_access_validation_done=False,
            account_service_access_validation_message="Invalid Request. This action will be reported.",
        )
    account_id = request.account.account_id
    # validate the account
    try:
        account_mismatch = get_account(account_id=account_id).account_id != account_id
    except:
        return ValidateAccountServicesResponse(
            account_service_access_validation_done=False,
            account_service_access_validation_message="Requesting account is not legit. This action will be reported.",
        )

    if account_mismatch:
        # create the response here
        logging.info("account id mis-match, will return")
        return ValidateAccountServicesResponse(
            account_service_access_validation_done=False,
            account_service_access_validation_message="Requesting account is not legit. This action will be reported.",
        )
    else:
        # validate the session
        session_valid, session_valid_message = is_persistent_session_valid(
            request.account_services_access_session_token_details.session_token,
            account_id,
            session_scope,
        )
        return ValidateAccountServicesResponse(
            account_service_access_validation_done=session_valid,
            account_service_access_validation_message=session_valid_message,
        )
