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

from application_context import ApplicationContext
from ethos.elint.entities import account_assistant_pb2, account_pb2
from ethos.elint.entities.account_assistant_pb2 import AccountAssistantConnectedAccount
from ethos.elint.services.product.identity.account.access_account_pb2 import AccountServicesAccessAuthDetails
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails, AccountAssistantAccessTokenWithMasterConnectionRequest
from ethos.elint.services.product.identity.account_assistant.connect_account_assistant_pb2 import ConnectAccountRequest
from ethos.elint.services.product.identity.account_assistant.create_account_assistant_pb2 import \
    GetAccountAssistantNameCodeRequest, CreateAccountAssistantRequest


def account_assistant_access_token_caller(
        access_auth_details: AccountServicesAccessAuthDetails,
) -> (bool, str, AccountAssistantServicesAccessAuthDetails):
    stub = ApplicationContext.access_account_assistant_service_stub()
    response = stub.AccountAssistantAccessToken(access_auth_details)
    return (response.meta.meta_done,
            response.meta.meta_message,
            response.account_assistant_services_access_auth_details)


def account_assistant_access_token_with_master_connection_caller(
        account_assistant_id: str,
        connected_account: AccountAssistantConnectedAccount) -> (bool, str, AccountAssistantServicesAccessAuthDetails):
    stub = ApplicationContext.access_account_assistant_service_stub()
    response = stub.AccountAssistantAccessTokenWithMasterConnection(
        AccountAssistantAccessTokenWithMasterConnectionRequest(
            account_assistant_id=account_assistant_id,
            connected_account=connected_account))
    return response.meta.meta_done, response.meta.meta_message, response.account_assistant_services_access_auth_details


def validate_account_assistant_services_caller(
        access_auth_details: AccountAssistantServicesAccessAuthDetails) -> (bool, str):
    stub = ApplicationContext.access_account_assistant_service_stub()
    response = stub.ValidateAccountAssistantServices(access_auth_details)
    return response.validation_done, response.validation_message


def create_account_assistant_caller(
        access_auth_details: AccountServicesAccessAuthDetails,
        account_assistant_name: str
) -> (bool, str, AccountAssistantServicesAccessAuthDetails):
    stub = ApplicationContext.create_account_assistant_service_stub()
    response = stub.CreateAccountAssistant(
        CreateAccountAssistantRequest(
            access_auth_details=access_auth_details,
            account_assistant_name=account_assistant_name
        )
    )
    return (response.response_meta.meta_done,
            response.response_meta.meta_message,
            response.account_assistant_services_access_auth_details)


def get_account_assistant_by_account_caller(account: account_pb2.Account) -> account_assistant_pb2.AccountAssistant:
    stub = ApplicationContext.discover_account_assistant_service_stub()
    return stub.GetAccountAssistantByAccount(account)


def get_account_assistant_name_code_caller(access_auth_details: AccountServicesAccessAuthDetails,
                                           account_assistant_name: str) -> (bool, str, int):
    stub = ApplicationContext.create_account_assistant_service_stub()
    response = stub.GetAccountAssistantNameCode(
        GetAccountAssistantNameCodeRequest(
            access_auth_details=access_auth_details,
            account_assistant_name=account_assistant_name
        )
    )
    return response.response_meta.meta_done, response.response_meta.meta_message, response.account_assistant_name_code


def connect_account_caller(access_auth_details: AccountAssistantServicesAccessAuthDetails,
                           connecting_account_id: str) -> (bool, str, AccountAssistantConnectedAccount):
    stub = ApplicationContext.connect_account_assistant_service_stub()
    response = stub.ConnectAccount(
        ConnectAccountRequest(
            access_auth_details=access_auth_details,
            connecting_account_id=connecting_account_id)
    )
    return response.response_meta.meta_done, response.response_meta.meta_message, response.connected_account


def get_account_assistant_name_code_by_id(account_assistant_id: str) -> (int, str):
    stub = ApplicationContext.discover_account_assistant_service_stub()
    response = stub.GetAccountAssistantNameCodeById(
        GetAccountAssistantNameCodeByIdRequest(
            account_assistant_id=account_assistant_id
        )
    )
