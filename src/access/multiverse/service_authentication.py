from access.base_access_authentication import BaseAccessAuthentication
from ethos.elint.services.product.identity.multiverse.access_multiverse_pb2 import MultiverseServicesAccessAuthDetails
from support.db_service import get_core_collaborator


class AccessMultiverseServicesAuthentication(BaseAccessAuthentication):

    def __init__(self, session_scope: str, collaborator_first_name: str, collaborator_last_name: str,
                 collaborator_community_code: int):
        self.collaborator_first_name = collaborator_first_name
        self.collaborator_last_name = collaborator_last_name
        self.collaborator_community_code = collaborator_community_code
        self.collaborator_identifier = f"{collaborator_first_name}." \
                                       f"{collaborator_last_name}." \
                                       f"{collaborator_community_code}"
        super(AccessMultiverseServicesAuthentication, self).__init__(session_scope=session_scope)

    def _get_core_collaborator(self):
        return get_core_collaborator(
            collaborator_first_name=self.collaborator_first_name,
            collaborator_last_name=self.collaborator_last_name,
            collaborator_community_code=self.collaborator_community_code
        )

    def create_authentication_details(self) -> MultiverseServicesAccessAuthDetails:
        return MultiverseServicesAccessAuthDetails(
            core_collaborator=self._get_core_collaborator,
            multiverse_services_access_session_token_details=self._create_persistent_session_token_details(
                account_identifier=self.collaborator_identifier),
            requested_at=self.requested_at
        )
