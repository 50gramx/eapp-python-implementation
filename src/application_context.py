from support.application.registry import Registry


class ApplicationContext(object):

    # ----------  Services ---------
    @staticmethod
    def get_onboard_organization_space_service():
        """
        :rtype: src.service.onboard_organization_space_service.OnboardOrganizationSpaceService
        """
        return Registry.get_service('onboard_organization_space_service')

    @staticmethod
    def get_onboard_account_service():
        """
        :rtype: src.service.onboard_account_service.OnboardAccountService
        """
        return Registry.get_service('onboard_account_service')
