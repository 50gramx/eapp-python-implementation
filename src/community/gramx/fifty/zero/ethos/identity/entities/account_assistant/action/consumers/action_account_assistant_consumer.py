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
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails
from ethos.elint.services.product.identity.account_assistant.action_account_assistant_pb2 import \
    ActOnAccountMessageRequest

from application_context import ApplicationContext


class ActionAccountAssistantConsumer:

    @staticmethod
    def act_on_account_message(access_auth_details: AccountAssistantServicesAccessAuthDetails, space_knowledge_action,
                               connected_account: AccountAssistantConnectedAccount, message):
        stub = ApplicationContext.action_account_assistant_service_stub()
        request = ActOnAccountMessageRequest(
            access_auth_details=access_auth_details,
            space_knowledge_action=space_knowledge_action,
            connected_account=connected_account,
            message=message
        )
        stub.ActOnAccountMessage(request)
