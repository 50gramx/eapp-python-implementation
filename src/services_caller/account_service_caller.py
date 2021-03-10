from application_context import ApplicationContext
from ethos.elint.entities import account_pb2
from ethos.elint.services.product.identity.account.access_account_pb2 import AccountServicesAccessAuthDetails
from ethos.elint.services.product.identity.account.discover_account_pb2 import GetAccountByIdRequest


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
