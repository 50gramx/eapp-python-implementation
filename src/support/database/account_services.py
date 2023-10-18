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


from ethos.elint.entities import account_pb2
from sqlalchemy import exists, and_

from db_session import DbSession
from models.base_models import Account
from support.helper_functions import format_datetime_to_timestamp


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


def is_existing_account_mobile(account_country_code: str, account_mobile_number: str) -> bool:
    """
      Checks for the existence of the specified mobile number and country code in the account table.
      :param account_country_code: The country code of the account.
      :param account_mobile_number: The mobile number of the account.
      :return: True if the mobile number exists, otherwise False.
    """
    with DbSession.session_scope() as session:
        return session.query(
            exists().where(
                and_(
                    Account.account_country_code == account_country_code,
                    Account.account_mobile_number == account_mobile_number
                )
            )
        ).scalar()


def add_new_account(account: Account) -> None:
    with DbSession.session_scope() as session:
        session.add(account)
        session.commit()
    return


def get_account(account_id: str = None, account_mobile_number: str = None) -> account_pb2.Account:
    with DbSession.session_scope() as session:
        if account_id is not None:
            account = session.query(Account).filter(
                Account.account_id == account_id
            ).first()
        else:
            account = session.query(Account).filter(
                Account.account_mobile_number == account_mobile_number
            ).first()
        # TODO: check if account exists
        # create the account obj here wrt proto contract
        account_obj = account_pb2.Account(
            account_analytics_id=account.account_analytics_id,
            account_id=account.account_id,
            account_personal_email_id=account.account_personal_email_id,
            account_work_email_id=account.account_work_email_id,
            account_country_code=account.account_country_code,
            account_mobile_number=account.account_mobile_number,
            account_first_name=account.account_first_name,
            account_last_name=account.account_last_name,
            account_galaxy_id=account.account_galaxy_id,
            account_birth_at=format_datetime_to_timestamp(account.account_birth_at),
            account_gender=account_pb2.AccountGender.Name(int(account.account_gender)),
            created_at=format_datetime_to_timestamp(account.account_created_at),
            account_billing_active=account.account_billing_active
        )
    return account_obj


def is_account_billing_active(account_id: str) -> bool:
    with DbSession.session_scope() as session:
        account = session.query(Account).filter(
            Account.account_id == account_id
        ).first()
        return account.account_billing_active


def activate_account_billing(account_id: str) -> bool:
    try:
        with DbSession.session_scope() as session:
            account = session.query(Account).filter(
                Account.account_id == account_id
            ).first()
            account.account_billing_active = True
            session.commit()
        return True
    except:  # todo: catch them all!
        return False


def deactivate_account_billing(account_id: str) -> bool:
    try:
        with DbSession.session_scope() as session:
            account = session.query(Account).filter(
                Account.account_id == account_id
            ).first()
            account.account_billing_active = False
            session.commit()
        return True
    except:  # todo: catch them all!
        return False
