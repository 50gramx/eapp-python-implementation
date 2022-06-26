from access.base_access_authentication import BaseAccessAuthentication
from ethos.elint.services.product.identity.multiverse.access_multiverse_pb2 import CoreCollaboratorAccessAuthDetails


class AccessCommunityCollaboratorAuthentication(BaseAccessAuthentication):

    def __init__(self, session_scope: str, core_collaborator_name_code: str):
        self.core_collaborator_name_code = core_collaborator_name_code
        super(AccessCommunityCollaboratorAuthentication, self).__init__(session_scope=session_scope)

    def create_core_collaborator_authentication_details(self):
        return CoreCollaboratorAccessAuthDetails(
            core_collaborator_name_code=self.core_collaborator_name_code,
            account_access_auth_session_token_details=self._create_persistent_session_token_details(
                account_identifier=self.core_collaborator_name_code
            )
        )
