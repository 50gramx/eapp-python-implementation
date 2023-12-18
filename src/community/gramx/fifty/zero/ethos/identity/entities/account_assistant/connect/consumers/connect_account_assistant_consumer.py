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
from ethos.elint.services.product.identity.account.connect_account_pb2 import ConnectAccountRequest, \
    IsAccountConnectedRequest
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails

from application_context import ApplicationContext


class ConnectAccountAssistantConsumer:

    @staticmethod
    def connect_account(access_auth_details: AccountAssistantServicesAccessAuthDetails,
                        connecting_account_id: str) -> (bool, str, AccountAssistantConnectedAccount):
        stub = ApplicationContext.connect_account_assistant_service_stub()
        response = stub.ConnectAccount(
            ConnectAccountRequest(
                access_auth_details=access_auth_details,
                connecting_account_id=connecting_account_id)
        )
        return response.response_meta.meta_done, response.response_meta.meta_message, response.connected_account

    @staticmethod
    def is_account_connected(
            account_assistant_id: str, connected_account: AccountAssistantConnectedAccount) -> (bool, str):
        stub = ApplicationContext.connect_account_assistant_service_stub()
        response = stub.IsAccountConnected(IsAccountConnectedRequest(
            account_assistant_id=account_assistant_id, connected_account=connected_account))
        return response.meta_done, response.meta_message
