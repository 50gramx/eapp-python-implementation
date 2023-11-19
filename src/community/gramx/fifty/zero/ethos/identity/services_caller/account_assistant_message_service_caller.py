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

from application_context import ApplicationContext
from ethos.elint.entities.account_assistant_pb2 import AccountAssistantConnectedAccount
from ethos.elint.services.product.conversation.message.account_assistant.send_account_assistant_message_pb2 import \
    MessageForAccount
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails


def send_message_to_account(access_auth_details: AccountAssistantServicesAccessAuthDetails,
                            connected_account: AccountAssistantConnectedAccount, message: str,
                            message_source_space_id: str, message_source_space_type_id: str,
                            message_source_space_domain_id: str, message_source_space_domain_action: int,
                            message_source_space_domain_action_context_id: str, message_source):
    stub = ApplicationContext.send_account_assistant_message_service_stub()
    response = stub.SendMessageToAccount(MessageForAccount(
        access_auth_details=access_auth_details,
        connected_account=connected_account,
        message=message,
        message_source_space_id=message_source_space_id,
        message_source_space_type_id=message_source_space_type_id,
        message_source_space_domain_id=message_source_space_domain_id,
        message_source_space_domain_action=message_source_space_domain_action,
        message_source_space_domain_action_context_id=message_source_space_domain_action_context_id,
        message_source=message_source
    ))
    return response
