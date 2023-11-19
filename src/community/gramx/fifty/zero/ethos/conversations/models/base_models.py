import logging

from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from db_session import DbSession

Base = declarative_base()


class AccountMessagesInSpeed(Base):
    __tablename__ = "account_messages_in_speed"

    account_id = Column(String(255), primary_key=True)
    sending = Column(Boolean(), nullable=False)
    listening = Column(Boolean(), nullable=False)


def add_account_messages_in_speed(account_id: str) -> None:
    account_messages_in_speed = AccountMessagesInSpeed(
        account_id=account_id,
        sending=False,
        listening=False
    )
    with DbSession.session_scope() as session:
        session.add(account_messages_in_speed)
        session.commit()
    return


class AccountSpeedMessaging:
    def __init__(self, account_id: str):
        self.account_id = account_id

    def account_speed_message_sending_on(self):
        logging.info("account_speed_message_sending_on")
        with DbSession.session_scope() as session:
            account_messages_in_speed = session.query(AccountMessagesInSpeed).filter(
                AccountMessagesInSpeed.account_id == self.account_id
            ).first()
            account_messages_in_speed.sending = True
            session.commit()

    def account_speed_message_sending_off(self):
        logging.info("account_speed_message_sending_off")
        with DbSession.session_scope() as session:
            account_messages_in_speed = session.query(AccountMessagesInSpeed).filter(
                AccountMessagesInSpeed.account_id == self.account_id
            ).first()
            account_messages_in_speed.sending = False
            session.commit()

    def account_speed_message_listening_on(self):
        logging.info("account_speed_message_listening_on")
        with DbSession.session_scope() as session:
            account_messages_in_speed = session.query(AccountMessagesInSpeed).filter(
                AccountMessagesInSpeed.account_id == self.account_id
            ).first()
            account_messages_in_speed.listening = True
            session.commit()

    def account_speed_message_listening_off(self):
        logging.info("account_speed_message_listening_off")
        with DbSession.session_scope() as session:
            account_messages_in_speed = session.query(AccountMessagesInSpeed).filter(
                AccountMessagesInSpeed.account_id == self.account_id
            ).first()
            account_messages_in_speed.listening = False
            session.commit()

    def is_account_speed_message_listening(self) -> bool:
        with DbSession.session_scope() as session:
            account_messages_in_speed = session.query(AccountMessagesInSpeed).filter(
                AccountMessagesInSpeed.account_id == self.account_id
            ).first()
            return account_messages_in_speed.listening
