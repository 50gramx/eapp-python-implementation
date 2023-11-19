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


from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

from db_session import DbSession

PayIn = declarative_base()


class AccountPayIn(PayIn):
    __tablename__ = "account_pay_in"

    account_id = Column(String(255), primary_key=True)
    account_pay_id = Column(String(255), primary_key=True)


def add_new_account_pay_in(account_id: str, account_pay_id: str) -> None:
    with DbSession.session_scope() as session:
        session.add(AccountPayIn(account_id=account_id, account_pay_id=account_pay_id))
        session.commit()
    return


def get_account_pay_in_id(account_id: str) -> str:
    with DbSession.session_scope() as session:
        account_pay_in = session.query(AccountPayIn).filter(
            AccountPayIn.account_id == account_id
        ).first()
        return account_pay_in.account_pay_id
