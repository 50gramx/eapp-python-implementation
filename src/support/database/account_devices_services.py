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


from datetime import datetime

from db_session import DbSession
from models.base_models import AccountDevices


def add_new_account_devices(account_devices: AccountDevices) -> None:
    with DbSession.session_scope() as session:
        session.add(account_devices)
        session.commit()
    return


def update_account_devices(account_id: str, account_device_os: int, account_device_token: str,
                           account_device_token_accessed_at: datetime) -> None:
    with DbSession.session_scope() as session:
        existing_account_devices = session.query(AccountDevices).filter(
            AccountDevices.account_id == account_id
        ).first()
        existing_account_devices.account_device_os = account_device_os
        existing_account_devices.account_device_token = account_device_token
        existing_account_devices.account_device_token_accessed_at = account_device_token_accessed_at
        session.commit()
    return


def check_existing_account_device(account_device_token: str) -> bool:
    with DbSession.session_scope() as session:
        q = session.query(AccountDevices).filter(
            AccountDevices.account_device_token == account_device_token
        )
        return session.query(q.exists()).scalar()



def get_account_device_token(account_id: str) -> str:
    with DbSession.session_scope() as session:
        account_device = session.query(AccountDevices).filter(
            AccountDevices.account_id == account_id
        ).first()
        return account_device.account_device_token

