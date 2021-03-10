from application_context import ApplicationContext
from ethos.elint.entities.space_pb2 import SpaceAccessibilityType, SpaceIsolationType
from ethos.elint.services.product.identity.space.access_space_pb2 import SpaceAccessTokenResponse, \
    ValidateSpaceServicesResponse
from ethos.elint.services.product.identity.space.access_space_pb2_grpc import AccessSpaceServiceServicer
from ethos.elint.services.product.identity.space.create_space_pb2 import CreateAccountSpaceRequest
from services_caller.account_assistant_service_caller import validate_account_assistant_services_caller
from services_caller.account_service_caller import validate_account_services_caller
from support.db_service import get_space
from support.session_manager import create_space_services_access_auth_details, is_persistent_session_valid


class AccessSpaceService(AccessSpaceServiceServicer):
    def __init__(self):
        super(AccessSpaceService, self).__init__()
        self.session_scope = self.__class__.__name__

    def SpaceAccessToken(self, request, context):
        print("AccessSpaceService:SpaceAccessToken invoked.")
        validation_done, validation_message = validate_account_services_caller(access_auth_details=request)

        if validation_done is False:
            return SpaceAccessTokenResponse(
                space_services_access_done=validation_done,
                space_services_access_message=validation_message
            )
        else:
            space = get_space(with_account_id=request.account.account_id)
            if space is None:
                create_space_service_stub = ApplicationContext.create_space_service_stub()
                create_account_space_response = create_space_service_stub.CreateAccountSpace(
                    CreateAccountSpaceRequest(
                        account=request.account, space_accessibility_type=SpaceAccessibilityType.Value('OPEN'),
                        space_isolation_type=SpaceIsolationType.Value('NOT_ISOLATED'),
                        requested_at=request.requested_at))
                space = create_account_space_response.space
            access_auth_details = create_space_services_access_auth_details(
                session_scope=self.session_scope,
                space=space
            )
            return SpaceAccessTokenResponse(
                space_services_access_auth_details=access_auth_details,
                space_services_access_done=validation_done,
                space_services_access_message=validation_message
            )

    def ValidateSpaceServices(self, request, context):
        print("AccessSpaceService:ValidateSpaceServices invoked.")
        space = request.space
        space_services_access_session_token_details = request.space_services_access_session_token_details
        requested_at = request.requested_at

        # validate the space
        if not space.space_id == space.space_id:
            space_service_access_validation_done = False
            space_service_access_validation_message = "Requesting space is not legit. This action will be reported."
            # create the response here
            validate_space_services_response = ValidateSpaceServicesResponse(
                space_service_access_validation_done=space_service_access_validation_done,
                space_service_access_validation_message=space_service_access_validation_message
            )
            return validate_space_services_response
        else:
            # validate the session
            session_valid, session_valid_message = is_persistent_session_valid(
                space_services_access_session_token_details.session_token,
                space.space_id,
                self.session_scope
            )
            # create the response here
            validate_space_services_response = ValidateSpaceServicesResponse(
                space_service_access_validation_done=session_valid,
                space_service_access_validation_message=session_valid_message
            )
            return validate_space_services_response

    def AssistSpaceAccessToken(self, request, context):
        print("AccessSpaceService:AssistSpaceAccessToken invoked.")
        validation_done, validation_message = validate_account_assistant_services_caller(access_auth_details=request)
        if validation_done is False:
            return SpaceAccessTokenResponse(
                space_services_access_done=validation_done,
                space_services_access_message=validation_message
            )
        else:
            space = get_space(with_account_id=request.account_assistant.account.account_id)
            access_auth_details = create_space_services_access_auth_details(
                session_scope=self.session_scope,
                space=space
            )
            return SpaceAccessTokenResponse(
                space_services_access_auth_details=access_auth_details,
                space_services_access_done=validation_done,
                space_services_access_message=validation_message
            )
