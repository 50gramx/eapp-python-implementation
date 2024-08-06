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

import logging
from sqlalchemy import Column, String, DateTime, Boolean, update
from sqlalchemy.ext.declarative import declarative_base
from db_session import DbSession
from ethos.elint.entities import account_pb2
from support.helper_functions import (
    format_datetime_to_timestamp, 
    format_timestamp_to_datetime, 
    get_current_timestamp
)

Base = declarative_base()


class AccountConnections:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.account_assistant_connection_model_name = f"aac_{account_id}"
        self.account_connection_model_name = f"ac_{account_id}"
        Base.metadata.reflect(bind=DbSession.get_engine())
        
        self.account_assistant_connection_table = Base.metadata.tables.get(self.account_assistant_connection_model_name)
        self.account_connection_table = Base.metadata.tables.get(self.account_connection_model_name)

    def setup_account_connections(self):
        self.get_account_assistant_connection_model().__table__.create(bind=DbSession.get_engine())
        self.get_account_connection_model().__table__.create(bind=DbSession.get_engine())
        logging.info(f'Account connections setup successfully for account ID: {self.account_id}')

    def get_account_assistant_connection_model(self):
        class AccountAssistantConnection(Base):
            __tablename__ = self.account_assistant_connection_model_name

            account_assistant_connection_id = Column(String(255), primary_key=True, unique=True)
            account_assistant_id = Column(String(255), nullable=False)
            connected_at = Column(DateTime(), nullable=False)

        return AccountAssistantConnection

    def add_new_account_assistant_connection(self, account_assistant_connection_id: str, account_assistant_id: str):
        statement = self.account_assistant_connection_table.insert().values(
            account_assistant_connection_id=account_assistant_connection_id,
            account_assistant_id=account_assistant_id,
            connected_at=format_timestamp_to_datetime(get_current_timestamp())
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()

    def get_connected_account_assistant(self, account_assistant_id: str) -> account_pb2.AccountConnectedAccountAssistant:
        with DbSession.session_scope() as session:
            connected_account_assistant = session.query(self.account_assistant_connection_table).filter(
                self.account_assistant_connection_table.c.account_assistant_id == account_assistant_id
            ).first()
            return account_pb2.AccountConnectedAccountAssistant(
                account_assistant_connection_id=connected_account_assistant.account_assistant_connection_id,
                account_assistant_id=connected_account_assistant.account_assistant_id,
                connected_at=format_datetime_to_timestamp(connected_account_assistant.connected_at)
            )

    def get_connected_account_assistants(self) -> list[account_pb2.AccountConnectedAccountAssistant]:
        with DbSession.session_scope() as session:
            all_connected_account_assistant = session.query(self.account_assistant_connection_table).all()
            return [
                account_pb2.AccountConnectedAccountAssistant(
                    account_assistant_connection_id=connected_account_assistant.account_assistant_connection_id,
                    account_assistant_id=connected_account_assistant.account_assistant_id,
                    connected_at=format_datetime_to_timestamp(connected_account_assistant.connected_at)
                ) for connected_account_assistant in all_connected_account_assistant
            ]

    def is_account_assistant_connected(self, account_assistant_connection_id: str, account_assistant_id: str) -> bool:
        with DbSession.session_scope() as session:
            return session.query(
                session.query(self.account_assistant_connection_table).filter(
                    self.account_assistant_connection_table.c.account_assistant_connection_id == account_assistant_connection_id,
                    self.account_assistant_connection_table.c.account_assistant_id == account_assistant_id
                ).exists()
            ).scalar()

    def is_account_assistant_connection_exists(self, account_assistant_id: str) -> bool:
        with DbSession.session_scope() as session:
            return session.query(
                session.query(self.account_assistant_connection_table).filter(
                    self.account_assistant_connection_table.c.account_assistant_id == account_assistant_id
                ).exists()
            ).scalar()

    def get_account_connection_model(self):
        class AccountConnection(Base):
            __tablename__ = self.account_connection_model_name

            account_connection_id = Column(String(255), primary_key=True, unique=True)
            account_id = Column(String(255), nullable=False)
            account_interested_in_connection = Column(Boolean(), nullable=False)
            connected_account_interested_in_connection = Column(Boolean(), nullable=False)
            connected_at = Column(DateTime, nullable=False)

        return AccountConnection

    def add_new_account_connection(self, account_connection_id: str, account_id: str, self_connecting: bool):
        statement = self.account_connection_table.insert().values(
            account_connection_id=account_connection_id,
            account_id=account_id,
            account_interested_in_connection=self_connecting,
            connected_account_interested_in_connection=not self_connecting,
            connected_at=format_timestamp_to_datetime(get_current_timestamp())
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()

    def get_connected_accounts(self) -> list[account_pb2.AccountConnectedAccount]:
        with DbSession.session_scope() as session:
            all_connected_accounts = session.query(self.account_connection_table).all()
            return [
                account_pb2.AccountConnectedAccount(
                    account_connection_id=connected_account.account_connection_id,
                    account_id=connected_account.account_id,
                    account_interested_in_connection=connected_account.account_interested_in_connection,
                    connected_account_interested_in_connection=connected_account.connected_account_interested_in_connection,
                    connected_at=format_datetime_to_timestamp(connected_account.connected_at)
                ) for connected_account in all_connected_accounts
            ]

    def get_connected_account(self, account_id: str) -> account_pb2.AccountConnectedAccount:
        with DbSession.session_scope() as session:
            connected_account = session.query(self.account_connection_table).filter(
                self.account_connection_table.c.account_id == account_id
            ).first()
            return account_pb2.AccountConnectedAccount(
                account_connection_id=connected_account.account_connection_id,
                account_id=connected_account.account_id,
                account_interested_in_connection=connected_account.account_interested_in_connection,
                connected_account_interested_in_connection=connected_account.connected_account_interested_in_connection,
                connected_at=format_datetime_to_timestamp(connected_account.connected_at)
            )

    def is_account_connected(self, account_connection_id: str, account_id: str) -> bool:
        with DbSession.session_scope() as session:
            return session.query(
                session.query(self.account_connection_table).filter(
                    self.account_connection_table.c.account_connection_id == account_connection_id,
                    self.account_connection_table.c.account_id == account_id
                ).exists()
            ).scalar()

    def is_account_connection_exists(self, account_id: str) -> bool:
        with DbSession.session_scope() as session:
            return session.query(
                session.query(self.account_connection_table).filter(
                    self.account_connection_table.c.account_id == account_id
                ).exists()
            ).scalar()

    def update_account_interest_in_connection(self, account_id: str, is_interested: bool):
        statement = update(self.account_connection_table).where(
            self.account_connection_table.c.account_id == account_id
        ).values(account_interested_in_connection=is_interested)
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()

    def update_connected_account_interest_in_connection(self, account_id: str, is_interested: bool):
        statement = update(self.account_connection_table).where(
            self.account_connection_table.c.account_id == account_id
        ).values(connected_account_interested_in_connection=is_interested)
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
