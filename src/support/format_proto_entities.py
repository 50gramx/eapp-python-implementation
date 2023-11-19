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
from ethos.elint.entities.account_assistant_pb2 import AccountAssistantMeta
from community.gramx.fifty.zero.ethos.identity.models.base_models import AccountAssistant
from support.helper_functions import format_datetime_to_timestamp


def format_account_assistant_to_entity(
        account: account_pb2.Account,
        account_assistant: AccountAssistant,
        session
) -> account_assistant_pb2.AccountAssistant:
    session.add(account_assistant)
    created_at = account_assistant.created_at
    last_assisted_at = account_assistant.last_assisted_at
    return account_assistant_pb2.AccountAssistant(
        account_assistant_id=account_assistant.account_assistant_id,
        account_assistant_name_code=account_assistant.account_assistant_name_code,
        account_assistant_name=account_assistant.account_assistant_name,
        account=account,
        created_at=format_datetime_to_timestamp(created_at),
        last_assisted_at=format_datetime_to_timestamp(last_assisted_at)
    )


def format_account_assistant_meta_to_entity(
        account_assistant_id: str, account_assistant_name_code: int, account_assistant_name: str, account_id: str
) -> AccountAssistantMeta:
    return AccountAssistantMeta(
        account_assistant_id=account_assistant_id,
        account_assistant_name_code=account_assistant_name_code,
        account_assistant_name=account_assistant_name,
        account_id=account_id
    )
