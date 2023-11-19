from application_context import ApplicationContext
from ethos.elint.entities.account_pb2 import AccountConnectedAccountAssistant, AccountConnectedAccount
from ethos.elint.services.product.identity.account.access_account_pb2 import AccountServicesAccessAuthDetails
from ethos.elint.services.product.identity.account.connect_account_pb2 import IsAccountAssistantConnectedRequest, \
    IsAccountConnectedRequest
from ethos.elint.services.product.identity.account.notify_account_pb2 import \
    NewReceivedMessageFromAccountAssistantRequest, NewReceivedMessageFromAccountRequest


def validate_account_services_caller(
        access_auth_details: AccountServicesAccessAuthDetails) -> (bool, str):
    stub = ApplicationContext.access_account_service_stub()
    response = stub.ValidateAccountServices(access_auth_details)
    return (response.account_service_access_validation_done,
            response.account_service_access_validation_message)


def is_account_assistant_connected_caller(
        account_id: str, connected_account_assistant: AccountConnectedAccountAssistant) -> (bool, str):
    stub = ApplicationContext.connect_account_service_stub()
    response = stub.IsAccountAssistantConnected(IsAccountAssistantConnectedRequest(
        account_id=account_id, connected_account_assistant=connected_account_assistant))
    return response.meta_done, response.meta_message


def is_account_connected_caller(account_id: str, connected_account: AccountConnectedAccount) -> (bool, str):
    stub = ApplicationContext.connect_account_service_stub()
    response = stub.IsAccountConnected(IsAccountConnectedRequest(
        account_id=account_id,
        connected_account=connected_account
    ))
    return response.meta_done, response.meta_message


def new_received_message_from_account_assistant_caller(account_id: str,
                                                       connecting_account_assistant_id: str,
                                                       message: str) -> (bool, str):
    stub = ApplicationContext.notify_account_service_stub()
    response = stub.NewReceivedMessageFromAccountAssistant(
        NewReceivedMessageFromAccountAssistantRequest(
            account_id=account_id,
            connecting_account_assistant_id=connecting_account_assistant_id,
            message=message,
        ))
    return response.meta_done, response.meta_message


def new_received_message_from_account_caller(account_id: str, connecting_account_id: str, message: str) -> (bool, str):
    stub = ApplicationContext.notify_account_service_stub()
    response = stub.NewReceivedMessageFromAccount(
        NewReceivedMessageFromAccountRequest(
            account_id=account_id,
            connecting_account_id=connecting_account_id,
            message=message
        ))
    return response.meta_done, response.meta_message
