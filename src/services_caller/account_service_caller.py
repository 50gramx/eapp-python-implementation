from application_context import ApplicationContext
from ethos.elint.entities import account_pb2
from ethos.elint.entities.account_pb2 import AccountConnectedAccount
from ethos.elint.services.product.identity.account.access_account_pb2 import AccountServicesAccessAuthDetails
from ethos.elint.services.product.identity.account.connect_account_pb2 import ConnectAccountRequest
from ethos.elint.services.product.identity.account.discover_account_pb2 import GetAccountByIdRequest, \
    IsAccountExistsWithMobileRequest


def validate_account_services_caller(
        access_auth_details: AccountServicesAccessAuthDetails) -> (bool, str):
    stub = ApplicationContext.access_account_service_stub()
    response = stub.ValidateAccountServices(access_auth_details)
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
