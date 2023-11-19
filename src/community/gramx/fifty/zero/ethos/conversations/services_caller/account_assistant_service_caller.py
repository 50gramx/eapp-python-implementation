from application_context import ApplicationContext
from ethos.elint.entities.account_assistant_pb2 import AccountAssistantConnectedAccount
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantAccessTokenWithMasterConnectionRequest, AccountAssistantServicesAccessAuthDetails
from ethos.elint.services.product.identity.account_assistant.connect_account_assistant_pb2 import \
    IsAccountConnectedRequest


def account_assistant_access_token_with_master_connection_caller(
        account_assistant_id: str,
        connected_account: AccountAssistantConnectedAccount) -> (bool, str, AccountAssistantServicesAccessAuthDetails):
    stub = ApplicationContext.access_account_assistant_service_stub()
    response = stub.AccountAssistantAccessTokenWithMasterConnection(
        AccountAssistantAccessTokenWithMasterConnectionRequest(
            account_assistant_id=account_assistant_id,
            connected_account=connected_account))
    return response.meta.meta_done, response.meta.meta_message, response.account_assistant_services_access_auth_details


def is_account_connected_caller(
        account_assistant_id: str, connected_account: AccountAssistantConnectedAccount) -> (bool, str):
    stub = ApplicationContext.connect_account_assistant_service_stub()
    response = stub.IsAccountConnected(IsAccountConnectedRequest(
        account_assistant_id=account_assistant_id, connected_account=connected_account))
    return response.meta_done, response.meta_message


def validate_account_assistant_services_caller(
        access_auth_details: AccountAssistantServicesAccessAuthDetails) -> (bool, str):
    stub = ApplicationContext.access_account_assistant_service_stub()
    response = stub.ValidateAccountAssistantServices(access_auth_details)
    return response.validation_done, response.validation_message
