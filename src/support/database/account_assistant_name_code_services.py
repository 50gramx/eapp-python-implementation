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


from db_session import DbSession
from models.base_models import AccountAssistantNameCode


def get_account_assistant_name_code(account_assistant_name: str, account_id: str) -> int:
    account_assistant_name = account_assistant_name.lower()
    with DbSession.session_scope() as session:
        # get all the AccountAssistantNameCode which has same name as the user requested
        account_assistant_name_code = session.query(AccountAssistantNameCode).filter(
            AccountAssistantNameCode.account_assistant_name == account_assistant_name
        ).all()
        if len(account_assistant_name_code) > 0:
            # there exists a assistant name as the user requested
            new_name_code = len(account_assistant_name_code) + 1
            # TODO(amit): add limiter till 50
        else:
            new_name_code = 1
        session.add(AccountAssistantNameCode(account_assistant_name=account_assistant_name,
                                             account_assistant_name_code=new_name_code, account_id=account_id))
        session.commit()
        return new_name_code
