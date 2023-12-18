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
from ethos.elint.entities import account_pb2, account_assistant_pb2
from ethos.elint.services.product.identity.account_assistant.discover_account_assistant_pb2 import \
    GetAccountAssistantNameCodeByIdRequest

from application_context import ApplicationContext


class DiscoverAccountAssistantConsumer:

    @staticmethod
    def get_account_assistant_by_account(account: account_pb2.Account) -> account_assistant_pb2.AccountAssistant:
        stub = ApplicationContext.discover_account_assistant_service_stub()
        return stub.GetAccountAssistantByAccount(account)

    @staticmethod
    def get_account_assistant_name_code_by_id(account_assistant_id: str) -> (int, str):
        stub = ApplicationContext.discover_account_assistant_service_stub()
        response = stub.GetAccountAssistantNameCodeById(
            GetAccountAssistantNameCodeByIdRequest(
                account_assistant_id=account_assistant_id
            )
        )
        return response.account_assistant_name_code, response.account_assistant_name
