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

from application_context import ApplicationContext
from ethos.elint.entities import account_pb2
from ethos.elint.entities.account_pb2 import AccountConnectedAccount
from ethos.elint.services.product.identity.account.access_account_pb2 import AccountServicesAccessAuthDetails
from ethos.elint.services.product.identity.account.connect_account_pb2 import ConnectAccountRequest
from ethos.elint.services.product.identity.account.discover_account_pb2 import GetAccountByIdRequest, \
    IsAccountExistsWithMobileRequest
from ethos.elint.services.product.identity.account.notify_account_pb2 import AccountConnectedAccountNotificationRequest


def validate_account_services_caller(
        access_auth_details: AccountServicesAccessAuthDetails) -> (bool, str):
    logging.info("validate_account_services_caller")
    stub = ApplicationContext.access_account_service_stub()
    logging.info("fetched stub, will call")
    response = stub.ValidateAccountServices(access_auth_details)
    logging.info("response received")
    return (response.account_service_access_validation_done,
            response.account_service_access_validation_message)


def get_account_by_id_caller(account_id: str) -> (account_pb2.Account, bool, str):
    stub = ApplicationContext.discover_account_service_stub()
    response = stub.GetAccountById(GetAccountByIdRequest(account_id=account_id))
    return response.account, response.response_meta.meta_done, response.response_meta.meta_message


def is_account_exists_with_mobile_caller(access_auth_details: AccountServicesAccessAuthDetails,
                                         account_country_code: str, account_mobile_number: str) -> (bool, str):
    stub = ApplicationContext.discover_account_service_stub()
    response = stub.IsAccountExistsWithMobile(IsAccountExistsWithMobileRequest(
        access_auth_details=access_auth_details, account_country_code=account_country_code,
        account_mobile_number=account_mobile_number))
    return response.meta_done, response.meta_message


def connect_account_caller(access_auth_details: AccountServicesAccessAuthDetails,
                           connecting_account_id: str) -> (bool, str, AccountConnectedAccount):
    stub = ApplicationContext.connect_account_service_stub()
    response = stub.ConnectAccount(ConnectAccountRequest(
        access_auth_details=access_auth_details, connecting_account_id=connecting_account_id))
    return response.response_meta.meta_done, response.response_meta.meta_message, response.connected_account


def account_connected_account_notification_caller(
        account: account_pb2.Account,
        connecting_account_connected_account: account_pb2.AccountConnectedAccount) -> (bool, str):
    stub = ApplicationContext.notify_account_service_stub()
    response = stub.AccountConnectedAccountNotification(AccountConnectedAccountNotificationRequest(
        account=account,
        connecting_account_connected_account=connecting_account_connected_account
    ))
    return response.meta_done, response.meta_message
