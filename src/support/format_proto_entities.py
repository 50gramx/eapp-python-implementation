from ethos.elint.entities import account_pb2, account_assistant_pb2
from models.base_models import AccountAssistant
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
