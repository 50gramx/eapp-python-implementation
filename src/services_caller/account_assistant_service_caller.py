from application_context import ApplicationContext
from ethos.elint.entities import account_assistant_pb2, account_pb2
from ethos.elint.entities.account_assistant_pb2 import AccountAssistantConnectedAccount
from ethos.elint.services.product.identity.account.access_account_pb2 import AccountServicesAccessAuthDetails
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails, AccountAssistantAccessTokenWithMasterConnectionRequest
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
