from db_session import DbSession
from ethos.elint.entities import account_pb2
from models import Account


def is_existing_account_email(account_email_id: str) -> bool:
    """
    checks for the existence of account_email_id in account table as a personal_email_id
    :param account_email_id:
    :return:
    """
    with DbSession.session_scope() as session:
        q = session.query(Account.account_id).filter(
            Account.account_personal_email_id == account_email_id
        )
        account_exists = session.query(q.exists()).scalar()
    return account_exists


def is_existing_account_mobile(account_mobile_number: str) -> bool:
    """
    check for the existence of account_mobile_number in account table as a account_mobile_number
    :param account_mobile_number:
    :return:
    """
    with DbSession.session_scope() as session:
        q = session.query(Account.account_id).filter(
            Account.account_mobile_number == account_mobile_number
        )
        account_exists = session.query(q.exists()).scalar()
        return account_exists


def add_new_account(account: Account):
    with DbSession.session_scope() as session:
        session.add(account)
    return


def get_account(account_id: str = None, account_mobile_number: str = None) -> account_pb2.Account:
    if account_id is not None:
        with DbSession.session_scope() as session:
            account = session.query(Account).filter(
                Account.account_id == account_id
            ).first()
    else:
        with DbSession.session_scope() as session:
            account = session.query(Account).filter(
                Account.account_mobile_number == account_mobile_number
            ).first()
    # create the account obj here wrt proto contract
    account_obj = account_pb2.Account(
        account_analytics_id=account.account_analytics_id,
        account_id=account.account_id,
        account_mobile_number=account.account_mobile_number,
        account_first_name=account.account_first_name,
        account_last_name=account.account_last_name,
        account_birth_at=account.account_born_at,
        account_gender=account.account_gender,
        created_at=account.account_created_at
    )
    return account_obj
