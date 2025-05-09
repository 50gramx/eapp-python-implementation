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
from ethos.elint.services.product.identity.account.access_account_pb2 import AccountServicesAccessAuthDetails
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails
from ethos.elint.services.product.identity.account_assistant.create_account_assistant_pb2 import \
    GetAccountAssistantNameCodeRequest, CreateAccountAssistantRequest

from application_context import ApplicationContext


class CreateAccountAssistantConsumer:

    @staticmethod
    def get_account_assistant_name_code(access_auth_details: AccountServicesAccessAuthDetails,
                                        account_assistant_name: str) -> (bool, str, int):
        stub = ApplicationContext.create_account_assistant_service_stub()
        response = stub.GetAccountAssistantNameCode(
            GetAccountAssistantNameCodeRequest(
                access_auth_details=access_auth_details,
                account_assistant_name=account_assistant_name
            )
        )
        return response.response_meta.meta_done, response.response_meta.meta_message, response.account_assistant_name_code

    @staticmethod
    def create_account_assistant(
            access_auth_details: AccountServicesAccessAuthDetails,
            account_assistant_name: str
    ) -> (bool, str, AccountAssistantServicesAccessAuthDetails):
        stub = ApplicationContext.create_account_assistant_service_stub()
        response = stub.CreateAccountAssistant(
            CreateAccountAssistantRequest(
                access_auth_details=access_auth_details,
                account_assistant_name=account_assistant_name
            )
        )
        return (response.response_meta.meta_done,
                response.response_meta.meta_message,
                response.account_assistant_services_access_auth_details)
