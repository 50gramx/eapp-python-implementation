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

from db_session import DbSession
from models.base_models import AccountAssistant
from support.database.account_services import get_account
from support.db_service import add_new_entity
from support.format_proto_entities import format_account_assistant_to_entity
from support.helper_functions import gen_uuid, get_current_timestamp, \
    format_timestamp_to_datetime


def get_account_assistant(account: account_pb2.Account) -> account_assistant_pb2.AccountAssistant:
    with DbSession.session_scope() as session:
        account_assistant = session.query(AccountAssistant).filter(
            AccountAssistant.account_id == account.account_id
        ).first()
        return format_account_assistant_to_entity(
            account=account,
            account_assistant=account_assistant,
            session=session
        )


def get_account_assistant_by_id(account_assistant_id: str) -> account_assistant_pb2.AccountAssistant:
    with DbSession.session_scope() as session:
        account_assistant = session.query(AccountAssistant).filter(
            AccountAssistant.account_assistant_id == account_assistant_id
        ).first()
        account = get_account(account_id=account_assistant.account_id)
        return format_account_assistant_to_entity(
            account=account,
            account_assistant=account_assistant,
            session=session
        )


def get_account_assistant_meta(account_id: str = None, account_assistant_id: str = None) -> AccountAssistantMeta:
    with DbSession.session_scope() as session:
        if account_id is not None:
            account_assistant = session.query(AccountAssistant).filter(
                AccountAssistant.account_id == account_id
            ).first()
        else:
            account_assistant = session.query(AccountAssistant).filter(
                AccountAssistant.account_assistant_id == account_assistant_id
            ).first()
        return AccountAssistantMeta(
            account_assistant_id=account_assistant.account_assistant_id,
            account_assistant_name_code=account_assistant.account_assistant_name_code,
            account_assistant_name=account_assistant.account_assistant_name,
            account_id=account_assistant.account_id
        )


def add_new_account_assistant(account_id: str, account_assistant_name_code: int, account_assistant_name: str) -> str:
    created_at = get_current_timestamp()
    last_assisted_at = get_current_timestamp()
    account_assistant_id = gen_uuid()
    new_account_assistant = AccountAssistant(
        account_assistant_id=account_assistant_id,
        account_assistant_name_code=account_assistant_name_code,
        account_assistant_name=account_assistant_name,
        account_id=account_id,
        created_at=format_timestamp_to_datetime(created_at),
        last_assisted_at=format_timestamp_to_datetime(last_assisted_at)
    )
    add_new_entity(new_account_assistant)
    return account_assistant_id
