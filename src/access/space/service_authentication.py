from access.base_access_authentication import BaseAccessAuthentication
from ethos.elint.entities import space_pb2
from ethos.elint.services.product.identity.space.access_space_pb2 import SpaceServicesAccessAuthDetails


class AccessSpaceServicesAuthentication(BaseAccessAuthentication):

    def __init__(self, session_scope: str, space: space_pb2.Space):
        self.space = space
        super(AccessSpaceServicesAuthentication, self).__init__(session_scope=session_scope)

    def create_authentication_details(self) -> SpaceServicesAccessAuthDetails:
        return SpaceServicesAccessAuthDetails(
            space=self.space,
            space_services_access_session_token_details=self._create_persistent_session_token_details(
                account_identifier=self.space.space_id
            ),
            requested_at=self.requested_at
        )
