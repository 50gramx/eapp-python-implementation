from helpers.registry import Registry
from service.onboard_account_service import OnboardAccountService
from service.onboard_organization_space_service import OnboardOrganizationSpaceService


class Loader(object):

    @staticmethod
    def init_identity_context(app_root_path: str):
        Loader.__init_services(app_root_path)
        return

    @staticmethod
    def __init_services(app_root_path: str):
        onboard_organization_space_service = OnboardOrganizationSpaceService()
        Registry.register_service('onboard_organization_space_service', onboard_organization_space_service)

        onboard_account_service = OnboardAccountService()
        Registry.register_service('onboard_account_service', onboard_account_service)
