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
from support.helper_functions import format_datetime_to_timestamp, format_timestamp_to_datetime, get_current_timestamp

AccountConnectionModels = declarative_base()


class AccountConnections:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.account_assistant_connection_model_name = f"aac_{account_id}"
        self.account_connection_model_name = f"ac_{account_id}"
        AccountConnectionModels.metadata.reflect(bind=DbSession.get_engine())
        try:
            self.account_assistant_connection_table = AccountConnectionModels.metadata.tables[
                self.account_assistant_connection_model_name]
            self.account_connection_table = AccountConnectionModels.metadata.tables[self.account_connection_model_name]
        except KeyError:
            self.account_assistant_connection_table = None
            self.account_connection_table = None

    # Setup Account Connection
    def setup_account_connections(self):
        self.get_account_assistant_connection_model().__table__.create(bind=DbSession.get_engine())
        self.get_account_connection_model().__table__.create(bind=DbSession.get_engine())
        logging.info(f'account connections setup successfully for account id: {self.account_id}')
        return

    # Account Assistant Connection
    def get_account_assistant_connection_model(self):
        class AccountAssistantConnection(AccountConnectionModels):
            __tablename__ = self.account_assistant_connection_model_name

            account_assistant_connection_id = Column(String(255), primary_key=True, unique=True)
            account_assistant_id = Column(String(255), nullable=False)
            connected_at = Column(DateTime(), nullable=False)

        return AccountAssistantConnection

    def get_account_assistant_connection_model_name(self):
        return self.account_assistant_connection_model_name

    def add_new_account_assistant_connection(self, account_assistant_connection_id: str, account_assistant_id: str):
        statement = AccountConnectionModels.metadata.tables[
            self.account_assistant_connection_model_name].insert().values(
            account_assistant_connection_id=account_assistant_connection_id,
            account_assistant_id=account_assistant_id,
            connected_at=format_timestamp_to_datetime(get_current_timestamp())
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.flush()
            session.commit()
        return

    def get_connected_account_assistants(self) -> [account_pb2.AccountConnectedAccountAssistant]:
        with DbSession.session_scope() as session:
            all_connected_account_assistant = session.query(self.account_assistant_connection_table).all()
            return [account_pb2.AccountConnectedAccountAssistant(
                account_assistant_connection_id=connected_account_assistant.account_assistant_connection_id,
                account_assistant_id=connected_account_assistant.account_assistant_id,
                connected_at=format_datetime_to_timestamp(connected_account_assistant.connected_at)
            ) for connected_account_assistant in all_connected_account_assistant]

    def is_account_assistant_connected(self, account_assistant_connection_id: str, account_assistant_id: str) -> bool:
        with DbSession.session_scope() as session:
            statement = session.query(self.account_assistant_connection_table).filter(
                self.account_assistant_connection_table.c.account_assistant_connection_id == account_assistant_connection_id,
                self.account_assistant_connection_table.c.account_assistant_id == account_assistant_id
            )
            account_assistant_connected = session.query(statement.exists()).scalar()
            return account_assistant_connected

    # Account Connection
    def get_account_connection_model(self):
        class AccountConnection(AccountConnectionModels):
            __tablename__ = self.account_connection_model_name

            account_connection_id = Column(String(255), primary_key=True, unique=True)
            account_id = Column(String(255), nullable=False)
            account_interested_in_connection = Column(Boolean(), nullable=False)
            connected_account_interested_in_connection = Column(Boolean(), nullable=False)
            connected_at = Column(DateTime, nullable=False)

        return AccountConnection

    def get_account_connection_model_name(self):
        return self.account_connection_model_name

    def get_connected_accounts(self) -> [account_pb2.AccountConnectedAccount]:
        with DbSession.session_scope() as session:
            all_connected_account = session.query(self.account_connection_table).all()
            return [account_pb2.AccountConnectedAccount(
                account_connection_id=connected_account.account_connection_id,
                account_id=connected_account.account_id,
                account_interested_in_connection=connected_account.account_interested_in_connection,
                connected_account_interested_in_connection=connected_account.connected_account_interested_in_connection,
                connected_at=format_datetime_to_timestamp(connected_account.connected_at)
            ) for connected_account in all_connected_account]

    def get_connected_account(self, account_id) -> account_pb2.AccountConnectedAccount:
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
            statement = session.query(self.account_connection_table).filter(
                self.account_connection_table.c.account_connection_id == account_connection_id,
                self.account_connection_table.c.account_id == account_id
            )
            account_connected = session.query(statement.exists()).scalar()
            return account_connected

    def is_account_connection_exists(self, account_id: str) -> bool:
        with DbSession.session_scope() as session:
            statement = session.query(self.account_connection_table).filter(
                self.account_connection_table.c.account_id == account_id
            )
            account_connection_exists = session.query(statement.exists()).scalar()
            return account_connection_exists

    def add_new_account_connection(self, account_connection_id: str, account_id: str, self_connecting: bool):
        statement = AccountConnectionModels.metadata.tables[
            self.account_connection_model_name].insert().values(
            account_connection_id=account_connection_id,
            account_id=account_id,
            account_interested_in_connection=self_connecting,
            connected_account_interested_in_connection=not self_connecting,
            connected_at=format_timestamp_to_datetime(get_current_timestamp())
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.flush()
            session.commit()
        return

    def update_account_interest_in_connection(self, account_id: str, is_interested: bool):
        statement = (update(self.account_connection_table).where(
            self.account_connection_table.c.account_id == account_id).values(
            account_interested_in_connection=is_interested))
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return

    def update_connected_account_interest_in_connection(self, account_id: str, is_interested: bool):
        statement = (update(self.account_connection_table).where(
            self.account_connection_table.c.account_id == account_id).values(
            connected_account_interested_in_connection=is_interested))
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return
