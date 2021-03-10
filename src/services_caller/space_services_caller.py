from application_context import ApplicationContext
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails
from ethos.elint.services.product.identity.space.access_space_pb2 import SpaceServicesAccessAuthDetails


def assist_space_access_token(access_auth_details: AccountAssistantServicesAccessAuthDetails) -> (
        bool, str, SpaceServicesAccessAuthDetails):
    stub = ApplicationContext.access_space_service_stub()
    response = stub.AssistSpaceAccessToken(access_auth_details)
    return (
        response.space_services_access_done,
        response.space_services_access_message,
        response.space_services_access_auth_details)


def validate_space_services_caller(
        access_auth_details: SpaceServicesAccessAuthDetails) -> (bool, str):
    stub = ApplicationContext.access_space_service_stub()
    response = stub.ValidateSpaceServices(access_auth_details)
    return (response.space_service_access_validation_done,
            response.space_service_access_validation_message)
