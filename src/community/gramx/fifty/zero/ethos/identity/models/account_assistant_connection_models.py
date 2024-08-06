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
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from db_session import DbSession
from ethos.elint.entities import account_assistant_pb2
from support.helper_functions import (
    format_timestamp_to_datetime, 
    get_current_timestamp, 
    format_datetime_to_timestamp
)

Base = declarative_base()


class AccountAssistantConnections:
    def __init__(self, account_assistant_id: str):
        self.account_assistant_id = account_assistant_id
        self.account_connection_model_name = f"ac_{account_assistant_id}"
        self.account_assistant_connection_model_name = f"aac_{account_assistant_id}"
        Base.metadata.reflect(bind=DbSession.get_engine())

        self.account_connection_table = Base.metadata.tables.get(self.account_connection_model_name)
        self.account_assistant_connection_table = Base.metadata.tables.get(self.account_assistant_connection_model_name)

    def setup_account_assistant_connections(self):
        self.get_account_connection_model().__table__.create(bind=DbSession.get_engine())
        self.get_account_assistant_connection_model().__table__.create(bind=DbSession.get_engine())
        logging.info(f'Account assistant connections setup successfully for account ID: {self.account_assistant_id}')

    def get_account_connection_model(self):
        class AccountConnection(Base):
            __tablename__ = self.account_connection_model_name

            account_connection_id = Column(String(255), primary_key=True, unique=True)
            account_id = Column(String(255), nullable=False)
            connected_at = Column(DateTime, nullable=False)

        return AccountConnection

    def add_new_account_connection(self, account_connection_id: str, account_id: str):
        statement = Base.metadata.tables[self.account_connection_model_name].insert().values(
            account_connection_id=account_connection_id,
            account_id=account_id,
            connected_at=format_timestamp_to_datetime(get_current_timestamp())
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.flush()
            session.commit()

    def is_account_connected(self, account_id: str) -> bool:
        with DbSession.session_scope() as session:
            statement = session.query(self.account_assistant_connection_table).filter(
                self.account_connection_table.c.account_id == account_id
            )
            return session.query(statement.exists()).scalar()

    def get_connected_account(self, account_id: str) -> account_assistant_pb2.AccountAssistantConnectedAccount:
        with DbSession.session_scope() as session:
            connected_account = session.query(self.account_connection_table).filter(
                self.account_connection_table.c.account_id == account_id
            ).first()

            return account_assistant_pb2.AccountAssistantConnectedAccount(
                account_connection_id=connected_account.account_connection_id,
                account_id=connected_account.account_id,
                connected_at=format_datetime_to_timestamp(connected_account.connected_at)
            )

    def get_account_assistant_connection_model(self):
        class AccountAssistantConnection(Base):
            __tablename__ = self.account_assistant_connection_model_name

            account_assistant_connection_id = Column(String(255), primary_key=True, unique=True)
            account_assistant_id = Column(String(255), nullable=False)
            connected_at = Column(DateTime(), nullable=False)

        return AccountAssistantConnection
    
    def get_account_connection_model_name(self):
        return self.account_connection_model_name

    def get_account_assistant_connection_model_name(self):
        return self.account_assistant_connection_model_name