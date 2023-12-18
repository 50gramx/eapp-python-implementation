#   /*************************************************************************
#   *
#   * AMIT KUMAR KHETAN CONFIDENTIAL
#   * __________________
#   *
#   *  [2017] - [2021] Amit Kumar Khetan
#   *  All Rights Reserved.
#   *
#   * NOTICE:  All information contained herein is, and remains
#   * the property of Amit Kumar Khetan and its suppliers,
#   * if any.  The intellectual and technical concepts contained
#   * herein are proprietary to Amit Kumar Khetan
#   * and its suppliers and may be covered by U.S. and Foreign Patents,
#   * patents in process, and are protected by trade secret or copyright law.
#   * Dissemination of this information or reproduction of this material
#   * is strictly forbidden unless prior written permission is obtained
#   * from Amit Kumar Khetan.
#   */
from ethos.elint.entities.account_assistant_pb2 import AccountAssistantConnectedAccount
from ethos.elint.services.product.identity.account.access_account_pb2 import AccountServicesAccessAuthDetails
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails, AccountAssistantAccessTokenWithMasterConnectionRequest

from application_context import ApplicationContext


class AccessAccountAssistantConsumer:

    @staticmethod
    def account_assistant_access_token(
            access_auth_details: AccountServicesAccessAuthDetails,
    ) -> (bool, str, AccountAssistantServicesAccessAuthDetails):
        stub = ApplicationContext.access_account_assistant_service_stub()
        response = stub.AccountAssistantAccessToken(access_auth_details)
        return (response.meta.meta_done,
                response.meta.meta_message,
                response.account_assistant_services_access_auth_details)

    @staticmethod
    def account_assistant_access_token_with_master_connection(
            account_assistant_id: str,
            connected_account: AccountAssistantConnectedAccount) -> (
            bool, str, AccountAssistantServicesAccessAuthDetails):
        stub = ApplicationContext.access_account_assistant_service_stub()
        response = stub.AccountAssistantAccessTokenWithMasterConnection(
            AccountAssistantAccessTokenWithMasterConnectionRequest(
                account_assistant_id=account_assistant_id,
                connected_account=connected_account))
        return response.meta.meta_done, response.meta.meta_message, response.account_assistant_services_access_auth_details

    @staticmethod
    def validate_account_assistant_services(
            access_auth_details: AccountAssistantServicesAccessAuthDetails) -> (bool, str):
        stub = ApplicationContext.access_account_assistant_service_stub()
        response = stub.ValidateAccountAssistantServices(access_auth_details)
        return response.validation_done, response.validation_message
